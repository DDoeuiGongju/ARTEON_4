from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os

from base_value import background_w, background_h
import start_UI

class StickerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.startImage = QImage('./image/background_image/sticker_back1.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.palette = QPalette()
        self.palette.setBrush(10, QBrush(self.startImage))

        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h*0.168)))
        upperImage = QPixmap('./image/background_image/upper.png').scaled(QSize(background_w, int(background_h*0.168)))
        self.upperLabel.setPixmap(QPixmap(upperImage))


        self._back_window = None
        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back.png'))
        self.back.setIconSize(QSize(int(background_w * 0.0259), int(background_h * 0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w * 0.0259),
                              int(background_h * 0.026))
        self.back.clicked.connect(self.backPressEvent)

        self.image_x = 0
        self.image_y = int(background_h*0.093)
        self.image_w = background_w
        self.image_h = int(background_h*0.83)

        # self.image = QImage(QSize(self.image_w, self.image_h), QImage.Format_RGB32)
        self.image = QImage('./image/background_image/canvas.png').scaled(QSize(self.image_w, self.image_h))
        self.drawing = False
        self.brush_size = 5
        self.brush_alpha = 255
        self.brush_color = QColor(0, 0, 0, self.brush_alpha)
        self.r, self.g, self.b = 0, 0, 0

        self.last_point = QPoint()

        self.stickerEvent = False
        self.btnGroup = QButtonGroup()
        self.btnGroup.setExclusive(False)
        self.btnGroup.buttonClicked[int].connect(self.setStickerEvent)
        self.file_path = []

        self.setColorButton()
        self.setPenButton()
        self.setAnotherButton()

        self.setPalette(self.palette)
        self.setWindowTitle('이리오너라')
        self.setGeometry(0, 0, background_w, background_h)
        self.show()

    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = start_UI.MakeWindow()
        self.close()
        self._back_window.show()

    def setColorButton(self):
        # 색 선택
        # https://doc.qt.io/qt-5/stylesheet-examples.html
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
        normal_x = int(background_w*0.478)
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

        #self.normalPen.setStyleSheet("background-image:url(brush.png);background-color: rgba(0,0,0,0%);border-style: outset;")
        self.normalPen.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.marker.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

    def setAnotherButton(self):
        save_x, save_y = int(background_w * 0.877), int(background_h * 0.77)
        save_w, save_h = int(background_w * 0.060), int(background_h * 0.0247)
        self.saveButton = QPushButton(self)
        self.saveButton.setIcon(QIcon('./image/button_image/save.png'))
        self.saveButton.setIconSize(QSize(save_w, save_h))
        self.saveButton.clicked.connect(self.saveResult)
        self.saveButton.setGeometry(save_x, save_y, save_w, save_h)
        self.saveButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setGeometry(int(background_w*0.037),int(background_h*0.3458),int(background_w*0.0324),int(background_h*0.2625))
        self.slider.setRange(3, 20)
        self.slider.valueChanged[int].connect(self.changeBrush_size)

        sticker_x, sticker_y = int(background_w * 0.03148), int(background_h * 0.8526)
        sticker_w, sticker_h = int(background_w * 0.139), int(background_h * 0.109)
        self.stickerButton = QPushButton(self)
        self.stickerButton.setIcon(QIcon('./image/button_image/sticker.png'))
        self.stickerButton.setIconSize(QSize(sticker_w, sticker_h))
        self.stickerButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.stickerButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.stickerButton.clicked.connect(lambda: self.setSticker(True))

        sticker_x, sticker_y = int(background_w * 0.03148), int(background_h * 0.848)
        sticker_w, sticker_h = int(background_w * 0.139), int(background_h * 0.127)
        self.drawButton = QPushButton(self)
        self.drawButton.setIcon(QIcon('./image/button_image/drawing.png'))
        self.drawButton.setIconSize(QSize(sticker_w, sticker_h))
        self.drawButton.setGeometry(sticker_x, sticker_y, sticker_w, sticker_h)
        self.drawButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.drawButton.clicked.connect(lambda: self.setSticker(False))
        self.drawButton.setVisible(False)

        self.layer_xywh = QRect(int(background_w * 0.205), int(background_h * 0.83),
                                int(background_w * 0.795), int(background_h * 0.171))
        self.createLayout_Container()
        self.scrollarea.setVisible(False)


    def setStickerEvent(self, path_num):
        self.stickerEvent = True
        self.veiwImage = QPixmap(self.file_path[path_num]).scaled(
            QSize(int(background_w*0.2), int(background_h*0.137)))


    def setSticker(self, set):
        if set:
            self.stickerButton.setVisible(False)
            self.drawButton.setVisible(True)
            self.scrollarea.setVisible(True)
        else:
            self.stickerEvent = False
            self.drawing = True
            self.stickerButton.setVisible(True)
            self.drawButton.setVisible(False)
            self.scrollarea.setVisible(False)


    def createLayout_group(self):
        sgroupbox = QGroupBox(self)
        stickerView_w, stickerView_h = int(background_w*0.2), int(background_h*0.137)

        layout_groupbox = QHBoxLayout(sgroupbox)
        layout_groupbox.setContentsMargins(0,0,0,0)

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

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setStyleSheet('background-color: #FFFFFF;')
        self.scrollarea.setGeometry(self.layer_xywh)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.createLayout_group())


    def changeBrush_size(self, size):
        self.brush_size = size


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

    def paintEvent(self, e):
        canvas = QPainter(self)

        canvas.drawImage(self.image_x, self.image_y, self.image, self.image_x, self.image_y, self.image_w, self.image_h)

    def mousePressEvent(self, e):
        if (e.button() == Qt.LeftButton) & (self.stickerEvent is False):
            self.drawing = True
            self.last_point = e.pos()
        else:
            stickerImage = QPainter(self.image)
            stickerImage.drawPixmap(e.x()*0.85, e.y()*0.85, QPixmap(self.veiwImage))
            self.update()



    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    def saveResult(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")

        if fpath:
            self.image.save(fpath)
            QMessageBox.about(
                self, 'Message', 'Sticker has been saved :)'
            )

