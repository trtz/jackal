from PIL import Image


class cached_property:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, type):
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res


def median_cut2(image_path, num_colors):
    img = Image.open(image_path)
    quantized = img.quantize(num_colors)
    convert_rgb = quantized.convert('RGB')
    colors = convert_rgb.getcolors(512 * 512)
    color_str = str(sorted(colors, reverse=True))


