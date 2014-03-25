__author__ = 'Zhenyu'

import Image
import ImageDraw
import ImageFont


def draw_rectangle(pic, rects, ids=None):
    """
    Draw rectangles on a picture.
    pic is the file path of the picture.
    rects contain an array of rect.
    rect contains four arguments:
        origin: x, y
        size: width, height
    """
    im = Image.open(pic)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("utilities/arial.ttf", 24)

    id = 0
    for rect in rects:
        l = []
        l.append((rect[0], rect[1], rect[0] + rect[2], rect[1]))
        l.append((rect[0], rect[1], rect[0], rect[1] + rect[3]))
        l.append((rect[0] + rect[2], rect[1], rect[0] + rect[2], rect[1] + rect[3]))
        l.append((rect[0], rect[1] + rect[3], rect[0] + rect[2], rect[1] + rect[3]))
        for line in l:
            draw.line(line, width=3, fill=(255, 100, 100))

        txt = str(ids[id]) if ids else str(id)
        draw.text((rect[0] + 8, rect[1] + 8), txt, fill=(255, 100, 100), font=font)
        id += 1

    im.show()
    fs = pic.split('.')
    pic = fs[0] + 'm.png'
    im.save(pic, 'PNG')


def mark_nodes(pic, nodes, ids=None):
    """
    node:
        contains "rect" field
    """

    if not isinstance(nodes, list):
        nodes = [nodes]

    rects = []
    for node in nodes:
        rect = []
        rect.append(node['rect']['origin']['x'])
        rect.append(node['rect']['origin']['y'])
        rect.append(node['rect']['size']['width'])
        rect.append(node['rect']['size']['height'])
        rects.append(rect)
    draw_rectangle(pic, rects, ids)


def get_crop_of_element(pic, node):
    im = Image.open(pic)
    rect = (
        node['rect']['origin']['x'],
        node['rect']['origin']['y'],
        node['rect']['origin']['x'] + node['rect']['size']['width'],
        node['rect']['origin']['y'] + node['rect']['size']['height']
    )
    im1 = im.crop(rect)
    im1.show()


def resize(pic, size):
    im = Image.open(pic)
    scale = im.size[0] / size[0]
    size = (im.size[0] / scale, im.size[1] / scale)
    im2 = im.resize(size)
    im2.save(pic, 'PNG')


if __name__ == '__main__':
    pic = "1392109537.png"
    n = {
        'rect': {"origin": {
            "x": 280,
            "y": 985
        },
                 "size": {
                     "height": 119,
                     "width": 160
                 }
        }}
    mark_nodes(pic, n)

