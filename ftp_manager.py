import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFileDialog, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QFile, QIODevice
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTP Client")

        # FTP adresi, kullanıcı adı ve şifresi
        self.ftp_url = ""
        self.ftp_username = ""
        self.ftp_password = ""

        # FTP dosya sistemi modeli ve ağ yöneticisi
        self.model = QFileSystemModel()
        self.net_manager = QNetworkAccessManager(self)

        # FTP server adresi, kullanıcı adı ve şifresi için giriş kutuları ve bağlanma düğmesi
        self.server_address_label = QLabel("Server Adresi:")
        self.server_address_input = QLineEdit()
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
        left_layout.addWidget(self.server_address_label)
        left_layout.addWidget(self.server_address_input)
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
        self.ftp_url = self.server_address_input.text()
        self.ftp_username = self.username_input.text()
        self.ftp_password = self.password_input.text()

        # FTP bağlantısı kontrolü
        request = QNetworkRequest(QUrl(self.ftp_url))
        request.setRawHeader(b"Authorization", f"Basic {self.ftp_username}:{self.ftp_password}".encode())
        reply = self.net_manager.get(request)

        def handle_reply():
            if reply.error() == QNetworkReply.NoError:
                QMessageBox.information(self, "Bağlantı Başarılı", "FTP sunucusuna başarıyla bağlandınız.")
            else:
                QMessageBox.warning(self, "Bağlantı Hatası", "FTP sunucusuna bağlantı başarısız oldu.")

        reply.finished.connect(handle_reply)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
