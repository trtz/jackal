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


def to_binary(number):
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