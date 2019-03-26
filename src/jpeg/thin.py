from PIL import Image

from src.load import RIGHT
from src.ycbcr import ycbcr2, to_rgb_


def thin_1(image, yv, yh, crv, crh, cbv, cbh, output):
    res = Image.new("RGB", (512, 512))
    ycbcr_image = ycbcr2(image)
    for i in range(512):
        for j in range(512):
            if not (i % yv == 0 and j % yh == 0):
                closest_i = i // yv * yv
                closest_j = j // yh * yh
                ycbcr_image[j][i][0] = ycbcr_image[closest_j][closest_i][0]
            if not (i % crv == 0 and j % crh == 0):
                closest_i = i // crv * crv
                closest_j = j // crh * crh
                ycbcr_image[j][i][1] = ycbcr_image[closest_j][closest_i][1]
            if not (i % cbv == 0 and j % cbh == 0):
                closest_i = i // cbv * cbv
                closest_j = j // cbh * cbh
                ycbcr_image[j][i][2] = ycbcr_image[closest_j][closest_i][2]
            res.putpixel((i, j), to_rgb_(*ycbcr_image[j][i]))
    res.save(output)

