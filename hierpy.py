#!/usr/bin/env python3

from PIL import Image, ImageDraw

image_size = (100, 100)
offset = (20, 10)
background_color = (255, 255, 255)
foreground_color = (0, 0, 0)
thickness = 10

w = image_size[0]
h = image_size[1]
ox = offset[0]
oy = offset[1]
t = thickness

def DrawA(im):
    draw = ImageDraw.Draw(im)
    # left
    draw.rectangle([(ox, oy), (ox + t, h - oy)], foreground_color)
    # top
    draw.rectangle([(ox, oy), (w - ox, oy + t)], foreground_color)
    # right
    draw.rectangle([(w - ox - t, oy), (w - ox, h - oy)], foreground_color)
    # middle
    draw.rectangle([(ox, h / 2 - t / 2), (w - ox, h / 2 + t / 2)], foreground_color)

if __name__=="__main__":
    im = Image.new('RGB', image_size, background_color)
    DrawA(im)
    im.save('drawing.png')
