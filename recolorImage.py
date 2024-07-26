from PyQt5 import QtGui
from PIL import Image  # pip install pillow
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import *

import pathlib

def recolorImage(rF, gF, bF, canvasWidth, canvasHeight):
    cPath = pathlib.Path(__file__).parent.resolve()  # current script directory
    file = str(cPath) + "\\resource\\TestImage1.jpg"  # 5040 x 3600
    im = Image.open(file).convert('RGB')
    # pixmap = QPixmap("./resource/TestImage1.jpg").scaled(canvasWidth, canvasHeight, 0, 0)
    r1, g1, b1 = im.split()
    # color strength 0 - 1
    r1 = r1.point(lambda i: i * rF)
    g1 = g1.point(lambda i: i * gF)
    b1 = b1.point(lambda i: i * bF)
    im2 = Image.merge('RGB', (r1, g1, b1))
    img = im2.resize((canvasWidth, canvasHeight))
    data = img.tobytes("raw", "RGB")
    print(str(img.size[0]) + "      " + str(img.size[1]))
    qim = QtGui.QImage(data, img.size[0], img.size[1], QtGui.QImage.Format_RGB888)
    pix = QtGui.QPixmap.fromImage(qim)
    return pix