import os.path
import sys
import ScreenReader
import recolorImage
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPen, QPainter, QFontDatabase
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QToolTip,
    QMainWindow,
    qApp,
    QAction,
    QLabel,
    QVBoxLayout,
    QTabWidget,
    QGridLayout,
    QLayout,
    QHBoxLayout
)

colorSelect = 7
menu_select = 0

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.w = monitor1
        self.initUI()

    def initUI(self):
        r = int(colorSelect / 4)
        g = int(colorSelect / 2) - 2 * r
        b = colorSelect - 4 * r - 2 * g
        if menu_select == 0:
            self.setLayout(self.image_Show())

        self.move(self.w.xPos(1), self.w.yPos(1))
        self.showFullScreen()
    def image_Show(self):
        r = int(colorSelect / 4)
        g = int(colorSelect / 2) - 2 * r
        b = colorSelect - 4 * r - 2 * g
        pixmap = self.image_pixmap(r, g, b)
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.setContentsMargins(0, 0, 0, 0)
        return vbox
    def image_pixmap(self, r, g, b):
        pix = recolorImage.recolorImage(r, g, b, self.w.width(1), self.w.height(1))
        return pix
class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w1 = AnotherWindow()
        self.initUI()
    def show_new_window(self, checked):
       self.w1.show()

    def hide_new_window(self, checked):
        self.w1.hide()
    def create_tabs_Image(self):
        button1 = QPushButton(' RED  ', self)
        button1.move(50, 50)
        button1.resize(100,10)
        button1.clicked.connect(self.w1.image_Show)
        button1.setStyleSheet("padding: 15px; background-color: red; color: white;")
        # button1.setFont(QFont("Helvetica", 15))

        button2 = QPushButton(' BLUE  ', self)
        button2.move(80, 50)
        button2.resize(100, 10)
        button2.clicked.connect(self.w1.image_Show)
        button2.setStyleSheet("padding: 15px; background-color: blue; color: white;")


        button3 = QPushButton(' GREEN  ', self)
        button3.move(100, 50)
        button3.resize(100, 10)
        button3.clicked.connect(self.w1.image_Show)
        button3.setStyleSheet("padding: 15px; background-color: green; color: white;")

        # btn = QPushButton('quit', self)
        # btn.move(50, 50)
        # btn.resize(btn.sizeHint())
        # btn.clicked.connect(QCoreApplication.instance().quit)
        hbox = QHBoxLayout()
        hbox.addWidget(button1)
        hbox.addWidget(button2)
        hbox.addWidget(button3)
        # tab = QWidget()
        # tab.setLayout(hbox)
        return hbox
    def initUI(self):
        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(200, 200, 500, 400)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_tabs_Image(), "  Image  " )
        self.tabs.addTab(self.tab2, " Line  ")

        self.label01 = QLabel('-----Test View------')
        self.label01.resize(50,50)
        self.label02 = QLabel("testt")
        self.label02.resize(50,50)
        vbox1 = QGridLayout()
        vbox1.addWidget(self.label01, 0, 0)
        vbox1.addWidget(self.label02, 1, 0)
        # self.hbox1 = QHBoxLayout()
        # self.hbox1.addWidget(self.tabs)
        # self.tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 50px; background: 'red'}")
        # self.setCentralWidget(vbox1)
        vbox1.addWidget(self.tabs, 0, 1)
        # self.setLayout(self.vbox1)
        vbox1.setGeometry(200,200,500,400)
        self.setLayout(vbox1)

        # self.show()

def ExceptionHook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)

if __name__ == '__main__':
    sys.excepthook = ExceptionHook
    monitor1 = ScreenReader.monitor
    monitor1.scanning(monitor1)


    font = QFont("SF Pro Compressed Medium", 16)
    font1 = QFont("Times New Roman")
    app = QApplication(sys.argv)
    app.setFont(font)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())