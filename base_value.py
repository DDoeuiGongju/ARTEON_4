from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

app = QtWidgets.QApplication(sys.argv)

desktop_w = QApplication.desktop().screenGeometry().width()
desktop_h = QApplication.desktop().screenGeometry().height()

image = QImage('./image/background_image/start_image.png')

set_ratio = (desktop_h / image.height()) - 0.05
background_w = int(image.width() * set_ratio)
background_h = int(image.height() * set_ratio)

to_email = None

style1 = '''QSlider::groove:horizontal {
                    border-radius: 3px;
                    height: %d;
                    background-color: #EEDBB6;
                }
                QSlider::handle:horizontal {
                    background-color: rgb(255,255,255);
                    height: %d;
                    width: %d;
                    border-radius: 3px;
                    margin:3px
                }''' % (int(background_w * 0.0324), int(background_w * 0.03), int(background_w * 0.03))
style2 = '''QSlider::groove:vertical {
                    border-radius: 3px;
                    height: %d;
                    background-color: #EEDBB6;
                }
                QSlider::handle:vertical {
                    background-color: rgb(255,255,255);
                    height: %d;
                    width: %d;
                    border-radius: 3px;
                    margin:3px
                }''' % (int(background_h * 0.2625), int(background_w * 0.03), int(background_w * 0.03))
