import PIL

from src.load import RIGHT
from src.quantizer.lib.dithering.dithering import dithering
from src.quantizer.lib.image_db import ImageDB
from src.quantizer.lib.palette.median_cut import MedianCut


def median_cut3(image_path, num_colors):
    image = ImageDB(image_path)
    palette = MedianCut(image, 'luma')
    new_image = PIL.Image.new("P", (image.x, image.y))
    new_image.putpalette(palette.chain)
    pixels = new_image.load()
    dith = dithering(image, 'none', False)
    for x, y, color in image:
        index = palette.match(color)
        pixels[x, y] = index
        dith(x, y, palette[index])
    path = RIGHT
    new_image.save(path)
