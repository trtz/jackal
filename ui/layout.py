# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1107, 639)
        self.image_left = QtWidgets.QGraphicsView(Dialog)
        self.image_left.setGeometry(QtCore.QRect(10, 10, 512, 512))
        self.image_left.setObjectName("image_left")
        self.image_right = QtWidgets.QGraphicsView(Dialog)
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

