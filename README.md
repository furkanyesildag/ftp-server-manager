# ftp-server-manager
//merhabalar
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QUrl, QFile, QIODevice
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTP Client")

        
        self.ftp_url = "ftp://example.com/"
        self.ftp_username = "username"
        self.ftp_password = "password"

      
        self.model = QFileSystemModel()
        self.model.setRootPath(self.ftp_url)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.model.rootPath()))

        self.net_manager = QNetworkAccessManager(self)

  
        self.media_player = QMediaPlayer()
        self.media_player.setVolume(50)
        self.playlist = QMediaPlaylist(self.media_player)
        self.media_player.setPlaylist(self.playlist)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

  
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.tree)
        left_layout.addStretch()
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.label)
        right_layout.addWidget(self.media_player.videoOutput())
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        self.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)

        if QFile(file_path).isDir():
            return

        mime_type = QFile(file_path).mimeType()
        if mime_type.startswith("audio") or mime_type.startswith("video"):
            self.playlist.clear()
            media_content = QMediaContent(QUrl.fromUserInput(file_path))
            self.playlist.addMedia(media_content)
            self.media_player.play()
            self.label.setText(QFile(file_path).fileName())

            url = QUrl.fromUserInput(file_path)
            request = QNetworkRequest(url)
            request.setAttribute(QNetworkRequest.AuthenticationRequiredAttribute, True)
            request.setRawHeader(b"Authorization", "Basic " + f"{self.ftp_username}:{self.ftp_password}".encode())
            reply = self.net_manager.head(request)
            reply.finished.connect(lambda: self.label.setText(f"{QFile(file_path).fileName()} ({int(reply.header(QNetworkRequest.ContentLengthHeader))//(1024*1024)} MB)"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
