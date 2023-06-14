import sys
from ftplib import FTP
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFileDialog, QLineEdit, QPushButton, QMessageBox
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

        # IP kamera giriş kutusu ve bağlanma düğmesi
        self.camera_label = QLabel("IP Kamera:")
        self.camera_input = QLineEdit()
        self.connect_camera_button = QPushButton("Bağlan")
        self.connect_camera_button.clicked.connect(self.on_connect_camera_button_clicked)

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

        # Dosya indirme ve yükleme düğmeleri
        self.download_button = QPushButton("Dosya İndir")
        self.download_button.clicked.connect(self.on_download_button_clicked)
        self.upload_button = QPushButton("Dosya Yükle")
        self.upload_button.clicked.connect(self.on_upload_button_clicked)

        # Dosya silme ve yeniden adlandırma düğmeleri
        self.delete_button = QPushButton("Dosya Sil")
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.rename_button = QPushButton("Dosya Yeniden Adlandır")
        self.rename_button.clicked.connect(self.on_rename_button_clicked)

        # Dosya ve dizin oluşturma kutusu ve düğmesi
        self.create_file_label = QLabel("Yeni Dosya Adı:")
        self.create_file_input = QLineEdit()
        self.create_file_button = QPushButton("Dosya Oluştur")
        self.create_file_button.clicked.connect(self.on_create_file_button_clicked)
        self.create_dir_label = QLabel("Yeni Dizin Adı:")
        self.create_dir_input = QLineEdit()
        self.create_dir_button = QPushButton("Dizin Oluştur")
        self.create_dir_button.clicked.connect(self.on_create_dir_button_clicked)

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
        left_layout.addWidget(self.camera_label)
        left_layout.addWidget(self.camera_input)
        left_layout.addWidget(self.connect_camera_button)
        left_layout.addWidget(self.host_label)
        left_layout.addWidget(self.host_input)
        left_layout.addWidget(self.username_label)
        left_layout.addWidget(self.username_input)
        left_layout.addWidget(self.password_label)
        left_layout.addWidget(self.password_input)
        left_layout.addWidget(self.connect_button)
        left_layout.addWidget(self.download_button)
        left_layout.addWidget(self.upload_button)
        left_layout.addWidget(self.delete_button)
        left_layout.addWidget(self.rename_button)
        left_layout.addWidget(self.create_file_label)
        left_layout.addWidget(self.create_file_input)
        left_layout.addWidget(self.create_file_button)
        left_layout.addWidget(self.create_dir_label)
        left_layout.addWidget(self.create_dir_input)
        left_layout.addWidget(self.create_dir_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.label)
        right_layout.addWidget(self.video_widget)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def on_connect_camera_button_clicked(self):
        camera_url = self.camera_input.text()
        self.media_player.setMedia(QMediaContent(QUrl(camera_url)))
        self.media_player.play()

    def on_connect_button_clicked(self):
        self.ftp_host = self.host_input.text()
        self.ftp_username = self.username_input.text()
        self.ftp_password = self.password_input.text()

        try:
            ftp = FTP(self.ftp_host)
            ftp.login(self.ftp_username, self.ftp_password)
            self.model.setRootPath("/")
            self.tree_view = QTreeView()
            self.tree_view.setModel(self.model)
            self.tree_view.setRootIndex(self.model.index("/"))
            self.tree_view.doubleClicked.connect(self.on_tree_view_doubleClicked)
            self.tree_view.setWindowTitle("FTP Dosya Sistemi")
            self.tree_view.show()
        except:
            QMessageBox.critical(self, "Hata", "FTP sunucusuna bağlanırken bir hata oluştu.")

    def on_download_button_clicked(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            save_path, _ = QFileDialog.getSaveFileName(self, "Dosya İndir", path.split("/")[-1])
            if save_path:
                ftp = FTP(self.ftp_host)
                ftp.login(self.ftp_username, self.ftp_password)
                with open(save_path, "wb") as file:
                    ftp.retrbinary("RETR " + path, file.write)
                QMessageBox.information(self, "Başarılı", "Dosya indirme tamamlandı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dosya seçin.")

    def on_upload_button_clicked(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Yükle")
            if file_path:
                ftp = FTP(self.ftp_host)
                ftp.login(self.ftp_username, self.ftp_password)
                with open(file_path, "rb") as file:
                    ftp.storbinary("STOR " + path + "/" + file_path.split("/")[-1], file)
                QMessageBox.information(self, "Başarılı", "Dosya yükleme tamamlandı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dizin seçin.")

    def on_delete_button_clicked(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            if QMessageBox.question(self, "Onay", f"{path} dosyasını silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                ftp = FTP(self.ftp_host)
                ftp.login(self.ftp_username, self.ftp_password)
                if path.endswith("/"):
                    ftp.rmd(path)
                else:
                    ftp.delete(path)
                QMessageBox.information(self, "Başarılı", "Dosya silme tamamlandı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dosya seçin.")

    def on_rename_button_clicked(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            new_name, _ = QFileDialog.getSaveFileName(self, "Dosya Yeniden Adlandır", path.split("/")[-1])
            if new_name:
                ftp = FTP(self.ftp_host)
                ftp.login(self.ftp_username, self.ftp_password)
                ftp.rename(path, new_name)
                QMessageBox.information(self, "Başarılı", "Dosya yeniden adlandırma tamamlandı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dosya seçin.")

    def on_create_file_button_clicked(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            file_name = self.create_file_input.text()
            if file_name:
                ftp = FTP(self.ftp_host)
                ftp.login(self.ftp_username, self.ftp_password)
                with open(file_name, "w"):
                    pass
                ftp.storbinary("STOR " + path + "/" + file_name, open(file_name, "rb"))
                self.create_file_input.setText("")
                QMessageBox.information(self, "Başarılı", "Dosya oluşturma tamamlandı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dizin seçin.")

    def on_create_dir_button_clicked(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            dir_name = self.create_dir_input.text()
            if dir_name:
                ftp = FTP(self.ftp_host)
                ftp.login(self.ftp_username, self.ftp_password)
                ftp.mkd(path + "/" + dir_name)
                self.create_dir_input.setText("")
                QMessageBox.information(self, "Başarılı", "Dizin oluşturma tamamlandı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dizin seçin.")

    def on_tree_view_doubleClicked(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            self.tree_view.setRootIndex(index)
        elif self.model.isFile(index):
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.media_player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
