#!/usr/bin/env python3

from PIL import Image, ImageDraw
import numpy as np

large_size = (300, 500) # (x, y) in pixels
small_size = (.1 * np.array(large_size)).astype(int).tolist() # define relatively
#small_size = (30, 30) # define absolutely
large_layout = (3, 5) # composition of large letters (x, y)

small_thickness = (10, 10)
background_color = (255, 255, 255)
foreground_color = (0, 0, 0)


class PillowDrawer:
    """
    Class for drawing using Pillow
    """

    def __init__(self, size):
        self.image = Image.new('RGB', size, background_color)
        self.win = ImageDraw.Draw(self.image)

    def Save(self, filename):
        self.image.save(filename)

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

class GridDrawer:
    """Grid Drawer class

    Class for "drawing" into a global grid. That is, selecting the grid
    locations that should be included for a particular segment of a
    global letter.
    """

    def __init__(self, size):
        self.x, self.y = size
        self.grid = np.zeros((self.x, self.y), dtype=bool)

    def DrawLeftSegment(self):
        self.grid[0, :] = True

    def DrawTopSegment(self):
        self.grid[:, 0] = True

    def DrawBottomSegment(self):
        self.grid[:, -1] = True

    def DrawMiddleSegment(self):
        self.grid[:, np.floor(self.y/2.0).astype(int)] = True

    def Grid(self):
        return self.grid

class HierPySmallLetter:
    def __init__(self, letter):
        self.SetLetter(letter)

    def SetLetter(self, letter):
        self.letter = letter

    def Letter(self):
        return self.letter

class HierPy:
    def __init__(self, large_letter, small_letter):
        self.large_letter = large_letter
        self.small_letter = HierPySmallLetter(small_letter)
        self.Setup()

    def Setup(self):
        self.SetupGrid()

    def Letters(self):
        return self.Letter(), self.small_letter.Letter()

    def Letter(self):
        return self.large_letter

    def ComputeSpacingAndOffset(self, display_size, object_size, n_objects):
        """offset, spacing = ComputeSpacingAndOffset(display_size, object_size, n_objects)

        Computes and returns the offset (external border) between rects
        and the spacing (space between rects)
        """

        offset = np.ceil(object_size / 2.0)
        spacing = ((display_size - 2 * offset - n_objects * object_size) /
                   (n_objects - 1))
        return offset, spacing

    def SetupGrid(self):
        self.master_grid = self.MakeGrid()
        self.letter_grid = self.SetLetterGrid()
        print(self.letter_grid)
        pd = PillowDrawer(large_size)
        pd.DrawBoundingBoxes(self.master_grid[self.letter_grid])
        pd.Save("drawing.png")

    def MakeGrid(self):
        """MakeGrid(self)

        Creates an equally spaced grid
        """
        lw, lh = large_size
        sw, sh = small_size
        nx, ny = large_layout
        offset_x, spacing_x = self.ComputeSpacingAndOffset(lw, sw, nx)
        offset_y, spacing_y = self.ComputeSpacingAndOffset(lh, sh, ny)

        grid = np.zeros((nx, ny, 4), dtype=np.int_)
        for col in range(nx):
            for row in range(ny):
                grid[col, row, :] = [
                    offset_x + (sw + spacing_x) * col,
                    offset_y + (sh + spacing_y) * row,
                    offset_x + (sw + spacing_x) * col + sw,
                    offset_y + (sh + spacing_y) * row + sh]
        return grid

    def SetLetterGrid(self):
        gd = GridDrawer(large_layout)
        gd.DrawLeftSegment()
        gd.DrawTopSegment()
        gd.DrawMiddleSegment()
        gd.DrawBottomSegment()
        return gd.Grid()

    def Draw(self, large_letter, small_letter):
        print('drawing a "{}" composed of "{}"s'.format(large_letter, small_letter))

if __name__=="__main__":
    letter = HierPy("A", "E")
