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

    def DrawBoundingBoxes(self, rect):
        if len(rect.shape) == 3 and rect.shape[2] == 4:
            for col in range(rect.shape[0]):
                for row in range(rect.shape[1]):
                    self.DrawBoundingBox(rect[col, row, :])
        elif len(rect.shape) == 2 and rect.shape[1] == 4:
            for i in range(rect.shape[0]):
                self.DrawBoundingBox(rect[i, :])
        elif len(rect.shape) == 1 and rect.shape == 4:
            self.DrawBoundingBox(rect)
        else:
            print("Unknown rect argument: must have 1-3 dimensions with the last one length 4")

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

class HierPySmallLetter:
    def __init__(self, letter):
        self.letter = None
        self.SetLetter(letter)

    def SetLetter(self, letter):
        self.letter = letter

class HierPy:
    def __init__(self, large_letter, small_letter):
        self.large_letter = large_letter
        self.small_letter = HierPySmallLetter(small_letter)
        self.Setup()

    def Setup(self):
        self.SetupGrid()

    def Letters(self):
        return self.large_letter, self.small_letter

    def ComputeSpacingAndOffset(self, display_size, object_size, n_objects):
        """offset, spacing = ComputeSpacingAndOffset(display_size, object_size, n_objects)

        Computes and returns the offset (external border) between rects
        and the spacing (space between rects)
        """

        offset = np.ceil(object_size / 2.0)
        spacing = ((display_size - 2 * offset - n_objects * object_size) /
                   (n_objects - 1))
        return offset, spacing

    def SetupGrid(self, letter):
        self.grid = self.MakeGrid()
        print(self.grid)
        pd = PillowDrawer("drawing.png", large_size)
        pd.DrawBoundingBoxes(self.grid)
        pd.Save()

    def MakeGrid(self):
        """MakeGrid(self)

        Creates an equally spaced grid
        """
        lw, lh = large_size
        sw, sh = np.array(large_size) * np.array(small_size)
        nx, ny = large_layout
        offset_x, spacing_x = self.ComputeSpacingAndOffset(lw, sw, nx)
        offset_y, spacing_y = self.ComputeSpacingAndOffset(lh, sh, ny)

        print(offset_x, spacing_x)
        print(offset_x * 2 + nx * sw + (nx - 1) * spacing_x)

        grid = np.zeros((nx, ny, 4), dtype=np.int_)
        for col in range(nx):
            for row in range(ny):
                grid[col, row, :] = [
                    offset_x + (sw + spacing_x) * col,
                    offset_y + (sh + spacing_y) * row,
                    offset_x + (sw + spacing_x) * col + sw,
                    offset_y + (sh + spacing_y) * row + sh]
        return grid

    def Draw(self, large_letter, small_letter):
        print('drawing a "{}" composed of "{}"s'.format(large_letter, small_letter))

if __name__=="__main__":
    letter = HierPy("A", "E")
