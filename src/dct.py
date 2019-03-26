import math

import numpy as np
from PIL import Image

from src.load import RIGHT
from src.ycbcr import ycbcr_, to_rgb_


def get_m():
    dct_matrix = np.zeros((8, 8))

    for i in range(0, 8):
        for j in range(0, 8):
            if i == 0:
                dct_matrix[i][j] = 1 / math.sqrt(8)
            else:
                dct_matrix[i][j] = math.sqrt(2 / 8) * math.cos((math.pi * (2 * j + 1) * i) / (2 * 8))

    return dct_matrix


def multiply_block(mr, m, not_reverse=True):
    def mul(a, b, c):
        return np.matmul(np.matmul(a, b), c)

    mr1 = mul(m, mr, m.transpose()) if not_reverse else mul(m.transpose(), mr, m)
    return mr1


def dct1(d):
    m = get_m()
    getter = lambda i, j: d[j, i]
    result = [[[0] for _ in range(512)] for _ in range(512)]
    for i in range(0, 512, 8):
        for j in range(0, 512, 8):
            block1 = np.zeros((8, 8))
            block2 = np.zeros((8, 8))
            block3 = np.zeros((8, 8))
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    rgb = getter(i1, j1)
                    ycbcr = ycbcr_(*rgb)
                    block1[i1 - i, j1 - j] = ycbcr[0]
                    block2[i1 - i, j1 - j] = ycbcr[1]
                    block3[i1 - i, j1 - j] = ycbcr[2]
            block1 = multiply_block(block1, m)
            block2 = multiply_block(block2, m)
            block3 = multiply_block(block3, m)
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    result[j1][i1] = [block1[i1 - i, j1 - j], block2[i1 - i, j1 - j], block3[i1 - i, j1 - j]]
    return result


def idct(d, output_file=RIGHT):
    m = get_m()
    getter = lambda i, j: d[j][i]
    result = Image.new("RGB", (512, 512))
    for i in range(0, 512, 8):
        for j in range(0, 512, 8):
            block1 = np.zeros((8, 8))
            block2 = np.zeros((8, 8))
            block3 = np.zeros((8, 8))
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    ycbcr = getter(i1, j1)
                    block1[i1 - i, j1 - j] = ycbcr[0]
                    block2[i1 - i, j1 - j] = ycbcr[1]
                    block3[i1 - i, j1 - j] = ycbcr[2]
            block1 = multiply_block(block1, m, False)
            block2 = multiply_block(block2, m, False)
            block3 = multiply_block(block3, m, False)
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    var = [block1[i1 - i, j1 - j], block2[i1 - i, j1 - j], block3[i1 - i, j1 - j]]
                    rgb = to_rgb_(*var)
                    result.putpixel((j1, i1), rgb)
    result.save(output_file)
