from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

from base_value import background_w, background_h
import start_UI

import cv2
import numpy as np

import mediapipe as mp

class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.startImage = QImage('./image/background_image/video_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.palette = QPalette()
        self.palette.setBrush(10, QBrush(self.startImage))

        self.image_x = 0
        self.image_y = int(background_h * 0.0927)
        self.image_w = background_w
        self.image_h = int(background_h * 0.7354)

        # self.image = QImage(QSize(self.image_w, self.image_h), QImage.Format_RGB32)
        self.label = QLabel(self)
        self.label.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)

        self.faceLabel = QLabel(self)
        self.faceLabel.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)

        self.bodyLabel = QLabel(self)
        self.bodyLabel.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)

        self.video_thread = VideoThread()
        self.video_thread.changePixmap.connect(self.setImage)

        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h*0.168)))
        upperImage = QPixmap('./image/background_image/upper.png').scaled(QSize(background_w, int(background_h*0.168)))
        self.upperLabel.setPixmap(QPixmap(upperImage))

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

        self.face_file_path = []
        self.body_file_path =[]
        self.body_back = []

        self.programRun = False
        self.mouse = False

        self.last_point = QPoint()

        self.setScrollButton()
        self.setButton()

        self.setPalette(self.palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)
        self.show()

    def setScrollButton(self):
        self.layer_xywh = QRect(0, int(background_h * 0.8286), background_w, int(background_h * 0.1718))

        self.face_btnGroup = QButtonGroup()
        self.face_btnGroup.setExclusive(False)
        self.face_btnGroup.buttonClicked[int].connect(self.setFace)

        self.face_scrollarea = QScrollArea(self)
        self.face_scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.face_scrollarea.setGeometry(self.layer_xywh)
        self.face_scrollarea.setWidgetResizable(True)
        face_group, self.face_file_path = self.createLayout_group('./image/face_썸네일/', self.face_btnGroup)
        self.face_scrollarea.setWidget(face_group)
        self.face_scrollarea.setVisible(False)

        self.body_btnGroup = QButtonGroup()
        self.body_btnGroup.setExclusive(False)
        self.body_btnGroup.buttonClicked[int].connect(self.setBody)

        self.body_scrollarea = QScrollArea(self)
        self.body_scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.body_scrollarea.setGeometry(self.layer_xywh)
        self.body_scrollarea.setWidgetResizable(True)
        body_group, self.body_file_path = self.createLayout_group('./image/back_썸네일/', self.body_btnGroup)
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

        self.sticker = True
        sticker_x, sticker_y = int(background_w * 0.875), int(background_h * 0.4724)
        sticker_w, sticker_h = int(background_w * 0.0648), int(background_w * 0.0648)
        self.stickerButton = QPushButton(self)
        self.stickerButton.setIcon(QIcon('./image/button_image/addsticker.png'))
        self.stickerButton.setIconSize(QSize(sticker_w, sticker_h))
        self.stickerButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.stickerButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.stickerButton.clicked.connect(lambda: self.setScroll(self.sticker))
        self.stickerButton.hide()

    def backPressEvent(self):
        self.video_thread.seg = False
        self.video_thread.stop()
        if not self.programRun:
            if self._back_window is None:
                self._back_window = start_UI.MakeWindow()
            self._back_window.show()
            self.close()
        else:
            self.face_scrollarea.setVisible(False)
            self.body_scrollarea.setVisible(False)
            upperImage = QPixmap('./image/button_image/another.png').scaled(
                QSize(int(background_w * 0.1472), int(background_h * 0.03645)))
            self.anotherLabel.setPixmap(QPixmap(upperImage))
            self.stickerButton.hide()
            self.bodyButton.show()
            self.faceButton.show()
            self.video_thread.capture = False
            self.programRun = False
            self.faceLabel.clear()


    def setRun(self):
        if self.now_run:
            self.video_thread.capture = False
            self.now_run = False
        else:
            self.video_thread.capture = True
            self.video_thread.start()
            self.now_run = True

    def saveResult(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        saveimg = self.label.pixmap().toImage()
        if not self.video_thread.seg:
            saveimg2 = self.faceLabel.pixmap().toImage()

            p = QPainter(saveimg)
            p.drawImage(saveimg.rect(), saveimg2)
            p.end()

        if fpath:
            saveimg.save(fpath)
            QMessageBox.about(
                self, 'Message', 'Image has been saved :)'
            )

    def setSticker(self, num):
        self.mouse = True
        self.stickerImage = QPixmap('./image/sticker_image/'+self.sticker_file_path[num]).scaled(
            QSize(int(background_w * 0.2), int(background_h * 0.137)))

    def setScroll(self, set):
        if set:
            self.sticker_scrollarea.setVisible(True)
            self.sticker = False
        else:
            self.sticker_scrollarea.setVisible(False)
            self.sticker = True
            self.mouse = False

    def mousePressEvent(self, e):  ###### 스티커 위치
        if self.mouse:
            if not self.video_thread.seg:
                sticker = QPainter(self.faceLabel.pixmap())
                sticker.drawPixmap(e.x()*0.9, e.y()*0.9, QPixmap(self.stickerImage))
                sticker.end()
                self.faceLabel.setPixmap(self.faceLabel.pixmap())
            else:
                sticker = QPainter(self.label.pixmap())
                sticker.drawPixmap(e.x() * 0.9, e.y() * 0.9, QPixmap(self.stickerImage))
                sticker.end()
                self.label.setPixmap(self.label.pixmap())

    @pyqtSlot(np.ndarray)
    def setImage(self, frame):
        h, w, ch = frame.shape
        show_img = frame
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(show_img.data,
                                      w, h, bytes_per_line,
                                      QImage.Format_BGR888 if ch == 3 else QImage.Format_BGRA8888)
        pixmap = QPixmap.fromImage(convert_to_qt_format)
        self.label.setPixmap(pixmap)

    def facebodyEvent(self, str):
        upperImage = QPixmap('./image/button_image/another2.png').scaled(
            QSize(int(background_w * 0.1472), int(background_h * 0.03645)))
        self.anotherLabel.setPixmap(QPixmap(upperImage))
        self.stickerButton.show()
        self.bodyButton.hide()
        self.faceButton.hide()
        self.video_thread.start()
        self.programRun = True

        if str == 'face':
            self.video_thread.seg = False
            self.face_scrollarea.setVisible(True)
        else:
            self.body_scrollarea.setVisible(True)

    def setFace(self, num):
        print('./image/face_큰창/'+self.face_file_path[num])
        facePixmap = QPixmap('./image/face_큰창/'+self.face_file_path[num]).scaled(
            QSize(background_w,int(background_h*0.7354)))
        self.faceLabel.setPixmap(QPixmap(facePixmap))
        self.upperLabel.raise_()

    @pyqtSlot(np.ndarray, np.ndarray)
    def setBodySeg(self, image, condition):
        output_image = np.where(condition, image, self.bg_image)

        h, w, ch = output_image.shape
        show_img = output_image
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(show_img.data,
                                      w, h, bytes_per_line,
                                      QImage.Format_BGR888 if ch == 3 else QImage.Format_BGRA8888)
        pixmap = QPixmap.fromImage(convert_to_qt_format)
        self.label.setPixmap(pixmap)

    def setBody(self, num):
        self.body_back = './image/back_big/%s'%self.body_file_path[num]
        self.bg_image = cv2.imread(self.body_back, cv2.IMREAD_COLOR)
        self.bg_image = cv2.resize(self.bg_image, (background_w, int(background_h * 0.7354)),
                                   interpolation=cv2.INTER_CUBIC)
        self.video_thread.seg = True
        self.video_thread.changeSeg.connect(self.setBodySeg)


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



class VideoThread(QThread):
    changePixmap = pyqtSignal(np.ndarray)
    changeSeg = pyqtSignal(np.ndarray, np.ndarray)
    seg = False
    capture = False
    def run(self):
        self.capture = True
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
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5
                    self.changeSeg.emit(image, condition)
            else:
                self.changePixmap.emit(frame)

    def stop(self):
        self.capture = False
        self.quit()