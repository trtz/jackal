import os

from PIL import Image

from src.dct import dct1, idct
from src.jpeg.compression import matrix_comp
from src.jpeg.thin import thin_1
from src.psnr import psnr as psnr12
from src.zip import zig_zag, save_to_file, compress, decompress, load_from_file, get_3array


def main():
    source = 'images/image_Baboon512rgb.png'
    result = source + '.result.png'
    zigzagged = source + '.dat'
    compressed = zigzagged + '.gz'
    uncompressed = compressed + '.uncompressed'

    img = Image.open(source).load()
    print('dct done')

    thinned_fn = source + 'th.png'

    thin_1(img, 1, 1, 1, 1, 1, 1, thinned_fn)
    print('thin done')

    img = Image.open(thinned_fn).load()
    dct = dct1(img)
    step = dct

    step1 = matrix_comp(step, 1.0)

    step = step1

    zz = [
        zig_zag(step, 512, lambda inp, x, y: inp[x][y][0]),
        zig_zag(step, 512, lambda inp, x, y: inp[x][y][1]),
        zig_zag(step, 512, lambda inp, x, y: inp[x][y][2]),
    ]
    save_to_file(zz, zigzagged)

    compress(zigzagged, compressed)
    decompress(compressed, uncompressed)

    print_size(uncompressed)
    print_size(compressed)

    loaded = load_from_file(uncompressed)
    loaded2 = get_3array(*loaded)
    loaded3 = matrix_comp(loaded2, 1.0, True)
    idct(loaded3, result)

    psnr = psnr12(source, result)
    print('psnr ' + str(psnr))


def print_size(fn):
    print(fn + ' ' + str(os.path.getsize(fn)))


if __name__ == '__main__':
    main()
