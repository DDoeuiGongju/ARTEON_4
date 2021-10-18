from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from base_value import background_w, background_h
import start_UI

class LearnWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.startImage = QImage('./image/background_image/sticker_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.startImage.fill(QColor('#FFFFFF'))
        self.palette = QPalette()
        self.palette.setBrush(10, QBrush(self.startImage))

        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h*0.2109)))
        upperImage = QPixmap('./image/background_image/upper2.png').scaled(QSize(background_w, int(background_h*0.2109)))
        self.upperLabel.setPixmap(QPixmap(upperImage))

        self._back_window = None
        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back.png'))
        self.back.setIconSize(QSize(int(background_w*0.0259),int(background_h*0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w*0.0259),int(background_h*0.026))
        self.back.clicked.connect(self.backPressEvent)

        self.selectImageButton()

        self.setPalette(self.palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)

        self._next_window = None

    def selectImageButton(self):
        self.image_w = int(background_w*0.749*0.9)
        self.image_h = int(background_h*0.214*0.9)
        self.xywh = QRect(int(background_w * 0.1259), int(background_h * 0.2354),
                     int(background_w*0.749), int(background_h * 0.661))


        self.createLayout_Container()
        # self.layout_All = QVBoxLayout(self)
        # self.layout_All.addWidget(self.scrollarea)

        self.image1.clicked.connect(lambda: self.buttonPressEvent(1))
        self.image2.clicked.connect(lambda: self.buttonPressEvent(2))
        self.image3.clicked.connect(lambda: self.buttonPressEvent(3))
        self.image4.clicked.connect(lambda: self.buttonPressEvent(4))


    def createLayout_group(self):
        sgroupbox = QGroupBox(self)

        layout_groupbox = QVBoxLayout(sgroupbox)
        layout_groupbox.setContentsMargins(0,0,0,0)

        self.image1 = QPushButton(self)
        self.image1.setIcon(QIcon('./image/learning_image/1.png'))
        self.image1.setIconSize(QSize(self.image_w, self.image_h))
        self.image1.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        layout_groupbox.addWidget(self.image1)

        self.image2 = QPushButton(self)
        self.image2.setIcon(QIcon('./image/learning_image/2.png'))
        self.image2.setIconSize(QSize(self.image_w, self.image_h))
        self.image2.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        layout_groupbox.addWidget(self.image2)

        self.image3 = QPushButton(self)
        self.image3.setIcon(QIcon('./image/learning_image/3.png'))
        self.image3.setIconSize(QSize(self.image_w, self.image_h))
        self.image3.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        layout_groupbox.addWidget(self.image3)

        self.image4 = QPushButton(self)
        self.image4.setIcon(QIcon('./image/learning_image/4.png'))
        self.image4.setIconSize(QSize(self.image_w, self.image_h))
        self.image4.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        layout_groupbox.addWidget(self.image4)

        return sgroupbox

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setGeometry(self.xywh)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.createLayout_group())

    def buttonPressEvent(self, select):
        self.hide()
        if self._next_window is None:
            if select == 1:
                self._next_window = NextWindow('./image/learning_image/1-1.png')
            elif select == 2:
                self._next_window= NextWindow('./image/learning_image/2-1.png')
            elif select == 3:
                self._next_window= NextWindow('./image/learning_image/3-1.png')
            elif select == 4:
                self._next_window= NextWindow('./image/learning_image/4-1.png')
        self._next_window.show()

    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = start_UI.FirstWindow()
        self.close()
        self._back_window.show()

class NextWindow(QWidget):
    def __init__(self, imagePath):
        super().__init__()
        self.background_w = background_w
        self.background_h = background_h

        self.startImage = QImage('./image/background_image/sticker_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.startImage.fill(QColor('#FFFFFF'))
        self.palette = QPalette()
        self.palette.setBrush(10, QBrush(self.startImage))

        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h * 0.2109)))
        upperImage = QPixmap('./image/background_image/upper2.png').scaled(
            QSize(background_w, int(background_h * 0.2109)))
        self.upperLabel.setPixmap(QPixmap(upperImage))

        self.veiw = QLabel(self)
        self.veiw.resize(QSize(int(background_w * 0.749), int(background_h * 0.661)))
        self.veiw.move(int(background_w * 0.1259), int(background_h * 0.2354))
        veiwImage = QPixmap(imagePath).scaled(
            QSize(int(background_w * 0.749), int(background_h * 0.661)))

        self.veiw.setPixmap(QPixmap(veiwImage))


        self.setPalette(self.palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)

        self._learn_window = LearnWindow()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.close()
            self._learn_window.show()