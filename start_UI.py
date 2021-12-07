from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os

from base_value import background_w, background_h
import sticker
import learn
import video
import background


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))
        self.startImage = QPixmap('./image/background_image/start_image.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.mainLabel.setPixmap(self.startImage)

        self.setFixedSize(background_w, background_h)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)

        self._email_window = emailWindow()

        timer = QTimer(self)
        timer.timeout.connect(self.timeEvent)
        timer.start(3000)

    def timeEvent(self):
        self.setCentralWidget(self._email_window)
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.setCentralWidget(self._email_window)
            # self._first_window.setVisible(True)

    def closeEvent(self, QCloseEvent):
        if os.path.isfile('./email.txt'):
            os.remove('./email.txt')
        if os.path.isfile('./remove.txt'):
            with open('./remove.txt', 'r') as file:
                for f in file:
                    if os.path.isfile(f.strip()):
                        os.remove(f.strip())
            os.remove('./remove.txt')

class emailWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        self.startImage = QPixmap('./image/background_image/background2.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.mainLabel.setPixmap(self.startImage)
        # palette = QPalette()
        # palette.setBrush(10, QBrush(self.startImage))

        self.emailEdit = QLineEdit(self)
        self.emailEdit.setPlaceholderText("이메일을 입력하시오!")
        rx = QRegularExpression("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b",QRegularExpression.CaseInsensitiveOption)
        self.emailEdit.setValidator(QRegularExpressionValidator(rx,self))
        self.emailEdit.textChanged.connect(self.setText)
        self.emailEdit.setFont(QFont('맑은고딕',int(background_h*0.015)))
        self.emailEdit.setStyleSheet('QLineEdit{border-radius: 10px;border-style: outset;font-weight:bold;}')
        self.emailEdit.setGeometry(int(background_w * 0.11666), int(background_h * 0.4734375),
                                   int(background_w * 0.76759), int(background_h * 0.05885))

        button_w = int(background_w * 0.2111)
        button_y = int(background_h * 0.0588)
        self.ok_button = QPushButton(self)
        self.ok_button.setIcon(QIcon('./image/button_image/ok.png'))
        self.ok_button.setIconSize(QSize(button_w, button_y))
        self.ok_button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.ok_button.setGeometry(int(background_w * 0.39444), int(background_h * 0.5692), button_w, button_y)

        self.ok_button.clicked.connect(self.okEvent)

        self._first_window = FirstWindow()

    def setText(self):
        if self.emailEdit.hasAcceptableInput():
            self.emailEdit.setStyleSheet("QLineEdit {border-radius: 10px;border-style: outset;color: black;font-weight:bold;}")
        else:
            self.emailEdit.setStyleSheet("QLineEdit {border-radius: 10px;border-style: outset;color: red;font-weight:bold;}")

    def okEvent(self):
        if self.emailEdit.hasAcceptableInput():
            with open('./email.txt', 'w') as f:
                f.write(self.emailEdit.text())
            self.setCentralWidget(self._first_window)
        self.mainLabel.setVisible(False)


class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        self.startImage = QPixmap('./image/background_image/background2.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.mainLabel.setPixmap(self.startImage)
        # palette = QPalette()
        # palette.setBrush(10, QBrush(self.startImage))

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

        # self.setPalette(palette)
        # self.setWindowTitle('이리오너라')
        # self.setGeometry(0, 0, background_w, background_h)

        self._make_window = None
        self._learn_window = None

    def buttonPressEvent(self, button):
        if button == 'make':
            if self._make_window is None:
                self._make_window = MakeWindow()
            self.setCentralWidget(self._make_window)
        elif button == 'learn':
            if self._learn_window is None:
                self._learn_window = learn.LearnWindow1()
            self.setCentralWidget(self._learn_window)
        self.mainLabel.setVisible(False)


class MakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        self.startImage = QPixmap('./image/background_image/background3.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.mainLabel.setPixmap(self.startImage)


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

        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back.png'))
        self.back.setIconSize(QSize(int(background_w * 0.0259), int(background_h * 0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w * 0.0259),
                              int(background_h * 0.026))
        self.back.clicked.connect(self.backPressEvent)

        self._sticker_window = None
        self._video_window = None
        self._background_window = None
        self._back_window = None

    def buttonPressEvent(self, select):
        if select == 1:
            if self._video_window is None:
                self._video_window = video.VideoWindow()
            self.setCentralWidget(self._video_window)
        elif select == 2:
            if self._background_window is None:
                self._background_window = background.BackWindow()
            self.setCentralWidget(self._background_window)
        elif select == 3:
            if self._sticker_window is None:
                self._sticker_window = sticker.StickerWindow()
            self.setCentralWidget(self._sticker_window)
        self.mainLabel.setVisible(False)

    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = FirstWindow()
        self.setCentralWidget(self._back_window)
        self.mainLabel.setVisible(False)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = StartWindow()
    window.show()
    sys.exit(app.exec_())