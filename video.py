from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

from base_value import background_w, background_h, style1, style2
import start_UI

import cv2
import numpy as np

import time

import mediapipe as mp

import email_send

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 배경 이미지
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        self.startImage = QPixmap('./image/background_image/video_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.mainLabel.setPixmap(self.startImage)
        # self.palette = QPalette()
        # self.palette.setBrush(10, QBrush(self.startImage))

        # 상단 이미지
        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h * 0.168)))
        upperImage = QPixmap('./image/background_image/upper.png').scaled(
            QSize(background_w, int(background_h * 0.168)))
        self.upperLabel.setPixmap(QPixmap(upperImage))

        # 따로 기능이 없는 이미지
        self.anotherLabel = QLabel(self)
        self.anotherLabel.resize(QSize(int(background_w * 0.1472), int(background_h * 0.03645)))
        upperImage = QPixmap('./image/button_image/another.png').scaled(
            QSize(int(background_w * 0.1472), int(background_h * 0.03645)))
        self.anotherLabel.setPixmap(QPixmap(upperImage))
        self.anotherLabel.move(int(background_w * 0.762), int(background_h * 0.17448))

        self.anotherLabel1 = QLabel(self)
        self.anotherLabel1.resize(QSize(int(background_w * 0.28055), int(background_h * 0.03385)))
        upperImage = QPixmap('./image/button_image/another3.png').scaled(
            QSize(int(background_w * 0.28055), int(background_h * 0.03385)))
        self.anotherLabel1.setPixmap(QPixmap(upperImage))
        self.anotherLabel1.move(int(background_w * 0.36019), int(background_h * 0.7671875))

        self.anotherLabel2 = QLabel(self)
        self.anotherLabel2.resize(QSize(int(background_w * 0.06481), int(background_w * 0.06481)))
        upperImage = QPixmap('./image/button_image/another4.png').scaled(
            QSize(int(background_w * 0.06481), int(background_w * 0.06481)))
        self.anotherLabel2.setPixmap(QPixmap(upperImage))
        self.anotherLabel2.move(int(background_w * 0.84444), int(background_h * 0.17447))
        self.anotherLabel2.setVisible(False)

        self.image_x = 0
        self.image_y = int(background_h * 0.0927)
        self.image_w = background_w
        self.image_h = int(background_h * 0.7354)

        # 영상이 들어갈 공간
        self.label = QLabel(self)
        self.label.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)

        # 얼굴을 선택한 경우 얼굴 배경이 들어갈 공간
        self.faceLabel = QLabel(self)
        self.faceLabel.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)
        self.face_file_path = []

        # 몸을 선택할 경우 몸 배경이 들어갈 공간
        self.bodyLabel = QLabel(self)
        self.bodyLabel.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)
        self.body_file_path = []

        self.textLabel = QLabel(self)
        # self.textLabel.setAlignment(Qt.AlignCenter)
        # self.font_ = self.textLabel.font()
        # self.font_.setPointSize(50)
        self.textLabel.setGeometry(int(background_w*0.4083), int(background_h*0.39375),
                                   (background_w*18333), int(background_h*0.13386))


        self.video_thread = VideoThread()

        self.programRun = False # 얼굴이나 몸을 선택한 상태인지
        self.mouse = False      # 스티커 마우스 이벤트를 위한 시그넝
        self.body_back = False  # 바디에서 배경에 스티커를 붙이는 단계인지 확인

        self.sticker_ex = QLabel(self)              # 임시 스티커 공간
        self.sticker_size = int(background_w * 0.2) # 초기 스티커 사이즈
        self.stickerImage = None                    # 선택된 스티커 이미지
        self.stickerImage_path = []                 # 선택된 스티커 이미지 경로

        self.last_point = QPoint()

        # 실행취소/다시실행 buffer
        self.undo = []
        self.redo = []

        self.before_num = None

        self.setScrollButton()
        self.setButton()

        # self.setPalette(self.palette)
        # self.setWindowTitle('이리오너라')
        # self.setGeometry(0, 0, background_w, background_h)
        # self.show()

    def setScrollButton(self):
        self.layer_xywh = QRect(0, int(background_h * 0.8286), background_w, int(background_h * 0.1718))

        self.face_btnGroup = QButtonGroup()
        self.face_btnGroup.setExclusive(False)
        self.face_btnGroup.buttonClicked[int].connect(self.setFace)

        self.face_scrollarea = QScrollArea(self)
        self.face_scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.face_scrollarea.setGeometry(self.layer_xywh)
        self.face_scrollarea.setWidgetResizable(True)
        face_group, self.face_file_path = self.createLayout_group('./image/face/썸네일/', self.face_btnGroup)
        self.face_scrollarea.setWidget(face_group)
        self.face_scrollarea.setVisible(False)

        self.body_btnGroup = QButtonGroup()
        self.body_btnGroup.setExclusive(False)
        self.body_btnGroup.buttonClicked[int].connect(self.setBody)

        self.body_scrollarea = QScrollArea(self)
        self.body_scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.body_scrollarea.setGeometry(self.layer_xywh)
        self.body_scrollarea.setWidgetResizable(True)
        body_group, self.body_file_path = self.createLayout_group('./image/background/썸네일/', self.body_btnGroup)
        self.body_scrollarea.setWidget(body_group)
        self.body_scrollarea.setVisible(False)

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

    def setButton(self):
        undo_x, undo_y = int(background_w * 0.07222), int(background_h * 0.7745)
        undo_w, undo_h = int(background_w * 0.05556), int(background_h * 0.02059)
        self.undoButton = QPushButton(self)
        self.undoButton.setIcon(QIcon('./image/button_image/before.png'))
        self.undoButton.setIconSize(QSize(undo_w, undo_h))
        self.undoButton.clicked.connect(lambda: self.undoredoEvent('undo'))
        self.undoButton.setGeometry(undo_x, undo_y, undo_w, undo_h)
        self.undoButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.undoButton.hide()

        redo_x, redo_y = int(background_w * 0.2213), int(background_h * 0.7745)
        redo_w, redo_h = int(background_w * 0.05556), int(background_h * 0.02059)
        self.redoButton = QPushButton(self)
        self.redoButton.setIcon(QIcon('./image/button_image/after.png'))
        self.redoButton.setIconSize(QSize(undo_w, undo_h))
        self.redoButton.clicked.connect(lambda: self.undoredoEvent('redo'))
        self.redoButton.setGeometry(redo_x, redo_y, redo_w, redo_h)
        self.redoButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.redoButton.hide()

        self._back_window = None
        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back.png'))
        self.back.setIconSize(QSize(int(background_w * 0.0259), int(background_h * 0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w * 0.0259),
                              int(background_h * 0.026))
        self.back.clicked.connect(self.backPressEvent)

        save_x, save_y = int(background_w * 0.877), int(background_h * 0.77)
        save_w, save_h = int(background_w * 0.060), int(background_h * 0.0247)
        self.saveButton = QPushButton(self)
        self.saveButton.setIcon(QIcon('./image/button_image/save.png'))
        self.saveButton.setIconSize(QSize(save_w, save_h))
        self.saveButton.clicked.connect(self.saveResult)
        self.saveButton.setGeometry(save_x, save_y, save_w, save_h)
        self.saveButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.saveButton.hide()

        run_x, run_y = int(background_w * 0.4555), int(background_h * 0.7578)
        run_w, run_h = int(background_w * 0.0926), int(background_w * 0.0926)

        self.now_run = True
        self.runButton = QPushButton(self)
        self.runButton.setIcon(QIcon('./image/button_image/capture.png'))
        self.runButton.setIconSize(QSize(run_w, run_h))
        self.runButton.clicked.connect(self.setRun)
        self.runButton.setGeometry(run_x, run_y, run_w, run_h)
        self.runButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        face_x, face_y = int(background_w * 0.51666), int(background_h * 0.8552)
        face_w, face_h = int(background_w * 0.1389), int(background_h * 0.11875)
        self.faceButton = QPushButton(self)
        self.faceButton.setIcon(QIcon('./image/button_image/face.png'))
        self.faceButton.setIconSize(QSize(face_w, face_h))
        self.faceButton.clicked.connect(lambda: self.facebodyEvent('face'))
        self.faceButton.setGeometry(face_x, face_y, face_w, face_h)
        self.faceButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        body_x, body_y = int(background_w * 0.3444), int(background_h * 0.8552)
        self.bodyButton = QPushButton(self)
        self.bodyButton.setIcon(QIcon('./image/button_image/body.png'))
        self.bodyButton.setIconSize(QSize(face_w, face_h))
        self.bodyButton.clicked.connect(lambda: self.facebodyEvent('body'))
        self.bodyButton.setGeometry(body_x, body_y, face_w, face_h)
        self.bodyButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        # 공유 버튼
        share_x, share_y = int(background_w * 0.762), int(background_h * 0.17552)
        share_w, share_h = int(background_w * 0.05146), int(background_h * 0.0328)
        self.shareButton = QPushButton(self)
        self.shareButton.setIcon(QIcon('./image/button_image/share.png'))
        self.shareButton.setIconSize(QSize(share_w, share_h))
        self.shareButton.clicked.connect(self.sharePressEvent)
        self.shareButton.setGeometry(share_x, share_y, share_w, share_h)
        self.shareButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.shareButton.setVisible(False)

        self.sticker = True

        self.stickerSlider = QSlider(Qt.Vertical, self)
        self.stickerSlider.setGeometry(int(background_w * 0.037), int(background_h * 0.3458),
                                       int(background_w * 0.0324), int(background_h * 0.2625))
        self.stickerSlider.setRange(int((background_w * 0.2) / 2), int((background_w * 0.2) * 2))
        self.stickerSlider.valueChanged[int].connect(self.changeSticker_size)
        self.stickerSlider.setStyleSheet(style2)
        self.stickerSlider.setVisible(False)

        sticker_x, sticker_y = int(background_w * 0.875), int(background_h * 0.4724)
        sticker_w, sticker_h = int(background_w * 0.0648), int(background_w * 0.0648)
        self.stickerButton = QPushButton(self)
        self.stickerButton.setIcon(QIcon('./image/button_image/addsticker.png'))
        self.stickerButton.setIconSize(QSize(sticker_w, sticker_h))
        self.stickerButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.stickerButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.stickerButton.clicked.connect(lambda: self.setStickerScroll(self.sticker))
        self.stickerButton.hide()

        self.popup = QPushButton(self)
        self.popup.setIcon(QIcon('./image/background_image/popup.png'))
        self.popup.setIconSize(QSize(int(background_w * 0.5713), int(background_h * 0.05886)))
        self.popup.setGeometry(int(background_w * 0.23055), int(background_h * 0.44114), int(background_w * 0.5713),
                               int(background_h * 0.05886))
        self.popup.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.popup.clicked.connect(self.popupEvent)
        self.popup.setVisible(False)

    # 뒤로가기
    def backPressEvent(self):
        self.video_thread.seg = False
        self.video_thread.stop()
        if not self.programRun:
            if self._back_window is None:
                self._back_window = start_UI.MakeWindow()
            # self._back_window.show()
            self.setCentralWidget(self._back_window)
            # self.close()
        else:
            self.saveButton.hide()
            self.sticker_scrollarea.setVisible(False)
            self.face_scrollarea.setVisible(False)
            self.body_scrollarea.setVisible(False)
            # upperImage = QPixmap('./image/button_image/another.png').scaled(
            #     QSize(int(background_w * 0.1472), int(background_h * 0.03645)))
            # self.anotherLabel.setPixmap(QPixmap(upperImage))
            self.anotherLabel.setVisible(True)
            self.anotherLabel2.setVisible(False)
            self.shareButton.setVisible(False)
            self.stickerButton.hide()
            self.undoButton.hide()
            self.redoButton.hide()
            self.bodyButton.show()
            self.faceButton.show()

            self.programRun = False
            self.sticker_ex.clear()
            self.sticker_scrollarea.setVisible(False)
            self.stickerSlider.setVisible(False)
            self.sticker = True
            self.mouse = False
            self.before_num = None
            self.now_run = True

            self.label.clear()
            self.bodyLabel.clear()
            self.faceLabel.clear()
            self.textLabel.setVisible(False)

            self.label.hide()

            face_group, self.face_file_path = self.createLayout_group('./image/face/썸네일/', self.face_btnGroup)
            self.face_scrollarea.setWidget(face_group)
            body_group, self.body_file_path = self.createLayout_group('./image/background/썸네일/', self.body_btnGroup)
            self.body_scrollarea.setWidget(body_group)

    # 사진찍기
    def setRun(self):
        print(self.now_run)
        if self.now_run:
            self.video_thread.time_check = True
            self.now_run = False
        else:
            self.video_thread.capture = True
            self.video_thread.start()
            self.now_run = True

    def saveResult(self):
        if self.video_thread.seg:
            if self.body_back:
                fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', './',
                                                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
                saveimg = self.bodyLabel.pixmap().toImage()
            else:
                fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', './image/sticker_image',
                                                       "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
                saveimg = self.label.pixmap().toImage()
        else:
            fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', './',
                                                   "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            saveimg = self.label.pixmap().toImage()
            saveimg2 = self.faceLabel.pixmap().toImage()

            p = QPainter(saveimg)
            p.drawImage(saveimg.rect(), saveimg2)
            p.end()

        if fpath:
            saveimg.save(fpath)
            self.popup.setIcon(QIcon('./image/background_image/popup.png'))
            self.popup.setVisible(True)
            # QMessageBox.about(
            #     self, 'Message', '이미지가 저장되었습니다!'
            # )
        sticker_group, self.sticker_file_path = self.createLayout_group('./image/sticker_image/',
                                                                        self.sticker_btnGroup)
        self.sticker_scrollarea.setWidget(sticker_group)

    def sharePressEvent(self):
        fpath = 'temporary_v.png'
        if self.video_thread.seg: # 신체
            if self.body_back:    # 스티커붙인 배경 저장
                saveimg = self.bodyLabel.pixmap().toImage()
            else:                 # 신체로 만든 스티커
                saveimg = self.label.pixmap().toImage()
        else:
            saveimg = self.label.pixmap().toImage()
            saveimg2 = self.faceLabel.pixmap().toImage()

            p = QPainter(saveimg)
            p.drawImage(saveimg.rect(), saveimg2)
            p.end()
        # 이메일 주소 부르기
        with open('./email.txt', 'r') as f:
            to_email = f.readline()
            f.close()
        if fpath:
            saveimg.save(fpath)
            # 이메일로 이미지 전송 thread
            self.th = email_send.emailTread(to_email, fpath)
            self.th.start()

            self.popup.setIcon(QIcon('./image/background_image/popup.png'))
            self.popup.setVisible(True)
            # QMessageBox().about(
            #     self, 'Message', '이미지가 공유되었습니다!'
            # )

    def setSticker(self, num):
        self.mouse = True
        self.stickerImage_path = './image/sticker_image/' + self.sticker_file_path[num]

    def changeSticker_size(self, size):
        self.sticker_size = size

    def setStickerScroll(self, set):
        if self.bodyLabel.pixmap() or self.faceLabel.pixmap() :
            if set:
                self.sticker_scrollarea.setVisible(True)
                self.stickerSlider.setVisible(True)
                self.sticker = False
                self.mouse = True
            else:
                self.sticker_ex.clear()
                self.sticker_scrollarea.setVisible(False)
                self.stickerSlider.setVisible(False)
                self.sticker_ex.clear()
                self.sticker = True
                self.mouse = False

    @pyqtSlot(np.ndarray)
    def setImage(self, frame):
        if self.video_thread.time_check:
            self.textLabel.setVisible(True)
            self.textLabel.setText('%d'%self.video_thread.set_time)
            self.textLabel.setFont(QFont("Arial",int(background_h*0.1337)))
            self.textLabel.setStyleSheet('color: red')
            # self.textLabel.setAlignment(Qt.AlignCenter)
            # self.textLabel.set
        else:
            self.textLabel.setVisible(False)
        h, w, ch = frame.shape
        show_img = frame
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(show_img.data,
                                      w, h, bytes_per_line,
                                      QImage.Format_BGR888 if ch == 3 else QImage.Format_BGRA8888)
        pixmap = QPixmap.fromImage(convert_to_qt_format)
        self.label.setPixmap(pixmap)
        self.label.lower()
        self.mainLabel.lower()

    def facebodyEvent(self, str):
        self.video_thread.start()
        # upperImage = QPixmap('./image/button_image/another2.png').scaled(
        #     QSize(int(background_w * 0.1472), int(background_h * 0.03645)))
        # self.anotherLabel.setPixmap(QPixmap(upperImage))
        self.anotherLabel.setVisible(False)
        self.anotherLabel2.setVisible(True)
        self.shareButton.setVisible(True)
        self.bodyButton.hide()
        self.faceButton.hide()
        self.programRun = True

        self.stickerButton.show()
        self.saveButton.show()
        self.undoButton.show()
        self.redoButton.show()
        if str == 'face':
            self.video_thread.seg = False
            self.video_thread.changePixmap.connect(self.setImage)
            self.face_scrollarea.setVisible(True)
        elif str == 'body':
            self.video_thread.seg = True
            self.video_thread.changeSeg.connect(self.setBodySeg)
            self.body_scrollarea.setVisible(True)
        self.label.show()

    def setFace(self, num):
        self.now_run = True
        facePixmap = QPixmap('./image/face/큰창/'+self.face_file_path[num]).scaled(
            QSize(background_w,int(background_h*0.7354)))

        if os.path.isfile('./image/face/설명/'+self.face_file_path[num]):
            if self.before_num == None:
                self.face_btnGroup.button(num).setIcon(QIcon('./image/face/설명/' + self.face_file_path[num]))
            elif self.before_num != num:
                self.face_btnGroup.button(self.before_num).setIcon(QIcon('./image/face/썸네일/' + self.face_file_path[self.before_num]))
                self.face_btnGroup.button(num).setIcon(QIcon('./image/face/설명/'+self.face_file_path[num]))
        self.before_num = num

        self.faceLabel.setPixmap(QPixmap(facePixmap))
        # self.upperLabel.raise_()
        self.mainLabel.lower()
        self.upperLabel.raise_()
        self.anotherLabel2.raise_()
        self.anotherLabel1.raise_()
        self.runButton.raise_()


    @pyqtSlot(np.ndarray)
    def setBodySeg(self, output_image):
        if self.video_thread.time_check:
            self.textLabel.setVisible(True)
            self.textLabel.setText('%d'%self.video_thread.set_time)
            self.textLabel.setFont(QFont("Arial",int(background_h*0.1337)))
            self.textLabel.setStyleSheet('color: red')

        else:
            self.textLabel.setVisible(False)
        h, w, ch = output_image.shape
        show_img = output_image
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(show_img.data,
                                      w, h, bytes_per_line,
                                      QImage.Format_BGR888 if ch == 3 else QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(convert_to_qt_format)
        self.label.setPixmap(pixmap)
        self.label.lower()
        self.mainLabel.lower()


    def setBody(self, num):
        self.video_thread.capture = False
        self.body_back = True

        bodyPixmap = QPixmap('./image/background/큰창/%s'%self.body_file_path[num]).scaled(
            QSize(background_w, int(background_h * 0.7354)))

        if os.path.isfile('./image/background/설명/'+self.body_file_path[num]):
            if self.before_num == None:
                self.body_btnGroup.button(num).setIcon(QIcon('./image/background/설명/' + self.body_file_path[num]))
            elif self.before_num != num:
                self.body_btnGroup.button(self.before_num).setIcon(QIcon('./image/background/썸네일/' + self.body_file_path[self.before_num]))
                self.body_btnGroup.button(num).setIcon(QIcon('./image/background/설명/'+self.body_file_path[num]))
        self.before_num = num

        self.bodyLabel.setPixmap(QPixmap(bodyPixmap))
        self.mainLabel.lower()
        self.upperLabel.raise_()
        self.anotherLabel2.raise_()
        self.anotherLabel1.raise_()
        self.label.hide()

    def popupEvent(self):
        self.popup.setVisible(False)


    def createLayout_group(self, str, btnGroup): ##### 크기 조정
        sgroupbox = QGroupBox(self)
        view_w, view_h = int(background_w * 0.22), int(background_h * 0.15)

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

    def undoredoEvent(self, str):
        if not self.video_thread.seg:
            now = self.faceLabel.pixmap().toImage()
            if str == 'undo' and self.undo:
                self.redo.append(now)
                pix = QPixmap.fromImage(self.undo[-1])
                self.faceLabel.setPixmap(QPixmap(pix))
                del self.undo[-1]
                if self.redo:
                    self.redoButton.setEnabled(True)
            elif str == 'redo' and self.redo:
                self.undo.append(now)
                pix = QPixmap.fromImage(self.redo[-1])
                self.faceLabel.setPixmap(QPixmap(pix))
                print(len(self.redo))
                del self.redo[-1]
                if not self.redo:
                    self.redoButton.setEnabled(False)
        else:
            now = self.bodyLabel.pixmap().toImage()
            if str == 'undo' and self.undo:
                self.redo.append(now)
                pix = QPixmap.fromImage(self.undo[-1])
                self.bodyLabel.setPixmap(QPixmap(pix))
                del self.undo[-1]
                if not self.undo:
                    self.undoButton.setEnabled(False)
                if self.redo:
                    self.redoButton.setEnabled(True)
            elif str == 'redo' and self.redo:
                self.undoButton.setEnabled(True)
                self.undo.append(now)
                pix = QPixmap.fromImage(self.redo[-1])
                self.bodyLabel.setPixmap(QPixmap(pix))
                print(len(self.redo))
                del self.redo[-1]
                if not self.redo:
                    self.redoButton.setEnabled(False)

    def mousePressEvent(self, e):
        if self.mouse:
            self.stickerImage = QPixmap(self.stickerImage_path).scaledToWidth(self.sticker_size)
            self.sticker_ex.resize(QSize(self.stickerImage.size()))
            self.sticker_ex.setPixmap(QPixmap(self.stickerImage))
            self.sticker_ex.move(e.x() - (self.stickerImage.width() / 2), e.y() - (self.stickerImage.height() / 2))

    def mouseDoubleClickEvent(self, e):
        if self.mouse:
            self.sticker_ex.clear()
            self.redo = []
            self.undoButton.setEnabled(True)
            self.redoButton.setEnabled(False)
            if not self.video_thread.seg:
                self.undo.append(self.faceLabel.pixmap().toImage())
                sticker = QPainter(self.faceLabel.pixmap())
                sticker.drawPixmap(e.x() - (self.stickerImage.width() / 2),
                                   e.y() - (self.stickerImage.height() / 2) - self.image_y,
                                   QPixmap(self.stickerImage))
            else:
                self.undo.append(self.bodyLabel.pixmap().toImage())
                sticker = QPainter(self.bodyLabel.pixmap())
                sticker.drawPixmap(e.x() - (self.stickerImage.width() / 2),
                                   e.y() - (self.stickerImage.height() / 2) - self.image_y,
                                   QPixmap(self.stickerImage))
            self.update()





class VideoThread(QThread):
    changePixmap = pyqtSignal(np.ndarray)
    changeSeg = pyqtSignal(np.ndarray)


    seg = False
    capture = False

    time_check = False

    start_time = None

    set_time = 5

    def run(self):
        self.capture = True

        bg_image = cv2.imread('./image/background_image/canvas.png', cv2.IMREAD_UNCHANGED)
        bg_image = cv2.cvtColor(bg_image, cv2.COLOR_BGRA2RGBA)
        # add_dim = np.zeros((background_h, background_w), dtype=np.uint8)

        mp_selfie_segmentation = mp.solutions.selfie_segmentation
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.capture:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            r = int(background_h * 0.7354)/frame.shape[0]
            dim = (int(frame.shape[1]*r), int(background_h * 0.7354))
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            frame = frame[:int(background_h * 0.7354),:background_w].copy()
            if self.seg:
                with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    image.flags.writeable = False
                    results = selfie_segmentation.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

                    condition = np.stack((results.segmentation_mask,) * 4, axis=-1) > 0.5

                    bg_image = cv2.resize(bg_image, (image.shape[1], image.shape[0]), interpolation = cv2.INTER_AREA)

                    output_image = np.where(condition, image, bg_image)
                    self.changeSeg.emit(output_image)
            else:
                self.changePixmap.emit(frame)

            if self.time_check:
                if self.start_time is None:
                    self.start_time = time.time()
                if ( 5- (time.time() - self.start_time) +1) <6:
                    self.set_time = 5- (time.time() - self.start_time) +1
                if time.time() - self.start_time >= 5:
                    self.time_check = False
                    self.start_time = None
                    self.capture = False
                    self.set_time = 5

    def stop(self):
        self.capture = False
        self.quit()