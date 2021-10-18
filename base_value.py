from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

app = QtWidgets.QApplication(sys.argv)

desktop_w = QApplication.desktop().screenGeometry().width()
desktop_h = QApplication.desktop().screenGeometry().height()

image = QImage('./image/background_image/start_image.png')

set_ratio = (desktop_h / image.height()) - 0.1
background_w = int(image.width() * set_ratio)
background_h = int(image.height() * set_ratio)
