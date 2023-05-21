import sys
from ftplib import FTP
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFileDialog, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QUrl, QFile, QIODevice
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTP Client")

        # FTP adresi, kullanıcı adı ve şifresi
        self.ftp_host = ""
        self.ftp_username = ""
        self.ftp_password = ""

        # FTP dosya sistemi modeli
        self.model = QFileSystemModel()

        # FTP server adresi, kullanıcı adı ve şifresi için giriş kutuları ve bağlanma düğmesi
        self.host_label = QLabel("FTP Sunucu:")
        self.host_input = QLineEdit()
        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.connect_button = QPushButton("Bağlan")
        self.connect_button.clicked.connect(self.on_connect_button_clicked)

        # Medya oynatıcı, oynatma listesi, video widget'i ve etiket
        self.media_player = QMediaPlayer()
        self.media_player.setVolume(50)
        self.playlist = QMediaPlaylist(self.media_player)
        self.media_player.setPlaylist(self.playlist)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        # Arayüz düzeni
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.host_label)
        left_layout.addWidget(self.host_input)
        left_layout.addWidget(self.username_label)
        left_layout.addWidget(self.username_input)
        left_layout.addWidget(self.password_label)
        left_layout.addWidget(self.password_input)
        left_layout.addWidget(self.connect_button)
        left_layout.addStretch()
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.label)
        right_layout.addWidget(self.video_widget)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def on_connect_button_clicked(self):
        self.ftp_host = self.host_input.text()
        self.ftp_username = self.username_input.text()
        self.ftp_password = self.password_input.text()

        try:
            # FTP bağlantısı oluştur
            ftp = FTP()
            ftp.connect(self.ftp_host)
            ftp.login(self.ftp_username, self.ftp_password)

            # FTP'deki dosya listesini al
            file_list = ftp.nlst()

            # Dosya sistemi modeline dosya listesini ekle
            self.model.setRootPath("/")
            self.tree = QTreeView()
            self.tree.setModel(self.model)
            self.tree.setRootIndex(self.model.index("/"))
            self.tree.doubleClicked.connect(self.on_tree_double_clicked)

            # Dosya listesini göster
            if self.layout().itemAt(0) is not None:
                self.layout().replaceWidget(self.layout().itemAt(0).widget(), self.tree)
            else:
                self.layout().addWidget(self.tree)

            self.label.setText("FTP sunucusuna bağlantı başarılı.")
        except Exception as e:
            self.label.setText("FTP sunucusuna bağlantı başarısız: " + str(e))

    def on_tree_double_clicked(self, index):
        file_path = self.model.filePath(index)

        if QFile.exists(file_path):
            if file_path.lower().endswith((".mp4", ".avi", ".mkv")):
                self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                self.media_player.play()
            else:
                self.media_player.stop()
                self.label.setText("Dosya Türü Desteklenmiyor")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
