# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QLabel


class Ui_Dialog(object):
    def __init__(self):
        self.img_instance_right = None
        self.img_instance_left = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1107, 639)
        self.image_left = QLabel(self)
        self.image_left.setGeometry(QtCore.QRect(10, 10, 512, 512))
        self.image_left.setObjectName("image_left")

        self.image_right = QLabel(self)
        self.image_right.setGeometry(QtCore.QRect(580, 10, 512, 512))
        self.image_right.setObjectName("image_right")

        self.open_button_left = QtWidgets.QPushButton(Dialog)
        self.open_button_left.setGeometry(QtCore.QRect(10, 540, 141, 23))
        self.open_button_left.setObjectName("open_button_left")
        self.open_button_right = QtWidgets.QPushButton(Dialog)
        self.open_button_right.setGeometry(QtCore.QRect(580, 540, 161, 23))
        self.open_button_right.setObjectName("open_button_right")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.open_button_left.setText(_translate("Dialog", "Open left image"))
        self.open_button_right.setText(_translate("Dialog", "Open right image"))

        self.open_button_left.clicked.connect(lambda: self.handle_open_file(True))
        self.open_button_right.clicked.connect(lambda: self.handle_open_file(False))

    def handle_open_file(self, left: bool):
        fname = QFileDialog.getOpenFileName(self, 'Open image', '')[0]
        self.set_image(fname, left)

    def set_image(self, image_name: str, left: bool):
        curr = self.image_left if left else self.image_right
        pixmap = QPixmap(image_name)
        curr.setPixmap(pixmap)
