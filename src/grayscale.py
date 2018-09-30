from PIL import Image


def grayscale(image_filename, mode=1):
    coefficients = {
        1: (1 / 3, 1 / 3, 1 / 3, 0),
        2: (77 / 256, 150 / 256, 29 / 256, 0)
    }
    curr_coeffs = coefficients[mode]

    img = Image.open(image_filename)
    return img.convert('L', curr_coeffs)