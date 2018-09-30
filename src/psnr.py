from math import log10
import cv2


def psnr(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    sum = 0
    for i in range(512):
        for j in range(512):
            for k in range(3):
                x1 = img1[i][j][k]
                x2 = img2[i][j][k]
                sum += (float(x1) - float(x2)) ** 2
    PIXEL_MAX = 255.0
    if sum == 0:
        return -1
    res = 10 * log10(3 * PIXEL_MAX ** 2 * 512 ** 2 / sum)
    return res