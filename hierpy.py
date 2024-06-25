#!/usr/bin/env python3

from PIL import Image, ImageDraw
import numpy as np

image_size = (60, 100)
background_color = (255, 255, 255)
foreground_color = (0, 0, 0)
thickness = (10, 10)

w = image_size[0]
h = image_size[1]
t = thickness

def DrawLeftSegment(im, thickness):
    draw = ImageDraw.Draw(im)
    draw.rectangle([0, 0, thickness[0], im.size[1]], foreground_color)

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
    im = Image.new('RGB', image_size, background_color)
    DrawA(im)
    im.save('drawing.png')
