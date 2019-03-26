from math import log

import cv2
import numpy as np
from scipy.cluster.vq import vq, kmeans

from src.load import RIGHT
from src.ycbcr import save_arr_to_right


def get_centroids(c, p):
    final_centroids = np.copy(c)
    for centroid in c:
        final_centroids = np.vstack((final_centroids, np.add(centroid, p)))
    return final_centroids


def gla1(image_location, colors):
    image = cv2.imread(image_location, cv2.IMREAD_COLOR)
    image_height = len(image)
    image_width = len(image[0])
    block_width = 1
    block_height = 1
    vector_dimension = block_width * block_height

    codebook_size = colors
    perturbation_vector = np.full(vector_dimension, 10)

    image_vectors = []
    for i in range(0, image_width):
        for j in range(0, image_height):
            image_vectors.append(image[i, j])
    image_vectors = np.asarray(image_vectors).astype(float)

    centroid_vector = np.mean(image_vectors, axis=0)
    centroids = np.vstack((centroid_vector, np.add(centroid_vector, perturbation_vector)))
    reconstruction_values, distortion = kmeans(image_vectors, centroids)

    for i in range(0, int(log(codebook_size / 2, 2)), 1):
        reconstruction_values = get_centroids(reconstruction_values, perturbation_vector)
        reconstruction_values, distortion = kmeans(image_vectors, reconstruction_values, 1)

    print('reconstruction values finished')

    image_vector_indices, distance = vq(image_vectors, reconstruction_values)

    image_after_compression = np.zeros([image_width, image_height], dtype="uint8")
    res = [[[] for i in range(512)] for j in range(512)]
    for index, image_vector in enumerate(image_vectors):
        start_row = int(index / (image_width / block_width)) * block_height
        end_row = start_row + block_height
        start_column = (index * block_width) % image_width
        end_column = start_column + block_width
        b, g, r = list(reconstruction_values[image_vector_indices[index]])
        res[start_row][start_column] = [r, g, b]
    output_image_name = RIGHT
    save_arr_to_right(res)
