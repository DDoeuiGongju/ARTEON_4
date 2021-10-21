from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

from base_value import background_w, background_h
import start_UI

import cv2
import numpy as np

from PIL import ImageQt

class BackWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.startImage = QImage('./image/background_image/video_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.palette = QPalette()
        self.palette.setBrush(10, QBrush(self.startImage))

        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h*0.168)))
        self.upperImage = QPixmap('./image/background_image/upper.png').scaled(QSize(background_w, int(background_h*0.168)))
        self.upperLabel.setPixmap(QPixmap(self.upperImage))

        self.anotherLabel = QLabel(self)
        self.anotherLabel.resize(QSize(int(background_w*0.1472), int(background_h*0.03645)))
        upperImage = QPixmap('./image/button_image/another2.png').scaled(
            QSize(int(background_w*0.1472), int(background_h*0.03645)))
        self.anotherLabel.setPixmap(QPixmap(upperImage))
        self.anotherLabel.move(int(background_w * 0.762), int(background_h * 0.17448))

        self.backLabel = QLabel(self)
        self.backLabel.resize(QSize(background_w, int(background_h*0.7354)))
        self.backLabel.move(0,int(background_h*0.0927))



        self._back_window = None

        self.mouse = False

        self.last_point = QPoint()

        self.setButton()

        self.setPalette(self.palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)
        self.show()

    def setButton(self):
        self.layer_xywh = QRect(0, int(background_h * 0.83),
                                background_w, int(background_h * 0.171))

        self.back_btnGroup = QButtonGroup()
        self.back_btnGroup.setExclusive(False)
        self.back_btnGroup.buttonClicked[int].connect(self.setBack)

        self.scrollarea = QScrollArea(self)
        self.scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.scrollarea.setGeometry(self.layer_xywh)
        self.scrollarea.setWidgetResizable(True)
        back_group, self.back_file_path = self.createLayout_group('./image/back_썸네일/', self.back_btnGroup)
        self.scrollarea.setWidget(back_group)
        self.scrollarea.setVisible(True)

        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back.png'))
        self.back.setIconSize(QSize(int(background_w * 0.0259), int(background_h * 0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w * 0.0259),
                              int(background_h * 0.026))
        self.back.clicked.connect(self.backPressEvent)

        self.sticker_btnGroup = QButtonGroup()
        self.sticker_btnGroup.setExclusive(False)
        self.sticker_btnGroup.buttonClicked[int].connect(self.setSticker)

        self.scrollarea1 = QScrollArea(self)
        self.scrollarea1.setStyleSheet('background-color: #FFFFFF;')
        self.scrollarea1.setGeometry(self.layer_xywh)
        self.scrollarea1.setWidgetResizable(True)
        sticker_group, self.sticker_file_path = self.createLayout_group('./image/sticker_image/', self.sticker_btnGroup)
        self.scrollarea1.setWidget(sticker_group)
        self.scrollarea1.setVisible(False)

        self.sticker = True
        sticker_x, sticker_y = int(background_w * 0.875), int(background_h * 0.4724)
        sticker_w, sticker_h = int(background_w * 0.0648), int(background_w * 0.0648)
        self.stickerButton = QPushButton(self)
        self.stickerButton.setIcon(QIcon('./image/button_image/addsticker.png'))
        self.stickerButton.setIconSize(QSize(sticker_w, sticker_h))
        self.stickerButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.stickerButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.stickerButton.clicked.connect(lambda: self.setScroll(self.sticker))

        save_x, save_y = int(background_w * 0.877), int(background_h * 0.77)
        save_w, save_h = int(background_w * 0.060), int(background_h * 0.0247)
        self.saveButton = QPushButton(self)
        self.saveButton.setIcon(QIcon('./image/button_image/save.png'))
        self.saveButton.setIconSize(QSize(save_w, save_h))
        self.saveButton.clicked.connect(self.saveResult)
        self.saveButton.setGeometry(save_x, save_y, save_w, save_h)
        self.saveButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")


    def setSticker(self, num):
        self.mouse = True
        self.stickerImage = QPixmap('./image/sticker_image/'+self.sticker_file_path[num]).scaled(
            QSize(int(background_w * 0.2), int(background_h * 0.137)))

    def setScroll(self, set):
        print(1)
        if set:
            print(2)
            self.scrollarea.setVisible(False)
            self.scrollarea1.setVisible(True)
            self.sticker = False
        else:
            print(3)
            self.scrollarea.setVisible(True)
            self.scrollarea1.setVisible(False)
            self.sticker = True
            self.mouse = False

    def createLayout_group(self, str, btnGroup):
        sgroupbox = QGroupBox(self)
        view_w, view_h = int(background_w * 0.225), int(background_h * 0.1542)

        layout_groupbox = QHBoxLayout(sgroupbox)
        layout_groupbox.setContentsMargins(0, 0, 0, 0)
        sgroupbox.setContentsMargins(0, 0, 0, 0)

        file_path = []

        file_list = os.listdir(str)
        for i in range(len(file_list)):
            file_path.append(file_list[i])
            button = (QPushButton(self))
            button.setIcon(QIcon(str + file_list[i]))
            button.setIconSize(QSize(view_w, view_h))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
            btnGroup.addButton(button, i)
            layout_groupbox.addWidget(button)
        return sgroupbox, file_path

    def setBack(self, num):
        self.back_pixmap = QPixmap('./image/back_big/'+self.back_file_path[num]).scaled(
            QSize(background_w,int(background_h*0.7354)))
        self.backLabel.setPixmap(QPixmap(self.back_pixmap))
        self.upperLabel.raise_()
        self.anotherLabel.raise_()

    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = start_UI.MakeWindow()
        self.close()
        self._back_window.show()

    def mousePressEvent(self, e):  ###### 스티커 위치
        if self.mouse:
            sticker = QPainter(self.back_pixmap)
            sticker.drawPixmap(e.x()*0.9, e.y()*0.9, QPixmap(self.stickerImage))
            sticker.end()
            self.backLabel.setPixmap(self.back_pixmap)

    def saveResult(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        image = self.backLabel.pixmap().toImage()
        if fpath:
            image.save(fpath)
            QMessageBox.about(
                self, 'Message', 'Background has been saved :)'
            )
