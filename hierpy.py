#!/usr/bin/env python3

from PIL import Image, ImageDraw

if __name__=="__main__":
    im = Image.new('RGB', (100, 100), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    # draw an "A"
    # left
    draw.line([(20, 90), (20, 6)], (0, 0, 0), 10)
    # top
    draw.line([(20, 10), (80, 10)], (0, 0, 0), 10)
    # right
    draw.line([(80, 6), (80, 90)], (0, 0, 0), 10)
    # middle
    draw.line([(20, 50), (80, 50)], (0, 0, 0), 10)
    im.save('drawing.png')
