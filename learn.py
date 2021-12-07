from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from base_value import background_w, background_h, style1, style2

import email_send
import start_UI
import os

class LearnWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        self.startImage = QPixmap('./image/background_image/sticker_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.startImage.fill(QColor('#FFFFFF'))
        self.mainLabel.setPixmap(self.startImage)
        # self.palette = QPalette()
        # self.palette.setBrush(10, QBrush(self.startImage))

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

        self._home_window = None
        self.homeButton = QPushButton(self)
        self.homeButton.setIcon(QIcon('./image/button_image/home.png'))
        self.homeButton.setIconSize(QSize(int(background_w * 0.04629), int(background_h * 0.0282)))
        self.homeButton.clicked.connect(self.goHome)
        self.homeButton.setGeometry(int(background_w * 0.14722), int(background_h * 0.1776),
                                    int(background_w * 0.04629), int(background_h * 0.0282))
        self.homeButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        self.veiw = QLabel(self)
        self.veiw.resize(QSize(int(background_w * 0.749), int(background_h * 0.661)))
        self.veiw.move(int(background_w * 0.1259), int(background_h * 0.2354))

        self.selectImageButton()


        # self.setPalette(self.palette)
        # self.setWindowTitle('이리오너라')
        # self.setGeometry(0, 0, background_w, background_h)

        self._explain_window = None
        self.explain_path = None

    # 처음으로
    def goHome(self):
        if self._home_window is None:
            self._home_window = start_UI.StartWindow()
        self.setCentralWidget(self._home_window)


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
        # self.image_path = ('./image/learning_image/이미지/' + self.file_path[num][:-3] + 'jpg')
        self.explain_path = self.file_path[num]
        self._explain_window = LearnWindow2(self.explain_path)
        self.setCentralWidget(self._explain_window)


    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = start_UI.FirstWindow()
        # self._back_window.show()
        self.setCentralWidget(self._back_window)


class LearnWindow2(QMainWindow):
    def __init__(self, _explain_path):
        super().__init__()
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(QSize(background_w, background_h))

        self.startImage = QPixmap('./image/background_image/sticker_back.png')
        self.startImage = self.startImage.scaled(QSize(background_w, background_h))
        self.startImage.fill(QColor('#FFFFFF'))
        self.mainLabel.setPixmap(self.startImage)
        # self.palette = QPalette()
        # self.palette.setBrush(10, QBrush(self.startImage))

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

        self.veiw = QLabel(self)
        self.veiw.resize(QSize(int(background_w * 0.749), int(background_h * 0.661)))
        self.veiw.move(int(background_w * 0.1259), int(background_h * 0.2354))

        self._image_window = None
        self.explain_path = _explain_path
        self.image_path = None

        self.buttonPressEvent()

    # 처음으로
    def goHome(self):
        if self._home_window is None:
            self._home_window = start_UI.StartWindow()
        self.setCentralWidget(self._home_window)

    def buttonPressEvent(self):
        # self.image_path = './image/learning_image/이미지/' + self.explain_path[:-3] + 'jpg'
        self.image_path = self.explain_path[:-3] + 'jpg'

        self.view = QPushButton(self)
        self.view.setIcon(QIcon('./image/learning_image/설명/'+self.explain_path))
        self.view.setIconSize(QSize(int(background_w * 0.749), int(background_h * 0.661)))
        self.view.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.view.setGeometry(int(background_w * 0.1259), int(background_h * 0.2354),
                              int(background_w * 0.749), int(background_h * 0.661))
        self.view.show()
        self.view.clicked.connect(self.buttonDoubleClick)

        self.save = QPushButton(self)
        self.save.setIcon(QIcon('./image/button_image/save1.png'))
        self.save.setIconSize(QSize(int(background_w * 0.0648), int(background_w * 0.0648)))
        self.save.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.save.setGeometry(int(background_w * 0.7583), int(background_h * 0.177),
                              int(background_w * 0.0648), int(background_w * 0.0648))
        self.save.show()
        self.save.clicked.connect(lambda: self.savePressEvent('./image/learning_image/이미지/' + self.image_path))


    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = LearnWindow1()
        self.setCentralWidget(self._back_window)

    def buttonDoubleClick(self):
        self._image_window = ImageViewerWindow(self.image_path)
        self.setCentralWidget(self._image_window)


    def savePressEvent(self, image_path):
        # fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', './', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")
        fpath = 'temporary.png'
        with open('./remove.txt', 'a') as f:
            f.write(fpath + '\n')
        with open('./email.txt', 'r') as f:
            to_email = f.readline()
        self.saveimg = QImage(image_path)
        if fpath:
            self.saveimg.save(fpath)
            # 이메일로 이미지 전송 thread
            self.th = email_send.emailTread(to_email, fpath)
            self.th.start()
            self.popup.setVisible(True)
            self.popup.raise_()


    def popupEvent(self):
        self.popup.setVisible(False)



from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import QEvent, QPinchGesture
from typing import cast, Optional


class ImageViewer(QtWidgets.QGraphicsView):
    factor = 1.2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setBackgroundRole(QtGui.QPalette.Dark)

        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self._pixmap_item)

    def load_image(self, fileName):
        pixmap = QtGui.QPixmap(fileName)
        pixmap = pixmap.scaledToHeight(background_h)
        if pixmap.isNull():
            return False
        self._pixmap_item.setPixmap(pixmap)
        return True

    def zoomIn(self):
        self.zoom(self.factor)

    def zoomOut(self):
        self.zoom(1 / self.factor)

    def zoom(self, f):
        self.scale(f, f)

    def resetZoom(self):
        self.resetTransform()

    def fitToWindow(self):
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
    #
    # def gestureEvent(self, event: QGestureEvent):
    #     gesture = event.gesture(Qt.PinchGesture)
    #     if gesture.changeFlags() & QPinchGesture.ScaleFactorChanged:
    #         anchor = gesture.centerPoint().toPoint()
    #         anchor = self.mapToScene(anchor)
    #         self.__setZoomLevel(self.factor * gesture.scaleFactor(),
    #                             anchor=anchor)
    #         event.accept()
    #
    # def event(self, event: QEvent) -> bool:
    #     if event.type() == QEvent.Gesture:
    #         self.gestureEvent(cast(QGestureEvent, event))
    #     return super().event(event)


class ImageViewerWindow(QMainWindow):
    def __init__(self, fileName=None):
        super().__init__()

        self.explain_path = fileName[:-3] + 'png'

        self.view = ImageViewer()
        self.setCentralWidget(self.view)

        self.createActions()
        self.createMenus()

        self.upperLabel = QLabel(self)
        self.upperLabel.resize(QSize(background_w, int(background_h * 0.168)))
        upperImage = QPixmap('./image/background_image/upper.png').scaled(
            QSize(background_w, int(background_h * 0.168)))
        self.upperLabel.setPixmap(QPixmap(upperImage))
        self.resize(background_w, background_h)

        if fileName:
            is_loaded = self.view.load_image('./image/learning_image/이미지/' +fileName)
            self.fitToWindowAct.setEnabled(is_loaded)
            self.updateActions()

        self._back_window = None
        self.back = QPushButton(self)
        self.back.setIcon(QIcon('./image/button_image/back2.png'))
        self.back.setIconSize(QSize(int(background_w * 0.0259), int(background_h * 0.026)))
        self.back.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.back.setGeometry(int(background_w * 0.0925), int(background_h * 0.179), int(background_w * 0.0259),
                              int(background_h * 0.026))
        self.back.clicked.connect(self.backPressEvent)

        in_x, in_y = int(background_w * 0.887), int(background_h * 0.48125)
        in_w, in_h = int(background_w * 0.07685), int(background_w * 0.07685)
        self.inButton = QPushButton(self)
        self.inButton.setIcon(QIcon('./image/button_image/zoomin.png'))
        self.inButton.setIconSize(QSize(in_w, in_h))
        self.inButton.clicked.connect(self.view.zoomIn)
        self.inButton.setGeometry(in_x, in_y, in_w, in_h)
        self.inButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")

        out_x, out_y = int(background_w * 0.887), int(background_h * 0.526)
        self.outButton = QPushButton(self)
        self.outButton.setIcon(QIcon('./image/button_image/zoomout.png'))
        self.outButton.setIconSize(QSize(in_w, in_h))
        self.outButton.clicked.connect(self.view.zoomOut)
        self.outButton.setGeometry(out_x, out_y, in_w, in_h)
        self.outButton.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")


    def backPressEvent(self):
        if self._back_window is None:
            self._back_window = LearnWindow2(self.explain_path)
        self.setCentralWidget(self._back_window)


    def fitToWindow(self):
        if self.fitToWindowAct.isChecked():
            self.view.fitToWindow()
        else:
            self.view.resetZoom()
        self.updateActions()

    def createActions(self):
        self.zoomInAct = QtWidgets.QAction(
            self.tr("Zoom &In (10%)"),
            self,
            shortcut="Ctrl+up",
            enabled=False,
            triggered=self.view.zoomIn,
        )
        self.zoomOutAct = QtWidgets.QAction(
            self.tr("Zoom &Out (10%)"),
            self,
            shortcut="Ctrl+down",
            enabled=False,
            triggered=self.view.zoomOut,
        )
        self.normalSizeAct = QtWidgets.QAction(
            self.tr("&Normal Size"),
            self,
            shortcut="Ctrl+N",
            enabled=False,
            triggered=self.view.resetZoom,
        )
        self.fitToWindowAct = QtWidgets.QAction(
            self.tr("&Fit to Window"),
            self,
            enabled=False,
            checkable=True,
            shortcut="Ctrl+F",
            triggered=self.fitToWindow,
        )



    def createMenus(self):

        self.viewMenu = QtWidgets.QMenu(self.tr("&ZOOM"), self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().hide()

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
