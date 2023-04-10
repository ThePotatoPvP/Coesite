import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget

class MaFenetre(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Coesite')
        self.setWindowIcon(QIcon('coesite.ico'))

        desktop = QDesktopWidget().screenGeometry()
        self.setGeometry(desktop.width()//4, desktop.height()//4, desktop.width()//2, desktop.height()//2)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('coesite.ico'))
    fenetre = MaFenetre()
    sys.exit(app.exec_())