from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

from base_value import background_w, background_h
import start_UI

import cv2
import numpy as np

from PIL import ImageQt

class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.startImage = QImage('./image/background_image/video_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.palette = QPalette()
        self.palette.setBrush(10, QBrush(self.startImage))

        self.image_x = 0
        self.image_y = int(background_h * 0.093)
        self.image_w = background_w
        self.image_h = int(background_h * 0.83)

        # self.image = QImage(QSize(self.image_w, self.image_h), QImage.Format_RGB32)
        self.label = QLabel(self)
        self.label.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)
        self.label.setPixmap(QPixmap())

        self.video_thread = VideoThread()
        self.video_thread.changePixmap.connect(self.setImage)

        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h*0.168)))
        upperImage = QPixmap('./image/background_image/upper.png').scaled(QSize(background_w, int(background_h*0.168)))
        self.upperLabel.setPixmap(QPixmap(upperImage))

        self.btnGroup = QButtonGroup()
        self.btnGroup.setExclusive(False)
        self.btnGroup.buttonClicked[int].connect(self.setFace)
        self.face_file_path = []
        self.body_file_path =[]

        self.last_point = QPoint()

        self.setButton()

        self.setPalette(self.palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)
        self.show()

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

        face_x, face_y = int(background_w * 0.3444), int(background_h * 0.8552)
        face_w, face_h = int(background_w * 0.1389), int(background_h * 0.11875)
        self.faceButton = QPushButton(self)
        self.faceButton.setIcon(QIcon('./image/button_image/face.png'))
        self.faceButton.setIconSize(QSize(face_w, face_h))
        self.faceButton.clicked.connect(self.faceEvent)
        self.faceButton.setGeometry(face_x, face_y, face_w, face_h)
        self.faceButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        self.layer_xywh = QRect(0, int(background_h * 0.8286), background_w, int(background_h * 0.1718))
        self.createLayout_Container()
        self.scrollarea.setVisible(False)

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

    def backPressEvent(self):
        print(1)
        self.video_thread.capture = False
        if self._back_window is None:
            self._back_window = start_UI.MakeWindow()
        self._back_window.show()
        self.close()

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
        saveimg = ImageQt.fromqpixmap(self.label.pixmap())
        if fpath:
            saveimg.save(fpath)
            QMessageBox.about(
                self, 'Message', 'Sticker has been saved :)'
            )

    def setFace(self, num):
        print('./image/face_큰창/'+self.face_file_path[num])

    def createLayout_group(self):
        sgroupbox = QGroupBox(self)
        stickerView_w, stickerView_h = int(background_w * 0.2375), int(background_h*0.1542)

        layout_groupbox = QHBoxLayout(sgroupbox)
        layout_groupbox.setContentsMargins(0, 0, 0, 0)

        file_list = os.listdir('./image/face_썸네일/')
        for i in range(len(file_list)):
            self.face_file_path.append(file_list[i])
            button = (QPushButton(self))
            button.setIcon(QIcon('./image/face_썸네일/' + file_list[i]))
            button.setIconSize(QSize(stickerView_w, stickerView_h))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
            self.btnGroup.addButton(button, i)
            layout_groupbox.addWidget(button)

        return sgroupbox

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.scrollarea.setGeometry(self.layer_xywh)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.createLayout_group())

    def faceEvent(self):
        self.video_thread.start()
        self.scrollarea.setVisible(True)



class VideoThread(QThread):
    changePixmap = pyqtSignal(np.ndarray)
    capture = False
    def run(self):
        self.capture = True
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.capture:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            self.changePixmap.emit(frame)