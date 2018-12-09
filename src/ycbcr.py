import numpy as np
from PIL import Image

from src.load import RIGHT


def ycbcr_(R, G, B):
    Y = (77 / 256) * R + (150 / 256) * G + (29 / 256) * B
    Cb = (144 / 256) * (B - Y) + 128
    Cr = (183 / 256) * (R - Y) + 128
    return Y, Cb, Cr


def ycbcr2(img1):
    res = [[0 for i in range(512)] for j in range(512)]
    for i in range(512):
        for j in range(512):
            x1 = img1[i, j]
            y1, cb1, cr1 = ycbcr_(*x1)
            res[j][i] = [y1, cb1, cr1]
    return res


def ycbcr1(path1):
    img1 = Image.open(path1).load()
    return ycbcr2(img1)


def fuck(arr):
    np1 = np.array(arr).astype('uint8')
    img = Image.fromarray(np1)
    img.save(RIGHT)


def to_rgb(arr):
    res = [[0 for i in range(512)] for j in range(512)]
    for i in range(512):
        for j in range(512):
            temp = arr[i, j]
            temp1 = ycbcr_(*temp)
            res[j][i] = to_rgb_(*temp1)
    fuck(res)


def to_rgb_(Y, Cb, Cr):
    R = Y + (256 / 183) * (Cr - 128)
    G = Y - (5329 / 15481) * (Cb - 128) - (11103 / 15481) * (Cr - 128)
    B = Y + (256 / 144) * (Cb - 128)
    return int(R), int(G), int(B)
