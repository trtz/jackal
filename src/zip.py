import gzip
import pickle

import numpy as np


def zig_zag(input_matrix, block_size, getter):
    z = np.empty([block_size * block_size])
    index = -1
    for i in range(0, 2 * block_size - 1):
        if i < block_size:
            bound = 0
        else:
            bound = i - block_size + 1
        for j in range(bound, i - bound + 1):
            index += 1
            if i % 2 == 1:
                z[index] = getter(input_matrix, j, i - j)
            else:
                z[index] = getter(input_matrix, i - j, j)
    return z


def un_zig_zag(array, block_size):
    output_matrix = np.zeros((block_size, block_size))
    index = -1
    for i in range(0, 2 * block_size - 1):
        if i < block_size:
            bound = 0
        else:
            bound = i - block_size + 1
        for j in range(bound, i - bound + 1):
            index += 1
            if i % 2 == 1:
                output_matrix[j][i - j] = array[index]
            else:
                output_matrix[i - j][j] = array[index]
    return output_matrix


def decompress(fn, output_file):
    inF = gzip.GzipFile(fn, 'rb')
    s = inF.read()
    inF.close()

    outF = open(output_file, 'wb')
    outF.write(s)
    outF.close()


def compress(fn, output_file):
    inF = open(fn, 'rb')
    s = inF.read()
    inF.close()

    outF = gzip.GzipFile(output_file, 'wb')
    outF.write(s)
    outF.close()


def save_to_file(arr, output_file):
    with open(output_file, 'wb') as f:
        pickle.dump(arr, f)


def load_from_file(output_file):
    return pickle.load(open(output_file, 'rb'))


def get_3array(arr1, arr2, arr3):
    res1 = un_zig_zag(arr1, 512)
    res2 = un_zig_zag(arr2, 512)
    res3 = un_zig_zag(arr3, 512)
    res = [[[0, 0, 0] for i in range(512)] for j in range(512)]
    for i in range(512):
        for j in range(512):
            res[i][j][0] = res1[i][j]
            res[i][j][1] = res2[i][j]
            res[i][j][2] = res3[i][j]
    return res
