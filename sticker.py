from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os
import numpy as np

from base_value import background_w, background_h, style1, style2
import start_UI
import email_send

class StickerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 배경 이미지
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        self.startImage = QPixmap('./image/background_image/sticker_back1_.jpg')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.mainLabel.setPixmap(self.startImage)
        # self.palette = QPalette()
        # self.palette.setBrush(10, QBrush(self.startImage))

        # 상단 이미지
        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h*0.168)))
        upperImage = QPixmap('./image/background_image/upper.png').scaled(QSize(background_w, int(background_h*0.168)))
        self.upperLabel.setPixmap(QPixmap(upperImage))


        self.manualWindow = QLabel(self)
        self.manualWindow.resize(QSize(background_w, background_h))

        # self.anotherLabel = QLabel(self)
        # self.anotherLabel.resize(QSize(int(background_w * 0.06481), int(background_w * 0.06481)))
        # upperImage = QPixmap('./image/button_image/another4.png').scaled(
        #     QSize(int(background_w * 0.06481), int(background_w * 0.06481)))
        # self.anotherLabel.setPixmap(QPixmap(upperImage))
        # self.anotherLabel.move(int(background_w * 0.84444), int(background_h * 0.17447))

        # 사용법 버튼
        self.manual = True
        self.manualButton = QPushButton(self)
        self.manualButton.setIcon(QIcon('./image/button_image/manual.png'))
        self.manualButton.setIconSize(QSize(int(background_w * 0.093518), int(background_h * 0.053645)))
        self.manualButton.clicked.connect(self.manualEvent)
        self.manualButton.setGeometry(int(background_w * 0.84166), int(background_h * 0.17135)
                                      , int(background_w * 0.093518), int(background_h * 0.053645))
        self.manualButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        # 뒤로가기 버튼
        self._back_window = None
        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back.png'))
        self.back.setIconSize(QSize(int(background_w * 0.0259), int(background_h * 0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w * 0.0259),
                              int(background_h * 0.026))
        self.back.clicked.connect(self.backPressEvent)

        #스티커 그림이 그려질 공간
        self.image_x = 0
        self.image_y = int(background_h * 0.0927)
        self.image_w = background_w
        self.image_h = int(background_h * 0.7354)
        self.imageLabel = QLabel(self)
        self.piximage = QPixmap('./image/background_image/canvas.png').scaled(QSize(self.image_w, self.image_h))
        self.imageLabel.setGeometry(self.image_x, self.image_y, self.image_w, self.image_h)
        self.imageLabel.setPixmap(QPixmap(self.piximage))
        self.imageLabel.lower()
        self.mainLabel.lower()

        self.drawing = False
        self.brush_size = 5
        self.brush_alpha = 255
        self.brush_color = QColor(0, 0, 0, self.brush_alpha)
        self.r, self.g, self.b = 0, 0, 0

        self.sticker_ex = QLabel(self)            # 임시 스티커 공간
        self.sticker_size = int(background_w*0.2) # 초기 스티커 사이즈
        self.viewImage = None                     # 선택된 스티커 이미지
        self.viewImage_path = []                  # 선택된 스티커 이미지 경로

        self.last_point = QPoint()

        # 스티커 그룹
        self.stickerEvent = False

        self.file_path = []

        # 실행취소/다시실행 buffer
        self.undo = []
        self.redo = []


        self.setColorButton()
        # self.setPenButton()
        self.setAnotherButton()

    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = start_UI.MakeWindow()
        self.setCentralWidget(self._back_window)

    def setColorButton(self):
        button_size = int(background_w * 0.083)
        red_x = int(background_w*0.33)
        yellow_x = int(background_w*0.445)
        blue_x = int(background_w*0.561)
        green_x = int(background_w*0.677)
        colormap_x = int(background_w * 0.792)
        button_y = int(background_h*0.856)

        self.colorButton_red = QPushButton(self)
        self.colorButton_yellow = QPushButton(self)
        self.colorButton_blue = QPushButton(self)
        self.colorButton_green = QPushButton(self)

        self.colorButton_colormap = QPushButton(self)
        self.colorButton_colormap.setIcon(QIcon('./image/button_image/colormap.png'))
        self.colorButton_colormap.setIconSize(QSize(button_size, button_size))

        self.colorButton_red.clicked.connect(lambda: self.changeColor(self.colorButton_red))
        self.colorButton_yellow.clicked.connect(lambda: self.changeColor(self.colorButton_yellow))
        self.colorButton_blue.clicked.connect(lambda: self.changeColor(self.colorButton_blue))
        self.colorButton_green.clicked.connect(lambda: self.changeColor(self.colorButton_green))
        self.colorButton_colormap.clicked.connect(lambda: self.changeColor(self.colorButton_colormap))

        self.colorButton_red.setGeometry(red_x, button_y, button_size, button_size)
        self.colorButton_yellow.setGeometry(yellow_x, button_y, button_size, button_size)
        self.colorButton_blue.setGeometry(blue_x, button_y, button_size, button_size)
        self.colorButton_green.setGeometry(green_x, button_y, button_size, button_size)
        self.colorButton_colormap.setGeometry(colormap_x, button_y, button_size, button_size)

        self.colorButton_red.setStyleSheet("background-color: #C23D3D;border-style: outset;border-radius:20%;")
        self.colorButton_yellow.setStyleSheet("background-color: #F6B228;border-style: outset;border-radius: 20%;")
        self.colorButton_blue.setStyleSheet("background-color: #3B5167;border-style: outset;border-radius: 20%;")
        self.colorButton_green.setStyleSheet("background-color: #4E5E47;border-style: outset;border-radius: 20%;")
        self.colorButton_colormap.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

    def setPenButton(self):
        #펜 선택
        ## 수정 확인
        normal_x = int(background_w*0.478)
        #normal_x = int(background_w*0.5648)
        marker_x = int(background_w*0.65)
        pen_y = int(background_h*0.92)
        pen_w, pen_h = int(background_w*0.075), int(background_h*0.091)
        self.normalPen = QPushButton(self)
        self.normalPen.setIcon(QIcon('./image/button_image/brush.png'))
        self.normalPen.setIconSize(QSize(pen_w, pen_h))
        self.marker = QPushButton(self)
        self.marker.setIcon(QIcon('./image/button_image/marker.png'))
        self.marker.setIconSize(QSize(pen_w, pen_h))

        self.normalPen.clicked.connect(lambda: self.changeColor(self.normalPen))
        self.marker.clicked.connect(lambda: self.changeColor(self.marker))

        self.normalPen.setGeometry(normal_x, pen_y, pen_w, pen_h)
        self.marker.setGeometry(marker_x, pen_y, pen_w, pen_h)

        self.normalPen.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.marker.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

    def setAnotherButton(self):
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

        save_x, save_y = int(background_w * 0.877), int(background_h * 0.77)
        save_w, save_h = int(background_w * 0.060), int(background_h * 0.0247)
        self.saveButton = QPushButton(self)
        self.saveButton.setIcon(QIcon('./image/button_image/save.png'))
        self.saveButton.setIconSize(QSize(save_w, save_h))
        self.saveButton.clicked.connect(self.saveResult)
        self.saveButton.setGeometry(save_x, save_y, save_w, save_h)
        self.saveButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        self.penSlider = QSlider(Qt.Horizontal, self)
        self.penSlider.setGeometry(int(background_w * 0.33), int(background_h * 0.9484), int(background_h * 0.3), int(background_w * 0.0324))
        self.penSlider.setRange(3, 20)
        self.penSlider.valueChanged[int].connect(self.changeBrush_size)
        self.penSlider.setStyleSheet(style1)

        self.stickerSlider = QSlider(Qt.Vertical, self)
        self.stickerSlider.setGeometry(int(background_w * 0.06), int(background_h * 0.3458),
                                       int(background_w * 0.0324), int(background_h * 0.3328))
        self.stickerSlider.setRange(int((background_w*0.2)/2), int((background_w*0.2)*4))
        self.stickerSlider.valueChanged[int].connect(self.changeSticker_size)
        self.stickerSlider.setStyleSheet(style2)
        self.stickerSlider.setVisible(False)




        # sticker_x, sticker_y = int(background_w * 0.03148), int(background_h * 0.8526)
        # sticker_w, sticker_h = int(background_w * 0.139), int(background_h * 0.109)
        # self.stickerButton = QPushButton(self)
        # self.stickerButton.setIcon(QIcon('./image/button_image/sticker.png'))
        # self.stickerButton.setIconSize(QSize(sticker_w, sticker_h))
        # self.stickerButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        # self.stickerButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        # self.stickerButton.clicked.connect(lambda: self.setSticker(True))

        # 스티커 스크롤 오픈 버튼
        self.sticker = True # 스티커 스크롤 오픈 버튼이 눌리면
        sticker_x, sticker_y = int(background_w * 0.875), int(background_h * 0.4724)
        sticker_w, sticker_h = int(background_w * 0.0648), int(background_w * 0.0648)
        self.stickerButton = QPushButton(self)
        self.stickerButton.setIcon(QIcon('./image/button_image/addsticker.png'))
        self.stickerButton.setIconSize(QSize(sticker_w, sticker_h))
        self.stickerButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.stickerButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.stickerButton.clicked.connect(lambda: self.setSticker(self.sticker))

        self.popup = QPushButton(self)
        self.popup.setIcon(QIcon('./image/background_image/share_popup.png'))
        self.popup.setIconSize(QSize(int(background_w * 0.5713), int(background_h * 0.05886)))
        self.popup.setGeometry(int(background_w * 0.23055), int(background_h * 0.44114), int(background_w * 0.5713),
                               int(background_h * 0.05886))
        self.popup.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.popup.clicked.connect(self.popupEvent)
        self.popup.setVisible(False)

        # 공유 버튼
        share_x, share_y = int(background_w * 0.762), int(background_h * 0.17552)
        share_w, share_h = int(background_w * 0.05146), int(background_h * 0.0328)
        self.shareButton = QPushButton(self)
        self.shareButton.setIcon(QIcon('./image/button_image/share.png'))
        self.shareButton.setIconSize(QSize(share_w, share_h))
        self.shareButton.clicked.connect(self.sharePressEvent)
        self.shareButton.setGeometry(share_x, share_y, share_w, share_h)
        self.shareButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        sticker_x, sticker_y = int(background_w * 0.03148), int(background_h * 0.848)
        sticker_w, sticker_h = int(background_w * 0.139), int(background_h * 0.127)
        self.drawButton = QPushButton(self)
        self.drawButton.setIcon(QIcon('./image/button_image/drawing.png'))
        self.drawButton.setIconSize(QSize(sticker_w, sticker_h))
        self.drawButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.drawButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        # self.drawButton.clicked.connect(lambda: self.setSticker(False))
        self.drawButton.setVisible(True)

        # self.layer_xywh = QRect(int(background_w * 0.205), int(background_h * 0.83),
        #                         int(background_w * 0.795), int(background_h * 0.171))
        self.layer_xywh = QRect(0, int(background_h * 0.83),
                                background_w, int(background_h * 0.171))
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.scrollarea.setGeometry(self.layer_xywh)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.createLayout_group())
        self.scrollarea.setVisible(False)

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

    def manualEvent(self):
        if self.manual:
            image = QPixmap('./image/background_image/manual3.png').scaled(
                QSize(background_w, background_h))
            self.manualWindow.setPixmap(QPixmap(image))
            self.manualWindow.setVisible(True)
            self.manual = False
        else:
            self.manualWindow.setVisible(False)
            self.manual = True

    def setStickerEvent(self, path_num):
        self.stickerEvent = True
        self.viewImage_path = self.file_path[path_num]


    def setSticker(self, set):
        if set:
            self.stickerSlider.setVisible(True)
            self.penSlider.setVisible(False)
            # self.stickerButton.setVisible(False)
            # self.drawButton.setVisible(True)
            self.scrollarea.setVisible(True)
            self.sticker = False
        else:
            self.stickerSlider.setVisible(False)
            self.penSlider.setVisible(True)
            self.stickerEvent = False
            self.drawing = True
            # self.stickerButton.setVisible(True)
            # self.drawButton.setVisible(True)
            self.scrollarea.setVisible(False)
            self.sticker = True



    def createLayout_group(self):
        self.btnGroup = QButtonGroup()
        self.btnGroup.setExclusive(False)
        self.btnGroup.buttonClicked[int].connect(self.setStickerEvent)
        sgroupbox = QGroupBox(self)
        stickerView_w, stickerView_h = int(background_w*0.2), int(background_h*0.137)

        layout_groupbox = QHBoxLayout(sgroupbox)
        layout_groupbox.setContentsMargins(0,0,0,0)
        self.file_path=[]

        file_list = os.listdir('./image/sticker_image/')
        for i in range(len(file_list)):
            self.file_path.append('./image/sticker_image/' + file_list[i])
            button = (QPushButton(self))
            button.setIcon(QIcon('./image/sticker_image/' + file_list[i]))
            button.setIconSize(QSize(stickerView_w, stickerView_h))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
            self.btnGroup.addButton(button, i)
            layout_groupbox.addWidget(button)
        return sgroupbox

    def changeBrush_size(self, size):
        self.brush_size = size

    def changeSticker_size(self, size):
        self.sticker_size = size

    def changeColor(self, button):
        if button == self.colorButton_red:
            self.r, self.g, self.b = 203, 69, 67
        elif button == self.colorButton_yellow:
            self.r, self.g, self.b = 246, 178, 40
        elif button == self.colorButton_blue:
            self.r, self.g, self.b = 59, 81, 103
        elif button == self.colorButton_green:
            self.r, self.g, self.b = 78, 94, 71
        elif button == self.colorButton_colormap:
            color = QColorDialog.getColor()
            self.r, self.g, self.b = color.red(), color.green(), color.blue()
        elif button == self.normalPen:
            self.brush_alpha = 255
        elif button == self.marker:
            self.brush_alpha = 50
        self.brush_color = QColor(self.r, self.g, self.b, self.brush_alpha)

    def mousePressEvent(self, e):
        if (e.button() == Qt.LeftButton) & (self.stickerEvent is False):
            self.undo.append(self.imageLabel.pixmap().toImage())
            self.redo = []
            self.undoButton.setEnabled(True)
            self.redoButton.setEnabled(False)
            self.drawing = True
            self.last_point = QPoint(e.x(), e.y()-self.image_y)
        else:
            self.viewImage = QPixmap(self.viewImage_path).scaledToWidth(self.sticker_size)
            self.sticker_ex.resize(QSize(self.viewImage.size()))
            self.sticker_ex.setPixmap(QPixmap(self.viewImage))
            self.sticker_ex.move(e.x()-(self.viewImage.width()/2), e.y()-(self.viewImage.height()/2))

    def mouseDoubleClickEvent(self, e):
        if (e.button() == Qt.LeftButton) & (self.stickerEvent):
            self.undo.append(self.imageLabel.pixmap().toImage())
            self.redo = []
            self.undoButton.setEnabled(True)
            self.redoButton.setEnabled(False)
            self.sticker_ex.clear()
            stickerImage = QPainter(self.imageLabel.pixmap())
            stickerImage.drawPixmap(e.x()-(self.viewImage.width()/2), e.y()-(self.viewImage.height()/2)-self.image_y, QPixmap(self.viewImage))
            self.update()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.imageLabel.pixmap())
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, QPoint(e.x(), e.y()-self.image_y))
            self.last_point = QPoint(e.x(), e.y()-self.image_y)
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    def undoredoEvent(self, str):
        now = self.imageLabel.pixmap().toImage()
        self.imageLabel.clear()
        self.imageLabel.setPixmap(QPixmap(self.piximage))
        self.imageLabel.lower()
        self.mainLabel.lower()
        if str == 'undo' and self.undo:
            self.redo.append(now)
            pix = QPixmap.fromImage(self.undo[-1])
            hist = QPainter(self.imageLabel.pixmap())
            hist.drawPixmap(self.image_x, 0, pix)
            hist.end()
            self.update()
            del self.undo[-1]
            if not self.undo:
                self.undoButton.setEnabled(False)
            if self.redo:
                self.redoButton.setEnabled(True)
        elif str == 'redo' and self.redo:
            self.undoButton.setEnabled(True)
            self.undo.append(now)
            pix = QPixmap.fromImage(self.redo[-1])
            hist = QPainter(self.imageLabel.pixmap())
            hist.drawPixmap(self.image_x, 0, pix)
            hist.end()
            self.update()
            # print(len(self.redo))
            del self.redo[-1]
            if not self.redo:
                self.redoButton.setEnabled(False)


    def saveResult(self):
        # fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', './image/sticker_image/', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")
        fpath = './image/sticker_image/%f.png'%np.random.rand(1)
        if fpath:
            self.imageLabel.pixmap().toImage().save(fpath)
            self.popup.setIcon(QIcon('./image/background_image/sticker_popup.png'))
            self.popup.setVisible(True)
            with open('./remove.txt', 'a') as f:
                f.write(fpath+'\n')
        self.scrollarea.setWidget(self.createLayout_group())

    def sharePressEvent(self):
        fpath = 'temporary_s.png'
        with open('./remove.txt', 'a') as f:
            f.write(fpath + '\n')
        with open('./email.txt', 'r') as f:
            to_email = f.readline()

        self.saveimg = QImage(self.imageLabel.pixmap().toImage())
        if fpath:
            self.saveimg.save(fpath)
            # 이메일로 이미지 전송 thread
            self.th = email_send.emailTread(to_email, fpath)
            self.th.start()

            self.popup.setIcon(QIcon('./image/background_image/share_popup.png'))
            self.popup.setVisible(True)


    def popupEvent(self):
        self.popup.setVisible(False)