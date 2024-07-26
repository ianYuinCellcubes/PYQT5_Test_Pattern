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
if __name__ == '__main__':
    monitor1 = ScreenReader.monitor
    monitor1.scanning(monitor1)

    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./resource/SF-Pro.ttf')
    app = QApplication(sys.argv)
    app.setFont(QFont('SF-Pro'))
    sys.exit(app.exec_())