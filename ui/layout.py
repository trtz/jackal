from PIL import Image
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel

from src.grayscale import grayscale
from src.load import save, LEFT, RIGHT
from src.psnr import psnr
from src.quant import urgb343_, urgb442_
from src.ycbcr import ycbcr1, fuck, to_rgb


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

        self.to_grayscale_button = QtWidgets.QPushButton(Dialog)
        self.to_grayscale_button.setGeometry(QtCore.QRect(200, 540, 141, 23))
        self.to_grayscale_button.setObjectName("to_grayscale_button")

        self.to_grayscale_button2 = QtWidgets.QPushButton(Dialog)
        self.to_grayscale_button2.setGeometry(QtCore.QRect(400, 540, 141, 23))
        self.to_grayscale_button2.setObjectName("to_grayscale_button2")

        self.psnr_button = QtWidgets.QPushButton(Dialog)
        self.psnr_button.setGeometry(QtCore.QRect(10, 570, 141, 23))
        self.psnr_button.setObjectName('psnr_button')

        self.y_button = QtWidgets.QPushButton(Dialog)
        self.y_button.setGeometry(QtCore.QRect(200, 570, 50, 23))
        self.y_button.setObjectName('y_button')

        self.cb_button = QtWidgets.QPushButton(Dialog)
        self.cb_button.setGeometry(QtCore.QRect(270, 570, 50, 23))
        self.cb_button.setObjectName('cb_button')

        self.cr_button = QtWidgets.QPushButton(Dialog)
        self.cr_button.setGeometry(QtCore.QRect(340, 570, 50, 23))
        self.cr_button.setObjectName('cr_button')

        self.ycbcr_to_rgb = QtWidgets.QPushButton(Dialog)
        self.ycbcr_to_rgb.setGeometry(QtCore.QRect(410, 570, 150, 23))
        self.ycbcr_to_rgb.setObjectName('ycbcr_to_rgb')

        self.urgb343 = QtWidgets.QPushButton(Dialog)
        self.urgb343.setGeometry(QtCore.QRect(580, 570, 80, 23))
        self.urgb343.setObjectName('urgb343')

        self.urgb442 = QtWidgets.QPushButton(Dialog)
        self.urgb442.setGeometry(QtCore.QRect(680, 570, 80, 23))
        self.urgb442.setObjectName('urgb343')

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.update_img(True)
        self.update_img(False)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.open_button_left.setText(_translate("Dialog", "Open left image"))
        self.open_button_right.setText(_translate("Dialog", "Open right image"))
        self.to_grayscale_button.setText(_translate("Dialog", "To grayscale"))
        self.to_grayscale_button2.setText(_translate("Dialog", "To grayscale 2"))
        self.psnr_button.setText(_translate("Dialog", "PSNR"))
        self.y_button.setText(_translate("Dialog", 'Y'))
        self.cb_button.setText(_translate("Dialog", 'Cb'))
        self.cr_button.setText(_translate("Dialog", 'Cr'))
        self.ycbcr_to_rgb.setText(_translate("Dialog", 'RGB->YCbCr->RGB'))
        self.urgb343.setText(_translate("Dialog", 'URGB343'))

        self.open_button_left.clicked.connect(lambda: self.handle_open_file(True))
        self.open_button_right.clicked.connect(lambda: self.handle_open_file(False))
        self.to_grayscale_button.clicked.connect(lambda: self.to_grayscale(1))
        self.to_grayscale_button2.clicked.connect(lambda: self.to_grayscale(2))
        self.psnr_button.clicked.connect(lambda: self.psnr())
        self.y_button.clicked.connect(lambda: self.ycbcr(0))
        self.cb_button.clicked.connect(lambda: self.ycbcr(1))
        self.cr_button.clicked.connect(lambda: self.ycbcr(2))
        self.ycbcr_to_rgb.clicked.connect(lambda: self.ycbcr_to_rgb1())
        self.urgb343.clicked.connect(lambda: self.urgb343_())
        self.urgb442.clicked.connect(lambda: self.urgb442_())

    def urgb343_(self):
        img = Image.open(LEFT).load()
        img1 = urgb343_(img)
        fuck(img1)
        self.update_img(False)

    def urgb442_(self):
        img = Image.open(LEFT).load()
        img1 = urgb442_(img)
        fuck(img1)
        self.update_img(False)

    def ycbcr_to_rgb1(self):
        img = Image.open(LEFT).load()
        to_rgb(img)
        self.update_img(False)

    def ycbcr(self, mode):
        res = ycbcr1(LEFT)
        curr = [[int(res[j][i][mode]) for i in range(512)] for j in range(512)]
        fuck(curr)
        self.update_img(False)

    def psnr(self):
        res = psnr(LEFT, RIGHT)
        self.psnr_button.setText('PSNR = ' + str(res))

    def handle_open_file(self, left: bool):
        fname = QFileDialog.getOpenFileName(self, 'Open image', '')[0]
        self.set_image(fname, left)

    def set_image(self, image_name: str, left: bool):
        curr = self.image_left if left else self.image_right
        pixmap = QPixmap(image_name)
        curr.setPixmap(pixmap)
        save(pixmap, left)

    def update_img(self, left=True):
        pixmap = QPixmap(LEFT if left else RIGHT)
        curr = self.image_left if left else self.image_right
        curr.setPixmap(pixmap)

    def to_grayscale(self, mode=1):
        res = grayscale(LEFT, mode)
        res.save(RIGHT)
        self.update_img(False)
