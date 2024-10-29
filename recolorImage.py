from PyQt5 import QtGui
from PIL import Image  # pip install pillow
# from PIL.ImageQt import ImageQt
from PyQt5.QtGui import *

import pathlib

def recolorImage( canvasWidth, canvasHeight):
    cPath = pathlib.Path(__file__).parent.resolve()  # current script directory
    file = str(cPath) + "\\resource\\TestImage1.jpg"  # 5040 x 3600
    im = Image.open(file).convert('RGB')
    # pixmap = QPixmap("./resource/TestImage1.jpg").scaled(canvasWidth, canvasHeight, 0, 0)
    img = im.resize((canvasWidth, canvasHeight))
    data = img.tobytes("raw", "RGB")
    print(str(img.size[0]) + "      " + str(img.size[1]))
    qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_RGB888)
    pix = QtGui.QPixmap.fromImage(qim)
    return pix