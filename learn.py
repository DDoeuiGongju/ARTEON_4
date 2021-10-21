from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from base_value import background_w, background_h
import start_UI
import os

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

        self.veiw = QLabel(self)
        self.veiw.resize(QSize(int(background_w * 0.749), int(background_h * 0.661)))
        self.veiw.move(int(background_w * 0.1259), int(background_h * 0.2354))

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

        self.btnGroup = QButtonGroup()
        self.btnGroup.setExclusive(False)
        self.btnGroup.buttonClicked[int].connect(self.buttonPressEvent)
        self.file_path = []

        self.createLayout_Container()


    def createLayout_group(self):
        sgroupbox = QGroupBox(self)
        layout_groupbox = QVBoxLayout(sgroupbox)
        layout_groupbox.setContentsMargins(0, 0, 0, 0)

        file_list = os.listdir('./image/learning_image/썸네일/')
        for i in range(len(file_list)):
            self.file_path.append(file_list[i])
            button = (QPushButton(self))
            button.setIcon(QIcon('./image/learning_image/썸네일/' + file_list[i]))
            button.setIconSize(QSize(self.image_w, self.image_h))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
            self.btnGroup.addButton(button, i)
            layout_groupbox.addWidget(button)
        return sgroupbox

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setGeometry(self.xywh)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.createLayout_group())

    def buttonPressEvent(self, num):
        print('./image/learning_image/설명/'+self.file_path[num])
        self.scrollarea.hide()
        self.view = QPushButton(self)
        self.view.setIcon(QIcon('./image/learning_image/설명/'+self.file_path[num]))
        self.view.setIconSize(QSize(int(background_w * 0.749), int(background_h * 0.661)))
        self.view.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.view.setGeometry(int(background_w * 0.1259), int(background_h * 0.2354),
                              int(background_w * 0.749), int(background_h * 0.661))
        self.view.show()
        self.view.clicked.connect(self.viewPressEvent)

        self.save = QPushButton(self)
        self.save.setIcon(QIcon('./image/button_image/save1.png'))
        self.save.setIconSize(QSize(int(background_w * 0.0648), int(background_w * 0.0648)))
        self.save.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.save.setGeometry(int(background_w * 0.7583), int(background_h * 0.177),
                              int(background_w * 0.0648), int(background_w * 0.0648))
        self.save.show()
        self.save.clicked.connect(lambda: self.savePressEvent('./image/learning_image/이미지/'+self.file_path[num]))

    def viewPressEvent(self):
        self.scrollarea.show()
        self.view.hide()
        self.save.hide()

    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = start_UI.FirstWindow()
        self.close()
        self._back_window.show()

    def savePressEvent(self, image_path):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")
        self.saveimg = QImage(image_path[:-3]+'jpg')
        if fpath:
            self.saveimg.save(fpath)
            QMessageBox.about(
                self, 'Message', 'Image has been saved :)'
            )
