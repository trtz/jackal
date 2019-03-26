import pdb
from operator import itemgetter
# pdb.set_trace()


def get_colors(image):
    colors = image.getcolors(image.size[0] * image.size[1])
    return [c[1] for c in colors]


def median_cut(image, num_colors):
    colors = get_colors(image)
    cubes = [ColorCube(*colors)]
    mapping = {color: cubes[0] for color in colors}
    while len(cubes) < num_colors:
        global_max_size = 0

        for index, cube in enumerate(cubes):
            size = cube.size
            max_size = max(size)
            max_dim = size.index(max_size)

            if max_size > global_max_size:
                global_max_size = max_size
                max_cube = index

        split_box = cubes[max_cube]
        cube_a, cube_b = split_box.split(max_dim, mapping)
        cubes = cubes[:max_cube] + [cube_a, cube_b] + cubes[max_cube + 1:]
    return cubes, mapping


class ColorCube(object):
    rmax = 255.
    rmin = 0.
    gmax = 255.
    gmin = 0.
    bmax = 255.
    bmin = 0.

    def __init__(self, *colors):
        self._colors = colors or []
        self.resize()
        self.colors_ = set(self.colors)

    @property
    def colors(self):
        return self._colors

    @property
    def rsize(self):
        return self.rmax - self.rmin

    @property
    def gsize(self):
        return self.gmax - self.gmin

    @property
    def bsize(self):
        return self.bmax - self.bmin

    @property
    def size(self):
        return self.rsize, self.gsize, self.bsize

    def _average(self, col, length):
        return sum(col) / length

    def color_columns(self):
        return [
            [_[0] for _ in self.colors],
            [_[1] for _ in self.colors],
            [_[2] for _ in self.colors],
        ]

    @property
    def average(self):
        length = len(self.colors)
        cols = self.color_columns()
        r, g, b = [self._average(col, length) for col in cols]
        return int(r), int(g), int(b)

    def resize(self):
        col_r, col_g, col_b = self.color_columns()

        self.rmin = min(col_r)
        self.rmax = max(col_r)
        self.gmin = min(col_g)
        self.gmax = max(col_g)
        self.bmin = min(col_b)
        self.bmax = max(col_b)

    def split(self, axis, mapping):
        self.resize()
        self._colors = sorted(self.colors, key=itemgetter(axis))
        med_idx = len(self.colors) // 2
        left = self.colors[:med_idx]
        right = self.colors[med_idx:]
        cubeleft = ColorCube(*left)
        cuberight = ColorCube(*right)
        for c in left:
            mapping[c] = cubeleft
        for c in right:
            mapping[c] = cuberight
        return (
            cubeleft,
            cuberight)
