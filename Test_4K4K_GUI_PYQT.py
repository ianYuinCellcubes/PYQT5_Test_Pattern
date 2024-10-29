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
    QHBoxLayout,
    QFrame
)

colorSelect = 7
menu_select = 0

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.w = monitor1
        self.initUI()

    def initUI(self):
        if menu_select == 0:
            self.setLayout(self.image_Show())
        self.move(self.w.xPos(1), self.w.yPos(1))
        self.showFullScreen()
    def image_Show(self):
        pixmap = self.image_pixmap()
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.setContentsMargins(0, 0, 0, 0)
        return vbox
    def image_pixmap(self):
        pix = recolorImage.recolorImage( self.w.width(1), self.w.height(1))
        return pix
class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w1 = AnotherWindow()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('4K4K Pattern Generator')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(200, 200, 800, 800)

        gboxlayout = QGridLayout()
        gboxlayout.addWidget(self.makeTopFrame(), 0, 0)
        gboxlayout.addWidget(self.makeBottomFrame(), 1, 0)
        gboxlayout.addWidget(self.makeMenuFrame(), 0, 1, 2, 1)

        widget = QWidget()
        widget.setLayout(gboxlayout)

        self.setCentralWidget(widget)
        self.show()

    def makeTopFrame(self):

        buttonL = QPushButton("  L  ", self)
        buttonR = QPushButton("  R  ", self)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(buttonL)
        hbox1.addStretch(1)
        hbox1.addWidget(buttonR)

        TF = QWidget()
        TF.setLayout(hbox1)
        return TF
    def makeBottomFrame(self):
        buttonL = QPushButton("  L  ", self)
        buttonR = QPushButton("  R  ", self)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(buttonL)
        hbox1.addStretch(1)
        hbox1.addWidget(buttonR)

        BF = QWidget()
        BF.setLayout(hbox1)
        return BF
    def makeMenuFrame(self):
        buttonG = QPushButton("Get Pattern", self)
        buttonR = QPushButton("  R  ", self)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(buttonG)
        vbox1.addWidget(buttonR)

        MF = QWidget()
        MF.setLayout(vbox1)
        return MF

    def closeEvent(self, QCloseEvent):
        self.w1.close()
        self.close()
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