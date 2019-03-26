import pickle

from PIL import Image
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel

from src.dct import dct1, idct
from src.fractal.fractal import fractal1
from src.gla import gla1
from src.grayscale import grayscale
from src.jpeg.compression import nync_, matrix_comp, standart_matrix_comp
from src.jpeg.thin import thin_1
from src.load import save, LEFT, RIGHT
from src.mcut.mcut import median_cut
from src.psnr import psnr
from src.quant import urgb343_, urgb442_, ycbcrq_
from src.ycbcr import ycbcr1, save_arr_to_right, to_rgb
from src.zip import gzip, zig_zag, un_zig_zag


class Ui_Dialog(object):
    def __init__(self):
        self.temp = None
        self.img_instance_right = None
        self.img_instance_left = None
        self.current = True

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
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

        self.toggle_image = QtWidgets.QPushButton(Dialog)
        self.toggle_image.setGeometry(QtCore.QRect(880, 540, 161, 23))
        self.toggle_image.setObjectName("toggle_image")

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
        self.urgb442.setObjectName('urgb442')

        self.ycbcrq1 = QtWidgets.QPushButton(Dialog)
        self.ycbcrq1.setGeometry(QtCore.QRect(780, 570, 80, 23))
        self.ycbcrq1.setObjectName('ycbcrq1')

        self.ycbcrq2 = QtWidgets.QPushButton(Dialog)
        self.ycbcrq2.setGeometry(QtCore.QRect(880, 570, 80, 23))
        self.ycbcrq2.setObjectName('ycbcrq2')

        self.ycbcrq3 = QtWidgets.QPushButton(Dialog)
        self.ycbcrq3.setGeometry(QtCore.QRect(980, 570, 80, 23))
        self.ycbcrq3.setObjectName('ycbcrq3')

        self.gla = QtWidgets.QPushButton(Dialog)
        self.gla.setGeometry(QtCore.QRect(200, 600, 50, 23))
        self.gla.setObjectName('ycbcrq3')

        self.mcut = QtWidgets.QPushButton(Dialog)
        self.mcut.setGeometry(QtCore.QRect(270, 600, 50, 23))
        self.mcut.setObjectName('mcut')

        self.fractal = QtWidgets.QPushButton(Dialog)
        self.fractal.setGeometry(QtCore.QRect(340, 600, 50, 23))
        self.fractal.setObjectName('fractal')

        self.thin444 = QtWidgets.QPushButton(Dialog)
        self.thin444.setGeometry(QtCore.QRect(410, 600, 50, 23))
        self.thin444.setObjectName('thin444')

        self.thin2h1v = QtWidgets.QPushButton(Dialog)
        self.thin2h1v.setGeometry(QtCore.QRect(480, 600, 50, 23))
        self.thin2h1v.setObjectName('thin2h1v')

        self.thin2v1h = QtWidgets.QPushButton(Dialog)
        self.thin2v1h.setGeometry(QtCore.QRect(550, 600, 50, 23))
        self.thin2v1h.setObjectName('thin2v1h')

        self.thin2v2h = QtWidgets.QPushButton(Dialog)
        self.thin2v2h.setGeometry(QtCore.QRect(620, 600, 50, 23))
        self.thin2v2h.setObjectName('thin2v2h')

        self.dct = QtWidgets.QPushButton(Dialog)
        self.dct.setGeometry(QtCore.QRect(690, 600, 50, 23))
        self.dct.setObjectName('dct')

        self.idct = QtWidgets.QPushButton(Dialog)
        self.idct.setGeometry(QtCore.QRect(760, 600, 50, 23))
        self.idct.setObjectName('idct')

        self.nync = QtWidgets.QPushButton(Dialog)
        self.nync.setGeometry(QtCore.QRect(830, 600, 50, 23))
        self.nync.setObjectName('nync')

        self.mcomp = QtWidgets.QPushButton(Dialog)
        self.mcomp.setGeometry(QtCore.QRect(900, 600, 50, 23))
        self.mcomp.setObjectName('mcomp')

        self.smcomp = QtWidgets.QPushButton(Dialog)
        self.smcomp.setGeometry(QtCore.QRect(200, 630, 50, 23))
        self.smcomp.setObjectName('smcomp')

        self.gzip = QtWidgets.QPushButton(Dialog)
        self.gzip.setGeometry(QtCore.QRect(270, 630, 50, 23))
        self.gzip.setObjectName('gzip')

        self.zigzag = QtWidgets.QPushButton(Dialog)
        self.zigzag.setGeometry(QtCore.QRect(340, 630, 50, 23))
        self.zigzag.setObjectName('zigzag')

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
        self.urgb442.setText(_translate("Dialog", 'URGB442'))
        self.ycbcrq1.setText(_translate("Dialog", 'YCbCr244'))
        self.ycbcrq2.setText(_translate("Dialog", 'YCbCr523'))
        self.ycbcrq3.setText(_translate("Dialog", 'YCbCr532'))
        self.gla.setText(_translate("Dialog", 'GLA'))
        self.mcut.setText(_translate("Dialog", 'MC'))
        self.fractal.setText(_translate("Dialog", "Fractal"))
        self.thin444.setText(_translate("Dialog", "Thin444"))
        self.thin2h1v.setText(_translate("Dialog", "Thin2h1v"))
        self.thin2v1h.setText(_translate("Dialog", "Thin2v1h"))
        self.thin2v2h.setText(_translate("Dialog", "Thin2v2h"))
        self.dct.setText(_translate("Dialog", "DCT"))
        self.idct.setText(_translate("Dialog", "iDCT"))
        self.toggle_image.setText(_translate("Dialog", "Current = " + "left" if self.current else "Current = right"))
        self.nync.setText(_translate("Dialog", "NyNc"))
        self.mcomp.setText(_translate("Dialog", "MC"))
        self.smcomp.setText(_translate("Dialog", "SMC"))
        self.gzip.setText(_translate("Dialog", "Gzip"))
        self.zigzag.setText(_translate("Dialog", "ZigZag"))

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
        self.ycbcrq1.clicked.connect(lambda: self.ycbcrq(6, 6, 6))
        self.ycbcrq2.clicked.connect(lambda: self.ycbcrq(5, 2, 3))
        self.ycbcrq3.clicked.connect(lambda: self.ycbcrq(5, 3, 2))
        self.gla.clicked.connect(lambda: self.gla_())
        self.mcut.clicked.connect(lambda: self.mcut_())
        self.fractal.clicked.connect(lambda: self.fractal_())
        self.thin444.clicked.connect(lambda: self.thin_(1, 1, 1, 1, 1, 1))
        self.thin2h1v.clicked.connect(lambda: self.thin_(1, 1, 1, 2, 1, 2))
        self.thin2v1h.clicked.connect(lambda: self.thin_(1, 1, 2, 1, 2, 1))
        self.thin2v2h.clicked.connect(lambda: self.thin_(1, 1, 2, 2, 2, 2))
        self.dct.clicked.connect(lambda: self.dct_())
        self.idct.clicked.connect(lambda: self.idct_())
        self.toggle_image.clicked.connect(lambda: self.toggle_image_())
        self.nync.clicked.connect(lambda: self.nync2())
        self.mcomp.clicked.connect(lambda: self.mcomp1(1))
        self.smcomp.clicked.connect(lambda: self.mcomp1(1))
        self.gzip.clicked.connect(lambda: self.gzip_())
        self.zigzag.clicked.connect(lambda: self.zigzag_())

    def gzip_(self):
        gzip(Image.open(self.get_current_image()), 'gzip.jpeg')

    def zigzag_(self):
        file = Image.open(self.get_current_image()).load()
        res = zig_zag(file, 512)
        with open('zz.dat', 'wb') as f:
            pickle.dump(res, f)
        self.unzigzag()

    def unzigzag(self):
        with open('zz.dat', 'rb') as f:
            new_data = pickle.load(f)
            res = un_zig_zag(new_data, 512)
            res1 = [[0 for j in range(512)] for i in range(512)]
            for i in range(512):
                for j in range(512):
                    res1[i][j] = res[j][i]
            save_arr_to_right(res1)
            self.update_img(False)

    def nync2(self):
        if self.temp is None:
            self.dct_()
        self.temp = nync_(self.temp, 2, 2)
        self.idct_()

    def smcomp1(self, factor):
        if self.temp is None:
            self.dct_()
        self.temp = standart_matrix_comp(self.temp, factor)
        self.idct_()

    def mcomp1(self, factor):
        if self.temp is None:
            self.dct_()
        self.temp = matrix_comp(self.temp, factor)
        self.idct_()

    def toggle_image_(self):
        self.current = not self.current
        self.toggle_image.setText("Current = " + "left" if self.current else "Current = right")

    def get_current_image(self):
        return LEFT if self.current else RIGHT

    def thin_(self, yv, yh, crv, crh, cbv, cbh):
        img = Image.open(self.get_current_image()).load()
        thin_1(img, yv, yh, crv, crh, cbv, cbh)
        self.update_img(False)

    def idct_(self):
        image = self.temp
        idct(image)
        self.update_img(False)

    def dct_(self):
        image = Image.open(self.get_current_image()).load()
        self.temp = dct1(image)
        print('DCT done')
        self.update_img(False)

    def gla_(self):
        gla1(LEFT, 256)
        self.update_img(False)
        # image = Image.open(LEFT).load()
        # image2 = []
        # for i in range(512):
        #     for j in range(512):
        #         image2.append(image[i, j])
        # res = gla2(image2, 256)
        # save_arr_to_right(res)
        # self.update_img(False)

    def fractal_(self):
        fractal1(LEFT)
        self.update_img(False)

    def mcut_(self):
        res = median_cut(LEFT, 256)
        save_arr_to_right(res)
        self.update_img(False)

    def urgb343_(self):
        img = Image.open(LEFT).load()
        img1 = urgb343_(img)
        save_arr_to_right(img1)
        self.update_img(False)

    def ycbcrq(self, x, y, z):
        img = Image.open(LEFT).load()
        img1 = ycbcrq_(img, x, y, z)
        save_arr_to_right(img1)
        self.update_img(False)

    def urgb442_(self):
        img = Image.open(LEFT).load()
        img1 = urgb442_(img)
        save_arr_to_right(img1)
        self.update_img(False)

    def ycbcr_to_rgb1(self):
        img = Image.open(LEFT).load()
        to_rgb(img)
        self.update_img(False)

    def ycbcr(self, mode):
        res = ycbcr1(LEFT)
        curr = [[int(res[j][i][mode]) for i in range(512)] for j in range(512)]
        save_arr_to_right(curr)
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
        pixmap = QPixmap(LEFT if left else RIGHT).scaledToHeight(512)
        curr = self.image_left if left else self.image_right
        curr.setPixmap(pixmap)

    def to_grayscale(self, mode=1):
        res = grayscale(LEFT, mode)
        res.save(RIGHT)
        self.update_img(False)
