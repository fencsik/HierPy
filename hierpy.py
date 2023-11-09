#!/usr/bin/env python3

from PIL import Image, ImageDraw

if __name__=="__main__":
    im = Image.new('RGB', (100, 100), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    # draw an "A"
    # left
    draw.rectangle([(15, 5), (25, 90)], (0, 0, 0))
    # top
    draw.rectangle([(15, 5), (85, 15)], (0, 0, 0))
    # right
    draw.rectangle([(75, 15), (85, 90)], (0, 0, 0))
    # middle
    draw.rectangle([(15, 45), (85, 55)], (0, 0, 0))
    im.save('drawing.png')
