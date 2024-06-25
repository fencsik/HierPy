#!/usr/bin/env python3

from PIL import Image, ImageDraw
import numpy as np

large_size = (300, 500) # (x, y) in pixels
small_size = (.1, .1) # proportion relative to large_size
large_layout = (3, 5) # composition of large letters (x, y)

small_thickness = (10, 10)
background_color = (255, 255, 255)
foreground_color = (0, 0, 0)


class PillowDrawer:
    """
    Class for drawing using Pillow
    """

    def __init__(self, filename, size):
        self.filename = filename
        self.image = Image.new('RGB', size, background_color)
        self.win = ImageDraw.Draw(self.image)

    def Save(self):
        self.image.save(self.filename)

    def DrawBoundingBox(self, rect):
        if isinstance(rect, np.ndarray):
            rect = rect.tolist()
        self.win.rectangle(rect, outline=foreground_color, width=1)

    def DrawDot(self, rect, radius):
        """Draws a dot in the center of the rect with given radius and fill color"""
        x = (rect[2] - rect[0]) / 2
        y = (rect[3] - rect[1]) / 2
        self.win.ellipse([x - radius, y - radius, x + radius, y + radius],
                             foreground_color)

    def DrawLeftSegment(self, rect):
        self.win.rectangle([rect[0], rect[1],
                            rect[0] + small_thickness[0], rect[3]],
                           foreground_color)

def DrawTopSegment(im, thickness):
    draw = ImageDraw.Draw(im)
    draw.rectangle([0, 0, im.size[0], thickness[1]], foreground_color)

def DrawRightSegment(im, thickness):
    w, h = im.size
    draw = ImageDraw.Draw(im)
    draw.rectangle([w - thickness[0], 0, w, h], foreground_color)

def DrawCenterHorizontalSegment(im, thickness):
    w, h = im.size
    mid = round(h / 2.0)
    t = round(thickness[1] / 2.0)
    draw = ImageDraw.Draw(im)
    draw.rectangle([0, mid - t, w, mid + t - 1], foreground_color)

def DrawA(im):
    DrawLeftSegment(im, thickness)
    DrawRightSegment(im, thickness)
    DrawTopSegment(im, thickness)
    DrawCenterHorizontalSegment(im, thickness)

if __name__=="__main__":
    try:
        small_size = np.array(large_size) * np.array(small_size)
        large_rect = np.array([0, 0, large_size[0], large_size[1]])
        small_rect = np.array([0, 0, small_size[0], small_size[1]]) + \
          np.array([50, 100, 50, 100])
        pd = PillowDrawer("drawing.png", large_size)
        pd.DrawDot(large_rect, 5)
        print(small_rect)
        pd.DrawBoundingBox(small_rect.tolist())
        pd.Save()
    except NotImplementedError:
        print("call to non implemented function")
