from PyQt5.QtGui import QPixmap

PATH = 'temp'
LEFT = PATH + '/left.png'
RIGHT = PATH + '/right.png'


def save(img: QPixmap, left: bool):
    path = LEFT if left else RIGHT
    img.save(path)


def get_pixmap_from_store(left: bool):
    return QPixmap(LEFT if left else RIGHT)


def get_pixmap(path: str):
    return QPixmap(path)

