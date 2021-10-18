from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from base_value import background_w, background_h
import sticker
import learn
import video

class StartWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.startImage = QImage('./image/background_image/start_image.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.startImage))

        self.setPalette(palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)

        self._first_window = FirstWindow()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.close()
            self._first_window.show()

class FirstWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.startImage = QImage('./image/background_image/background2.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.startImage))

        button_w = int(background_w * 0.23)
        button_y = int(background_h * 0.17)
        self.make_button = QPushButton(self)
        self.make_button.setIcon(QIcon('./image/button_image/making1.png'))
        self.make_button.setIconSize(QSize(button_w, button_y))
        self.make_button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.make_button.setGeometry(int(background_w * 0.23), int(background_h * 0.419), button_w, button_y)

        self.make_button.clicked.connect(lambda: self.buttonPressEvent('make'))

        button_w = int(background_w * 0.295)
        button_y = int(background_h * 0.173)
        self.lean_button = QPushButton(self)
        self.lean_button.setIcon(QIcon('./image/button_image/learning1.png'))
        self.lean_button.setIconSize(QSize(button_w, button_y))
        self.lean_button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.lean_button.setGeometry(int(background_w * 0.48), int(background_h * 0.417), button_w, button_y)

        self.lean_button.clicked.connect(lambda: self.buttonPressEvent('learn'))

        self.setPalette(palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)

        self._make_window = None
        self._learn_window = None

    def buttonPressEvent(self, button):
        self.close()
        if button == 'make':
            if self._make_window is None:
                self._make_window = MakeWindow()
            self._make_window.show()
        elif button == 'learn':
            if self._learn_window is None:
                self._learn_window = learn.LearnWindow()
            self._learn_window.show()

class MakeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.startImage = QImage('./image/background_image/background2.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        palette = QPalette()
        palette.setBrush(10, QBrush(self.startImage))


        button_w = int(background_w * 0.68)
        button_h = int(background_h * 0.17)
        button_x = int(background_w * 0.156)
        button_y = int(background_h * 0.27)

        self.select1 = QPushButton(self)
        self.select1.setIcon(QIcon('./image/button_image/select1.png'))
        self.select1.setIconSize(QSize(button_w, button_h))
        self.select1.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.select1.setGeometry(button_x, button_y, button_w, button_h)
        self.select1.clicked.connect(lambda: self.buttonPressEvent(1))

        button_y = int(background_h * 0.486)
        self.select2 = QPushButton(self)
        self.select2.setIcon(QIcon('./image/button_image/select2.png'))
        self.select2.setIconSize(QSize(button_w, button_h))
        self.select2.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.select2.setGeometry(button_x, button_y, button_w, button_h)
        self.select2.clicked.connect(lambda: self.buttonPressEvent(2))

        button_y = int(background_h * 0.696)
        self.select3 = QPushButton(self)
        self.select3.setIcon(QIcon('./image/button_image/select3.png'))
        self.select3.setIconSize(QSize(button_w, button_h))
        self.select3.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.select3.setGeometry(button_x, button_y, button_w, button_h)
        self.select3.clicked.connect(lambda: self.buttonPressEvent(3))


        self.setPalette(palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)

        self._sticker_window = None
        self._video_window = None

    def buttonPressEvent(self, select):
        if select == 1:
            if self._video_window is None:
                self._video_window = video.VideoWindow()
            self.close()
            self._video_window.show()
        elif select == 2:
            print(2)
        elif select == 3:
            if self._sticker_window is None:
                self._sticker_window = sticker.StickerWindow()
            self.close()
            self._sticker_window.show()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = StartWindow()
    window.show()
    sys.exit(app.exec_())