import math

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage


def get_greyscale_image(img):
    return np.mean(img[:, :, :2], 2)


def reduce(img, factor):
    result = np.zeros((img.shape[0] // factor, img.shape[1] // factor))
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i, j] = np.mean(img[i * factor:(i + 1) * factor, j * factor:(j + 1) * factor])
    return result


def rotate(img, angle):
    return ndimage.rotate(img, angle, reshape=False)


def flip(img, direction):
    return img[::direction, :]


def apply_transformation(img, direction, angle, contrast=1.0, brightness=0.0):
    return contrast * rotate(flip(img, direction), angle) + brightness


def get_d(X, Y):
    n = X[0].size
    mult = 0
    Xsum = 0
    Ysum = 0
    XSqSum = 0
    for i in range(n):
        for j in range(n):
            curr_x = X[i, j]
            curr_y = Y[i, j]
            mult += curr_x * curr_x
            Xsum += curr_x
            Ysum += curr_y
            XSqSum += curr_x ** 2
    lambda_ = (mult * n ** 2 - Xsum * Ysum) / (XSqSum * n ** 2 - Xsum ** 2 + 0.0001)
    tau = (XSqSum * Ysum - mult * Xsum) / (XSqSum * n ** 2 - Xsum ** 2 + 0.0001)
    res = Y - (lambda_ * X + tau)
    curr = 0
    for i in range(n):
        for j in range(n):
            curr += res[i, j] ** 2
    return curr


def get_contr_br(D, S):
    A = np.concatenate((np.ones((S.size, 1)), np.reshape(S, (S.size, 1))), axis=1)
    b = np.reshape(D, (D.size,))
    x, _, _, _ = np.linalg.lstsq(A, b)
    return x[1], x[0]


def get_all_transf_blocks(img, source_size, destination_size, step):
    factor = source_size // destination_size
    transformed_blocks = []
    for k in range((img.shape[0] - source_size) // step + 1):
        for l in range((img.shape[1] - source_size) // step + 1):
            S = reduce(img[k * step:k * step + source_size, l * step:l * step + source_size], factor)
            for direction, angle in candidates:
                transformed_blocks.append((k, l, direction, angle, apply_transformation(S, direction, angle)))
    return transformed_blocks


def compress(img, source_size, destination_size, step):
    transformations = []
    transformed_blocks = get_all_transf_blocks(img, source_size, destination_size, step)
    for i in range(img.shape[0] // destination_size):
        transformations.append([])
        for j in range(img.shape[1] // destination_size):
            print(i, j)
            transformations[i].append(None)
            min_d = float('inf')
            D = img[i * destination_size:(i + 1) * destination_size, j * destination_size:(j + 1) * destination_size]
            for k, l, direction, angle, S in transformed_blocks:
                contr, br = get_contr_br(D, S)
                d = get_d(S, D)

                if d < min_d:
                    min_d = d
                    transformations[i][j] = (k, l, direction, angle, contr, br)
    return transformations


def decomp(transformations, source_size, destination_size, step, nb_iter=8):
    factor = source_size // destination_size
    height = len(transformations) * destination_size
    width = len(transformations[0]) * destination_size
    img = mpimg.imread('images/64x64.bmp')
    img = get_greyscale_image(img)
    iterations = [img]
    cur_img = np.zeros((height, width))
    for i_iter in range(nb_iter):
        print(i_iter)
        for i in range(len(transformations)):
            for j in range(len(transformations[i])):
                k, l, flip, angle, contrast, brightness = transformations[i][j]
                S = reduce(iterations[-1][k * step:k * step + source_size, l * step:l * step + source_size], factor)
                D = apply_transformation(S, flip, angle, contrast, brightness)
                cur_img[i * destination_size:(i + 1) * destination_size,
                j * destination_size:(j + 1) * destination_size] = D
        iterations.append(cur_img)
        cur_img = np.zeros((height, width))
    return iterations


def plot_iterations(iterations):
    plt.figure()
    nb_row = math.ceil(np.sqrt(len(iterations)))
    nb_cols = nb_row
    for i, img in enumerate(iterations):
        plt.subplot(nb_row, nb_cols, i + 1)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='none')
        frame = plt.gca()
        frame.axes.get_xaxis().set_visible(False)
        frame.axes.get_yaxis().set_visible(False)
    plt.tight_layout()


directions = [1, -1]
angles = [0, 90, 180, 270]
candidates = [(dir_, angle) for dir_ in directions for angle in angles]


def main2():
    img = mpimg.imread('images/2.bmp')
    img = get_greyscale_image(img)
    transformations = compress(img, 16, 8, 16)
    iterations = decomp(transformations, 16, 8, 16, 10)
    plot_iterations(iterations)
    plt.show()


if __name__ == '__main__':
    main2()
