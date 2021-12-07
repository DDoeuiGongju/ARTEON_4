from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

from base_value import background_w, background_h, style1, style2
import start_UI
import email_send

import cv2
import numpy as np
import time

from PIL import ImageQt

class BackWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        # 배경 이미지
        self.startImage = QPixmap('./image/background_image/video_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.mainLabel.setPixmap(self.startImage)

        # 상단 이미지
        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h*0.168)))
        self.upperImage = QPixmap('./image/background_image/upper.png').scaled(QSize(background_w, int(background_h*0.168)))
        self.upperLabel.setPixmap(QPixmap(self.upperImage))

        self.anotherLabel = QLabel(self)
        self.anotherLabel.resize(QSize(int(background_w*0.06481), int(background_w*0.06481)))
        upperImage = QPixmap('./image/button_image/another4.png').scaled(
            QSize(int(background_w*0.06481), int(background_w*0.06481)))
        self.anotherLabel.setPixmap(QPixmap(upperImage))
        self.anotherLabel.move(int(background_w * 0.84444), int(background_h * 0.17447))

        # 배경이미지가 들어갈 공간
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.resize(QSize(background_w, int(background_h * 0.7354)))
        self.backgroundLabel.move(0, int(background_h * 0.0927))


        # 실행취소/다시실행 buffer
        self.undo = []
        self.redo = []

        self._back_window = None

        self.mouse = False


        self.before_num = None

        self.sticker_ex = QLabel(self)  # 임시 스티커 공간
        self.sticker_size = int(background_w * 0.2)  # 초기 스티커 사이즈
        self.stickerImage = None  # 선택된 스티커 이미지
        self.stickerImage_path = []  # 선택된 스티커 이미지 경로

        self.last_point = QPoint()

        self.setButton()

        # self.setPalette(self.palette)
        # self.setWindowTitle('이리오너라')
        # self.setGeometry(0, 0, background_w, background_h)

    def setButton(self):
        undo_x, undo_y = int(background_w * 0.07222), int(background_h * 0.7745)
        undo_w, undo_h = int(background_w * 0.05556), int(background_h * 0.02059)
        self.undoButton = QPushButton(self)
        self.undoButton.setIcon(QIcon('./image/button_image/before.png'))
        self.undoButton.setIconSize(QSize(undo_w, undo_h))
        self.undoButton.clicked.connect(lambda: self.undoredoEvent('undo'))
        self.undoButton.setGeometry(undo_x, undo_y, undo_w, undo_h)
        self.undoButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        redo_x, redo_y = int(background_w * 0.2213), int(background_h * 0.7745)
        redo_w, redo_h = int(background_w * 0.05556), int(background_h * 0.02059)
        self.redoButton = QPushButton(self)
        self.redoButton.setIcon(QIcon('./image/button_image/after.png'))
        self.redoButton.setIconSize(QSize(undo_w, undo_h))
        self.redoButton.clicked.connect(lambda: self.undoredoEvent('redo'))
        self.redoButton.setGeometry(redo_x, redo_y, redo_w, redo_h)
        self.redoButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        self.layer_xywh = QRect(0, int(background_h * 0.83),
                                background_w, int(background_h * 0.171))
        # 배경 이미지 선택 버튼 그룹
        self.bg_btnGroup = QButtonGroup()
        self.bg_btnGroup.setExclusive(False)
        self.bg_btnGroup.buttonClicked[int].connect(self.setBackground)

        self.bg_scrollarea = QScrollArea(self)
        self.bg_scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.bg_scrollarea.setGeometry(self.layer_xywh)
        self.bg_scrollarea.setWidgetResizable(True)
        back_group, self.back_file_path = self.createLayout_group('./image/background/썸네일/', self.bg_btnGroup)
        self.bg_scrollarea.setWidget(back_group)
        self.bg_scrollarea.setVisible(True)

        # 뒤로가기 버튼
        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back.png'))
        self.back.setIconSize(QSize(int(background_w * 0.0259), int(background_h * 0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w * 0.0259),
                              int(background_h * 0.026))
        self.back.clicked.connect(self.backPressEvent)

        # 스티커 그룹
        self.sticker_btnGroup = QButtonGroup()
        self.sticker_btnGroup.setExclusive(False)
        self.sticker_btnGroup.buttonClicked[int].connect(self.setSticker)

        self.sticker_scrollarea = QScrollArea(self)
        self.sticker_scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.sticker_scrollarea.setGeometry(self.layer_xywh)
        self.sticker_scrollarea.setWidgetResizable(True)
        sticker_group, self.sticker_file_path = self.createLayout_group('./image/sticker_image/', self.sticker_btnGroup)
        self.sticker_scrollarea.setWidget(sticker_group)
        self.sticker_scrollarea.setVisible(False)

        # 스티커 스크롤 오픈 버튼
        self.sticker = True # 스티커 스크롤 오픈 버튼이 눌리면
        sticker_x, sticker_y = int(background_w * 0.875), int(background_h * 0.4724)
        sticker_w, sticker_h = int(background_w * 0.0648), int(background_w * 0.0648)
        self.stickerButton = QPushButton(self)
        self.stickerButton.setIcon(QIcon('./image/button_image/addsticker.png'))
        self.stickerButton.setIconSize(QSize(sticker_w, sticker_h))
        self.stickerButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.stickerButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.stickerButton.clicked.connect(lambda: self.setScroll(self.sticker))

        # 스티커 크기 조정 슬라이더
        self.stickerSlider = QSlider(Qt.Vertical, self)
        self.stickerSlider.setGeometry(int(background_w * 0.06), int(background_h * 0.3458),
                                       int(background_w * 0.0324), int(background_h * 0.3328))
        self.stickerSlider.setRange(int((background_w * 0.2) / 2), int((background_w * 0.2) * 4))
        self.stickerSlider.valueChanged[int].connect(self.changeSticker_size)
        self.stickerSlider.setStyleSheet(style2)
        self.stickerSlider.setVisible(False)

        # 저장 버튼
        save_x, save_y = int(background_w * 0.877), int(background_h * 0.77)
        save_w, save_h = int(background_w * 0.060), int(background_h * 0.0247)
        self.saveButton = QPushButton(self)
        self.saveButton.setIcon(QIcon('./image/button_image/save.png'))
        self.saveButton.setIconSize(QSize(save_w, save_h))
        self.saveButton.clicked.connect(self.saveResult)
        self.saveButton.setGeometry(save_x, save_y, save_w, save_h)
        self.saveButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        # 공유 버튼
        share_x, share_y = int(background_w * 0.762), int(background_h * 0.17552)
        share_w, share_h = int(background_w * 0.05146), int(background_h * 0.0328)
        self.shareButton = QPushButton(self)
        self.shareButton.setIcon(QIcon('./image/button_image/share.png'))
        self.shareButton.setIconSize(QSize(share_w, share_h))
        self.shareButton.clicked.connect(self.sharePressEvent)
        self.shareButton.setGeometry(share_x, share_y, share_w, share_h)
        self.shareButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        # 팝업 버튼
        self.popup = QPushButton(self)
        self.popup.setIcon(QIcon('./image/background_image/share_popup.png'))
        self.popup.setIconSize(QSize(int(background_w * 0.5713), int(background_h * 0.05886)))
        self.popup.setGeometry(int(background_w * 0.23055), int(background_h * 0.44114), int(background_w * 0.5713),
                               int(background_h * 0.05886))
        self.popup.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.popup.clicked.connect(self.popupEvent)
        self.popup.setVisible(False)


        self._home_window = None
        self.homeButton = QPushButton(self)
        self.homeButton.setIcon(QIcon('./image/button_image/home.png'))
        self.homeButton.setIconSize(QSize(int(background_w * 0.04629), int(background_h * 0.0282)))
        self.homeButton.clicked.connect(self.goHome)
        self.homeButton.setGeometry(int(background_w * 0.14722), int(background_h * 0.1776),
                                    int(background_w * 0.04629), int(background_h * 0.0282))
        self.homeButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

    # 처음으로
    def goHome(self):
        if self._home_window is None:
            self._home_window = start_UI.StartWindow()
        self.setCentralWidget(self._home_window)

    def changeSticker_size(self, size):
        self.sticker_size = size

    def setSticker(self, num):
        self.mouse = True
        self.stickerImage_path = './image/sticker_image/' + self.sticker_file_path[num]

    def setScroll(self, set):
        if set:
            self.bg_scrollarea.setVisible(False)
            self.sticker_scrollarea.setVisible(True)
            self.stickerSlider.setVisible(True)
            self.sticker = False
        else:
            self.bg_scrollarea.setVisible(True)
            self.sticker_scrollarea.setVisible(False)
            self.sticker = True
            self.stickerSlider.setVisible(False)
            self.sticker_ex.clear()
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



    def setBackground(self, num):
        self.undo, self.redo = [], []
        self.back_pixmap = QPixmap('./image/background/큰창/'+self.back_file_path[num]).scaled(
            QSize(background_w, int(background_h*0.7354)))

        if os.path.isfile('./image/background/설명/'+self.back_file_path[num]):
            if self.before_num == None:
                self.bg_btnGroup.button(num).setIcon(QIcon('./image/background/설명/' + self.back_file_path[num]))
            elif self.before_num != num:
                self.bg_btnGroup.button(self.before_num).setIcon(QIcon('./image/background/썸네일/' + self.back_file_path[self.before_num]))
                self.bg_btnGroup.button(num).setIcon(QIcon('./image/background/설명/'+self.back_file_path[num]))
        self.before_num = num

        self.bg_btnGroup.button(num).setIconSize(QSize(int(background_w * 0.225), int(background_h * 0.1542)))
        self.backgroundLabel.setPixmap(QPixmap(self.back_pixmap))
        self.mainLabel.lower()
        self.upperLabel.raise_()
        self.anotherLabel.raise_()


    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = start_UI.MakeWindow()
        self.setCentralWidget(self._back_window)

    def mousePressEvent(self, e):
        if self.mouse:
            self.stickerImage = QPixmap(self.stickerImage_path).scaledToWidth(self.sticker_size)
            self.sticker_ex.resize(QSize(self.stickerImage.size()))
            self.sticker_ex.setPixmap(QPixmap(self.stickerImage))
            self.sticker_ex.move(e.x() - (self.stickerImage.width() / 2), e.y() - (self.stickerImage.height() / 2))

    def mouseDoubleClickEvent(self, e):
        if self.mouse:
            self.undo.append(self.backgroundLabel.pixmap().toImage())
            self.redo = []
            self.undoButton.setEnabled(True)
            self.redoButton.setEnabled(False)
            self.sticker_ex.clear()
            sticker = QPainter(self.backgroundLabel.pixmap())
            sticker.drawPixmap(e.x()-(self.stickerImage.width()/2), e.y()-(self.stickerImage.height()/2)-int(background_h*0.0927), QPixmap(self.stickerImage))
            self.update()

    def undoredoEvent(self, str):
        now = self.backgroundLabel.pixmap().toImage()
        if str == 'undo' and self.undo:
            self.redo.append(now)
            pix = QPixmap.fromImage(self.undo[-1])
            self.backgroundLabel.setPixmap(QPixmap(pix))
            del self.undo[-1]
            if not self.undo:
                self.undoButton.setEnabled(False)
            if self.redo:
                self.redoButton.setEnabled(True)
        elif str == 'redo' and self.redo:
            self.undoButton.setEnabled(True)
            self.undo.append(now)
            pix = QPixmap.fromImage(self.redo[-1])
            self.backgroundLabel.setPixmap(QPixmap(pix))
            # print(len(self.redo))
            del self.redo[-1]
            if not self.redo:
                self.redoButton.setEnabled(False)

    def saveResult(self):
        fpath = None
        image = None
        if self.backgroundLabel:
            # fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', './image/sticker_image',
            #                                        "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            fpath = './image/sticker_image/%f.png' % np.random.rand(1)
            image = self.backgroundLabel.pixmap().toImage()
        if fpath:
            image.save(fpath)
            self.popup.setIcon(QIcon('./image/background_image/sticker_popup.png'))
            self.popup.setVisible(True)
            with open('./remove.txt', 'a') as f:
                f.write(fpath+'\n')

            sticker_group, self.sticker_file_path = self.createLayout_group('./image/sticker_image/',
                                                                            self.sticker_btnGroup)
            self.sticker_scrollarea.setWidget(sticker_group)

    def sharePressEvent(self):
        fpath = 'temporary_b.png'
        with open('./remove.txt', 'a') as f:
            f.write(fpath + '\n')
        with open('./email.txt', 'r') as f:
            to_email = f.readline()

        self.saveimg = QImage(self.backgroundLabel.pixmap().toImage())
        if fpath:
            self.saveimg.save(fpath)

            # 이메일로 이미지 전송 thread
            self.th = email_send.emailTread(to_email, fpath)
            self.th.start()

            self.popup.setIcon(QIcon('./image/background_image/share_popup.png'))
            self.popup.setVisible(True)
            # QMessageBox.about(
            #     self, 'Message', '이미지가 공유되었습니다!'
            # )

    def popupEvent(self):
        self.popup.setVisible(False)