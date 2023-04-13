import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal

from youtube import search_youtube
from soundcloud import search_soundcloud
from audio import order

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Coesite")
        # Set window size
        self.width = QGuiApplication.primaryScreen().geometry().width() // 2
        self.height = QApplication.primaryScreen().geometry().height() // 2
        self.setGeometry(self.width // 2, self.height // 2, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        # Create a vertical layout for the widget list
        self.list_layout = QVBoxLayout()

        # Create a widget to hold the text input and the button
        self.search_bar = SearchBar(self.update_list)

        # Create a widget to hold the list of items
        self.list_widget = QWidget()
        self.list_widget.setLayout(self.list_layout)

        # Create folder select widget
        self.folder_select = FolderSelect()

        # Create a vertical layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.folder_select)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.list_widget)

        # Set the main layout for the main window
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create a thread pool
        self.threadpool = QThreadPool()

    def purge_list(self):
        while self.list_layout.count():
            item = self.list_layout.itemAt(0)
            self.list_layout.removeItem(item)
            widget = item.widget()
            widget.setParent(None)

    def update_list(self):
        self.threadpool.clear()
        search_term = self.search_bar.text_input.text()
        worker = SearchWorker(search_term)
        worker.signals.finished.connect(self.update_list_widget)
        self.threadpool.start(worker)

    def update_list_widget(self, results):
        self.purge_list()
        for r in results:
            self.list_layout.addWidget(ListItem(r))

class SearchSignals(QObject):
    finished = pyqtSignal(list)

class SearchWorker(QRunnable):
    def __init__(self, search_term):
        super().__init__()
        self.search_term = search_term
        self.signals = SearchSignals()

    def run(self):
        results = search_youtube(self.search_term, 8)
        results += search_soundcloud(self.search_term)
        results = order(results)
        self.signals.finished.emit(results)

class ListItem(QWidget):

    def __init__(self, songObject: dict):
        super(ListItem, self).__init__()
        self.setAutoFillBackground(True)

        layout = QHBoxLayout()
        self._label = QLabel(f"{songObject['video_name']} - {songObject['channel_name']} ({songObject['audio_quality']})")
        self._url = songObject['url']
        self.button = QPushButton("Download")

        layout.addWidget(self._label)
        layout.addStretch(1)
        layout.addWidget(self.button)

        self.setLayout(layout)

class SearchBar(QWidget):
    def __init__(self, func):
        super(SearchBar, self).__init__()

        self.text_input = QLineEdit()
        self.button = QPushButton("Search")
        self.button.clicked.connect(func)

        s_layout = QHBoxLayout()
        s_layout.addWidget(self.text_input)
        s_layout.addWidget(self.button)

        self.setLayout(s_layout)
        self.setMaximumHeight(50)

class FolderSelect(QWidget):
    def __init__(self):
        super(FolderSelect, self).__init__()

        # Display current folder
        self._folder = QLineEdit(self)
        self._folder.setGeometry(10, 10, 400, 30)

        # Folder changing button
        self.button = QPushButton("Change Folder", self)
        self.button.setGeometry(10, 50, 150, 30)
        self.button.clicked.connect(self.change_folder)

        # Set current as default
        self.cur_folder = os.getcwd()
        self._folder.setText(self.cur_folder)

        # Set layout
        f_layout = QHBoxLayout()
        f_layout.addWidget(self._folder)
        f_layout.addWidget(self.button)

        self.setLayout(f_layout)
        self.setMaximumHeight(50)

    def change_folder(self):
        # Open file explorer
        chosen_folder = QFileDialog.getExistingDirectory(None, "Chose a folder")

        # Update text entry
        self.cur_folder = chosen_folder
        self._folder.setText(self.cur_folder)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('coesite.ico'))
    window = MainWindow()
    window.show()
    app.exec()
