import math

import numpy as np


def nync2(flatteny, flattencb, flattencr, ny, nc):
    sorted_y = sorted(flatteny, key=lambda item: -item)
    sorted_cb = sorted(flattencb, key=lambda item: -item)
    sorted_cr = sorted(flattencr, key=lambda item: -item)
    return list(sorted_y)[:ny], list(sorted_cb)[:nc], list(sorted_cr)[:nc]


def nync_(image_arr, ny, nc):
    result = [[[0, 0, 0] for _ in range(512)] for _ in range(512)]
    for i in range(0, 512, 8):
        for j in range(0, 512, 8):
            ys_ = []
            cbs_ = []
            cbr_ = []
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    ys_.append(image_arr[j1][i1][0])
                    cbs_.append(image_arr[j1][i1][1])
                    cbr_.append(image_arr[j1][i1][2])

            ys, cbs, crs = nync2(ys_, cbs_, cbr_, ny, nc)
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    y, cb, cr = image_arr[j1][i1]
                    pixel = [0, 0, 0]
                    if y in ys:
                        pixel[0] = y
                    if cb in cbs:
                        pixel[1] = cb
                    if cr in crs:
                        pixel[2] = cr
                    result[j1][i1] = pixel
    return result


def get_q_p():
    q = np.zeros((8, 8))

    p = np.full((8, 8), 99)

    for i in range(0, 8):
        for j in range(0, 8):
            q[i][j] = 4 + math.ceil(15 / 2 * (i + j))
    q[0][0] = 16
    q[7][7] = 97

    for i in range(0, 8):
        for j in range(0, 7 - i):
            p[i][j] = 2 + 16 * (i + j)

    return q, p


def matrix_comp(image_arr, factor, inverse=False):
    q, p = get_q_p()
    q = factor * q
    p = factor * p
    result = [[[0, 0, 0] for _ in range(512)] for _ in range(512)]
    for i in range(0, 512, 8):
        for j in range(0, 512, 8):
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    y, cb, cr = image_arr[j1][i1]
                    if inverse:
                        y = y * q[i1 - i, j1 - j]
                        cb = cb * p[i1 - i, j1 - j]
                        cr = cr * p[i1 - i, j1 - j]
                    else:
                        y = y / q[i1 - i, j1 - j]
                        cb = cb / p[i1 - i, j1 - j]
                        cr = cr / p[i1 - i, j1 - j]
                    result[j1][i1] = [y, cb, cr]
    return result


def get_standart_matrices():
    p = np.full((8, 8), 99)

    p[0][0] = 17
    p[0][1] = p[1][0] = 18
    p[0][2] = p[2][0] = 24
    p[0][3] = p[3][0] = 47
    p[1][1] = 21
    p[1][2] = p[2][1] = 26
    p[2][2] = 56

    q = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]])

    return q, p


def standart_matrix_comp(image_arr, factor, inverse=False):
    q, p = get_standart_matrices()
    q = factor * q
    p = factor * p
    result = [[[0, 0, 0] for _ in range(512)] for _ in range(512)]
    for i in range(0, 512, 8):
        for j in range(0, 512, 8):
            for i1 in range(i, i + 8):
                for j1 in range(j, j + 8):
                    y, cb, cr = image_arr[j1][i1]
                    if inverse:
                        y = y * q[i1 - i, j1 - j]
                        cb = cb * p[i1 - i, j1 - j]
                        cr = cr * p[i1 - i, j1 - j]
                    else:
                        y = y / q[i1 - i, j1 - j]
                        cb = cb / p[i1 - i, j1 - j]
                        cr = cr / p[i1 - i, j1 - j]
                    result[j1][i1] = [y, cb, cr]
    return result
