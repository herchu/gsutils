import sys
import os
from PIL import Image, ImageFilter

def rgb_to_gobstones(r, g, b, k=0):
    a = []
    if r > 0:
        a.append('Rojo {}'.format(r))
    if g > 0:
        a.append('Verde {}'.format(g))
    if b > 0:
        a.append('Azul {}'.format(b))
    if k > 0:
        a.append('Negro {}'.format(k))
    return ' '.join(a)


def rgb_palette(max=3):
    level = max
    colors = [  # primary and secondary colors (by channel)
        [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1]
    ]
    color_ix = 0
    yield (0, 0, 0)  # black first
    while level > 0:
        c = colors[color_ix]
        yield (c[0] * level, c[1] * level, c[2] * level)
        color_ix += 1
        if color_ix >= len(colors):
            color_ix = 0
            level -= 1


def downsample(pixel, bpp):
    """
    """
    r, g, b = pixel
    sh = 8 - bpp
    return (r >> sh, g >> sh, b >> sh)


def build_pixel_line(x, y, r, g, b, k):
    return 'cell {} {} {}\n'.format(x, y, rgb_to_gobstones(r, g, b, k))


def calc_size(w, h, maxw=0, maxh=0):
    sizes = []
    if maxw and maxw < w:
        wpercent = (maxw / float(w))
        hsize = int((float(h) * float(wpercent)))
        sizes.append((maxw, hsize))
    if maxh and maxh < h:
        hpercent = (maxh / float(h))
        wsize = int((float(w) * float(hpercent)))
        sizes.append((wsize, maxh))
    for (w1, h1) in sizes:
        if h1 < h or w1 < w:
            w = w1
            h = h1
    return (w, h)

def write_image(
    img, filename='board.gbb', name='Board', row_offset=0, col_offset=0, bpp=2
):
    w = img.width
    h = img.height
    print("Generating board with {}+{} rows, {} cols ".format(
        img.height, row_offset, img.width
    ))
    with open(filename, 'wt') as file_out:
        file_out.write('GBB/1.0\n')
        file_out.write('size {} {}\n'.format(w + col_offset, h + row_offset))
        palette_gen = rgb_palette((1 << bpp) - 1)
        for y in range(row_offset):
            for x in range(w + col_offset):
                if y == row_offset - 1:  # top row: palette
                    try:
                        (r, g, b) = next(palette_gen)
                    except StopIteration:
                        (r, g, b) = (0, 0, 0)
                else:
                    (r, g, b) = (0, 0, 0)
                file_out.write(build_pixel_line(x, h + y, r, g, b, 1))
        for y in range(h):
            for x in range(w):
                r, g, b = downsample(img.getpixel((x, y)), bpp)
                if r + g + b > 0:  # skips pure black points
                    file_out.write(build_pixel_line(
                        x + col_offset,
                        h - y - 1,
                        r, g, b, 0
                    ))
        file_out.write('head 0 0\n')

# Parse command line arguments - TODO: use argparse
if len(sys.argv) != 3:
    print("Usage: im2board <in_image_file> <out_board_file>")
    sys.exit(1)
img_filename = sys.argv[1]
out_filename = sys.argv[2]

# Load image
im = Image.open(img_filename)
print("Loaded image {}, size {}*{}".format(img_filename, im.width, im.height))
# Resize to max gobstones board size, if necessary
(smallw, smallh) = calc_size(im.width, im.height, 30, 28)
if (smallw, smallh) != (im.width, im.height):
    # resize image
    print("Image too big, resizing to {}*{}".format(smallw, smallh))
    im = im.resize((smallw, smallh), Image.BILINEAR)
im = im.convert('RGB')
# Turn into board
write_image(im, out_filename, row_offset=2, name="Board")
