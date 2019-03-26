from src.ycbcr import ycbcr2, to_rgb, to_rgb_


def urgb343_(pixels):
    res = [[0 for i in range(512)] for j in range(512)]
    for i in range(512):
        for j in range(512):
            pixel = pixels[i, j]
            r, g, b = pixel
            r = cut(to_binary(r), 3)
            g = cut(to_binary(g), 4)
            b = cut(to_binary(b), 3)
            res[j][i] = [r, g, b]
    return res


def urgb442_(pixels):
    res = [[0 for i in range(512)] for j in range(512)]
    for i in range(512):
        for j in range(512):
            pixel = pixels[i, j]
            r, g, b = pixel
            r = cut(to_binary(r), 4)
            g = cut(to_binary(g), 4)
            b = cut(to_binary(b), 2)
            res[j][i] = [r, g, b]
    return res


def ycbcrq_(pixels, x1, y1, z1):
    res = ycbcr2(pixels)
    for i in range(512):
        for j in range(512):
            y, cb, cr = res[j][i]
            y = cut(to_binary(int(y)), x1)
            cb = cut(to_binary(int(cb)), y1)
            cr = cut(to_binary(int(cr)), z1)
            res[j][i] = to_rgb_(y, cb, cr)
    return res


def to_binary(number):
    number = int(number)
    if number < 0:
        number = 0
    if number > 255:
        number = 255
    bin8 = lambda x: ''.join(reversed([str((x >> i) & 1) for i in range(8)]))
    str_arr = bin8(number)
    num_arr = [int(i) for i in str_arr]
    return num_arr


def cut(bin_arr, count):
    cut_done = bin_arr[:count]
    res = 0
    for i, val in enumerate(cut_done):
        deg = 8 - i - 1
        res += val * 2 ** deg
    return res