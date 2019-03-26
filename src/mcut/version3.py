import cv2
from sklearn.cluster import MiniBatchKMeans


def median_cut3(path, colors):
    image = cv2.imread(path)
    (h, w) = image.shape[:2]

    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    image = image.reshape((image.shape[0] * image.shape[1], 3))

    clt = MiniBatchKMeans(n_clusters=colors)
    labels = clt.fit_predict(image)
    quant = clt.cluster_centers_.astype("uint8")[labels]

    quant = quant.reshape((h, w, 3))
    image = image.reshape((h, w, 3))

    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

    res = [[[] for i in range(512)] for j in range(512)]
    for i in range(512):
        for j in range(512):
            pixel = quant[i, j]
            res[i][j] = [pixel[2], pixel[1], pixel[0]]
    return res