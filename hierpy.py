#!/usr/bin/env python3

from PIL import Image, ImageDraw
import numpy as np
import os

letters_to_draw = ["A", "C", "E", "F", "H", "L", "M", "N",
                   "P", "S", "T", "U", "X", "Y", "Z"]
directory = "stim"
file_suffix = "-black"

large_size = (190, 250) # (x, y) in pixels
#small_size = (.1 * np.array(large_size)).astype(int).tolist() # define relatively
small_size = (28, 36) # define absolutely
large_layout = (5, 5) # composition of large letters (x, y)

small_thickness = (4, 4)
background_color = tuple([150] * 3)
foreground_color = tuple([0] * 3)

diagonal_offset = 1

rng = np.random.default_rng()

class PillowDrawer:
    """
    Class for drawing using Pillow
    """

    def __init__(self, size):
        # extract/compute values needed for drawing operations
        self.ht, self.vt = small_thickness
        self.ht -= 1
        self.vt -= 1
        self.halfht = int(self.ht / 2.)
        self.halfvt = int(self.vt / 2.)
        self.hmidpoint = int(size[0] / 2.)
        self.vmidpoint = int(size[1] / 2.)
        self.do = diagonal_offset
        self.fg = foreground_color
        self.bg = background_color

        self.image = Image.new('RGB', size, self.bg)
        self.bbox = self.image.getbbox(alpha_only = False)
        self.rect = (np.array(self.bbox) - np.array([0, 0, 1, 1])).tolist()
        self.draw = ImageDraw.Draw(self.image)

    def Save(self, filename):
        self.image.save(filename)

    def Reset(self):
        self.draw.rectangle(self.rect, fill=self.bg)

    def Fill(self):
        self.draw.rectangle(self.rect, fill=self.fg)

    def GetImage(self):
        return self.image

    def Place(self, im, locations):
        """Place(image, locations)

        Place the image im into specified location(s) in this image. The
        im argument must be a structure that has the function GetImage()
        to get a Pillow image. The locations can be a ROW x COLUMN x 4
        numpy array, a N x 4 numpy array, or an array/list with 4
        values.
        """

        if isinstance(locations, (list, tuple, np.ndarray)) and len(locations) == 4:
            self.image.paste(im.GetImage(), locations)
        elif len(locations.shape) == 3 and locations.shape[2] == 4:
            for col in range(locations.shape[0]):
                for row in range(locations.shape[1]):
                    self.image.paste(im.GetImage(), locations[col, row, :])
        elif len(locations.shape) == 2 and locations.shape[1] == 4:
            for i in range(locations.shape[0]):
                self.image.paste(im.GetImage(), locations[i, :])
        elif len(locations.shape) == 1 and locations.shape == 4:
            self.image.paste(im.GetImage(), locations)
        else:
            print("Unknown rect argument: must have 1-3 dimensions with the last one length 4")

    def DrawBoundingBox(self):
        self.draw.rectangle(self.rect, outline=self.fg, width=1)

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
        self.draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                             self.fg)

    def DrawLeftSegment(self):
        self.draw.rectangle([self.rect[0], self.rect[1],
                             self.rect[0] + self.ht, self.rect[3]],
                           fill=self.fg)

    def DrawUpperLeftSegment(self):
        self.draw.rectangle([self.rect[0], self.rect[1],
                             self.rect[0] + self.ht, self.vmidpoint],
                            fill=self.fg)

    def DrawLowerLeftSegment(self):
        self.draw.rectangle([self.rect[0], self.vmidpoint,
                             self.rect[0] + self.ht, self.rect[3]],
                            fill=self.fg)

    def DrawRightSegment(self):
        self.draw.rectangle([self.rect[2] - self.ht, self.rect[1],
                             self.rect[2], self.rect[3]],
                            fill=self.fg)

    def DrawUpperRightSegment(self):
        self.draw.rectangle([self.rect[2] - self.ht, self.rect[1],
                             self.rect[2], self.vmidpoint],
                            fill=self.fg)

    def DrawLowerRightSegment(self):
        self.draw.rectangle([self.rect[2] - self.ht, self.vmidpoint,
                             self.rect[2], self.rect[3]],
                            fill=self.fg)

    def DrawTopSegment(self):
        self.draw.rectangle([self.rect[0], self.rect[1],
                             self.rect[2], self.rect[1] + self.vt],
                            fill=self.fg)

    def DrawBottomSegment(self):
        self.draw.rectangle([self.rect[0], self.rect[3] - self.vt,
                             self.rect[2], self.rect[3]],
                            fill=self.fg)

    def DrawHorizontalCenterSegment(self):
        self.draw.rectangle([self.rect[0], self.vmidpoint - self.halfvt - 1,
                             self.rect[2], self.vmidpoint + self.halfvt],
                            fill=self.fg)

    def DrawVerticalCenterSegment(self):
        self.draw.rectangle([self.hmidpoint - self.halfht - 1, self.rect[1],
                             self.hmidpoint + self.halfht, self.rect[3]],
                            fill=self.fg)

    def DrawLowerVerticalCenterSegment(self):
        self.draw.rectangle([self.hmidpoint - self.halfht - 1, self.vmidpoint - 1,
                             self.hmidpoint + self.halfht, self.rect[3]],
                            fill=self.fg)

    def DrawLeftDiagonal(self):
        self.draw.polygon([(self.rect[0], self.rect[1]),
                           (self.rect[0] + self.halfht + self.do, self.rect[1]),
                           (self.rect[2], self.rect[3] - self.halfvt - self.do),
                           (self.rect[2], self.rect[3]),
                           (self.rect[2] - self.halfht - self.do, self.rect[3]),
                            (self.rect[0], self.rect[1] + self.halfvt + self.do)],
                          fill=self.fg)

    def DrawLeftDiagonalHorizontal(self):
        self.draw.polygon([(self.rect[0], self.rect[1]),
                           (self.rect[2] - self.ht - self.do, self.rect[3]),
                           (self.rect[2], self.rect[3]),
                           (self.rect[0] + self.ht + self.do, self.rect[1])],
                          fill=self.fg)

    def DrawRightDiagonal(self):
        self.draw.polygon([(self.rect[2], self.rect[1]),
                           (self.rect[2], self.rect[1] + self.halfvt + self.do),
                           (self.rect[0] + self.halfht + self.do, self.rect[3]),
                           (self.rect[0], self.rect[3]),
                           (self.rect[0], self.rect[3] - self.halfvt - self.do),
                           (self.rect[2] - self.halfht - self.do, self.rect[1])],
                          fill=self.fg)

    def DrawRightDiagonalHorizontal(self):
        self.draw.polygon([(self.rect[2] - self.ht - self.do, self.rect[1]),
                           (self.rect[0], self.rect[3]),
                           (self.rect[0] + self.ht + self.do, self.rect[3]),
                           (self.rect[2], self.rect[1])],
                          fill=self.fg)

    def DrawRightDiagonalVertical(self):
        # has vertical endpoints that look better on a "Z"
        self.draw.polygon([(self.rect[2], self.rect[1]),
                           (self.rect[0], self.rect[3] - self.vt - self.do),
                           (self.rect[0], self.rect[3]),
                           (self.rect[2], self.rect[1] + self.vt + self.do)],
                          fill=self.fg)

    def DrawUpperV(self):
        # draw the upper diagonals that would be used in a "Y"
        self.draw.polygon([(self.rect[0], self.rect[1]),
                           (self.hmidpoint - self.halfht - 1, self.vmidpoint - 2),
                           (self.hmidpoint + self.halfht, self.vmidpoint - 2),
                           (self.rect[0] + self.ht + self.do, self.rect[1])],
                          fill=self.fg)
        self.draw.polygon([(self.rect[2], self.rect[1]),
                           (self.hmidpoint + self.halfht, self.vmidpoint - 2),
                           (self.hmidpoint - self.halfht - 1, self.vmidpoint - 2),
                           (self.rect[2] - self.ht - self.do, self.rect[1])],
                          fill=self.fg)

class GridDrawer:
    """Grid Drawer class

    Class for "drawing" into a global grid. That is, selecting the grid
    locations that should be included for a particular segment of a
    global letter.
    """

    def __init__(self, size):
        self.x, self.y = size
        self.hmidpoint = int(np.floor(self.x / 2.))
        self.vmidpoint = int(np.floor(self.y / 2.))
        self.grid = np.zeros((self.x, self.y), dtype=bool)

    def Reset(self):
        self.grid[:] = False

    def Fill(self):
        self.grid[:] = True

    def DrawLeftSegment(self):
        self.grid[0, :] = True

    def DrawUpperLeftSegment(self):
        self.grid[0, 0:self.vmidpoint] = True

    def DrawLowerLeftSegment(self):
        self.grid[0, self.vmidpoint:] = True

    def DrawRightSegment(self):
        self.grid[-1, :] = True

    def DrawUpperRightSegment(self):
        self.grid[-1, 0:self.vmidpoint] = True

    def DrawLowerRightSegment(self):
        self.grid[-1, self.vmidpoint:] = True

    def DrawTopSegment(self):
        self.grid[:, 0] = True

    def DrawBottomSegment(self):
        self.grid[:, -1] = True

    def DrawHorizontalCenterSegment(self):
        self.grid[:, self.vmidpoint] = True

    def DrawVerticalCenterSegment(self):
        self.grid[self.hmidpoint, :] = True

    def DrawLowerVerticalCenterSegment(self):
        self.grid[self.hmidpoint, self.vmidpoint:self.y] = True

    def DrawLeftDiagonal(self):
        np.fill_diagonal(self.grid, True)

    def DrawLeftDiagonalHorizontal(self):
        self.DrawLeftDiagonal()

    def DrawRightDiagonal(self):
        np.fill_diagonal(np.rot90(self.grid), True)

    def DrawRightDiagonalHorizontal(self):
        self.DrawRightDiagonal()

    def DrawRightDiagonalVertical(self):
        self.DrawRightDiagonal()

    def DrawUpperV(self):
        # draw the upper diagonals that would be used in a "Y"
        np.fill_diagonal(self.grid[0:self.hmidpoint+1, 0:self.vmidpoint+1], True)
        np.fill_diagonal(np.flipud(self.grid)[0:self.hmidpoint+1, 0:self.vmidpoint+1], True)

    def Grid(self):
        return self.grid

class HierPyBase:
    """HierPyBase

    Base class for the other HierPy classes. Centralizes the drawing
    commands. Base classes should define self.win as a class that has
    the various segment drawing commands, at a bare minimum.
    """
    def __init__(self, letter=None):
        self.letter = letter
        self.win = None

    def Clear(self):
        self.win.Reset()

    def Fill(self):
        self.win.Fill()

    def SetLetter(self, letter):
        self.letter = letter
        self.win.Reset()
        if letter is None:
            return
        match self.letter:
            case "A":
                self.MakeLetterA()
            case "C":
                self.MakeLetterC()
            case "E":
                self.MakeLetterE()
            case "F":
                self.MakeLetterF()
            case "H":
                self.MakeLetterH()
            case "L":
                self.MakeLetterL()
            case "M":
                self.MakeLetterM()
            case "N":
                self.MakeLetterN()
            case "O":
                self.MakeLetterO()
            case "P":
                self.MakeLetterP()
            case "S":
                self.MakeLetterS()
            case "T":
                self.MakeLetterT()
            case "U":
                self.MakeLetterU()
            case "X":
                self.MakeLetterX()
            case "Y":
                self.MakeLetterY()
            case "Z":
                self.MakeLetterZ()
            case "All":
                self.Fill()
            case _:
                self.Fill()
                print('Requested small letter "{}" not implemented'.format(letter))

    def MakeLetterA(self):
        self.win.DrawLeftSegment()
        self.win.DrawRightSegment()
        self.win.DrawTopSegment()
        self.win.DrawHorizontalCenterSegment()

    def MakeLetterC(self):
        self.win.DrawLeftSegment()
        self.win.DrawTopSegment()
        self.win.DrawBottomSegment()

    def MakeLetterE(self):
        self.win.DrawLeftSegment()
        self.win.DrawTopSegment()
        self.win.DrawHorizontalCenterSegment()
        self.win.DrawBottomSegment()

    def MakeLetterF(self):
        self.win.DrawLeftSegment()
        self.win.DrawTopSegment()
        self.win.DrawHorizontalCenterSegment()

    def MakeLetterH(self):
        self.win.DrawLeftSegment()
        self.win.DrawRightSegment()
        self.win.DrawHorizontalCenterSegment()

    def MakeLetterL(self):
        self.win.DrawLeftSegment()
        self.win.DrawBottomSegment()

    def MakeLetterM(self):
        self.win.DrawLeftSegment()
        self.win.DrawRightSegment()
        self.win.DrawUpperV()

    def MakeLetterN(self):
        self.win.DrawLeftSegment()
        self.win.DrawRightSegment()
        self.win.DrawLeftDiagonal()

    def MakeLetterO(self):
        self.win.DrawLeftSegment()
        self.win.DrawRightSegment()
        self.win.DrawTopSegment()
        self.win.DrawBottomSegment()

    def MakeLetterP(self):
        self.win.DrawTopSegment()
        self.win.DrawLeftSegment()
        self.win.DrawUpperRightSegment()
        self.win.DrawHorizontalCenterSegment()

    def MakeLetterS(self):
        self.win.DrawTopSegment()
        self.win.DrawUpperLeftSegment()
        self.win.DrawHorizontalCenterSegment()
        self.win.DrawLowerRightSegment()
        self.win.DrawBottomSegment()

    def MakeLetterT(self):
        self.win.DrawTopSegment()
        self.win.DrawVerticalCenterSegment()

    def MakeLetterU(self):
        self.win.DrawLeftSegment()
        self.win.DrawRightSegment()
        self.win.DrawBottomSegment()

    def MakeLetterX(self):
        self.win.DrawLeftDiagonal()
        self.win.DrawRightDiagonal()

    def MakeLetterY(self):
        self.win.DrawUpperV()
        self.win.DrawLowerVerticalCenterSegment()

    def MakeLetterZ(self):
        self.win.DrawTopSegment()
        self.win.DrawBottomSegment()
        self.win.DrawRightDiagonal()

    def MakeRandom(self, nSegments):
        """MakeRandom(nSegments)

        Randoms draws up to 7 segments from the digit 8. Primary use is
        for drawing masks.
        """

        if nSegments < 0:
            nSegments = 0
        if nSegments > 7:
            nSegments = 7
        segments = rng.choice(7, nSegments, replace=False)
        if 0 in segments:
            self.win.DrawTopSegment()
        if 1 in segments:
            self.win.DrawUpperLeftSegment()
        if 2 in segments:
            self.win.DrawUpperRightSegment()
        if 3 in segments:
            self.win.DrawHorizontalCenterSegment()
        if 4 in segments:
            self.win.DrawLowerLeftSegment()
        if 5 in segments:
            self.win.DrawLowerRightSegment()
        if 6 in segments:
            self.win.DrawBottomSegment()

    def Letter(self):
        return self.letter

class HierPySmallLetter(HierPyBase):
    def __init__(self, letter=None):
        self.letter = letter
        self.win = PillowDrawer(small_size)
        self.SetLetter(letter)

    def GetImage(self):
        return self.win.GetImage()

class HierPy(HierPyBase):
    def __init__(self, large_letter=None, small_letter=None):
        # initialize object components
        self.letter = large_letter
        self.image = PillowDrawer(large_size)
        self.allLocations = self.MakeGrid()
        self.win = GridDrawer(large_layout)
        self.smallLetter = HierPySmallLetter(small_letter)

        # if the large letter was specified, then set it up
        if self.letter is not None:
            self.SetLetter(self.letter)

    def SetLetters(self, large_letter=None, small_letter=None):
        self.SetLetter(large_letter)
        self.SetSmallLetter(small_letter)

    def SetLetter(self, letter):
        self.image.Reset()
        super().SetLetter(letter)

    def SetSmallLetter(self, letter):
        self.smallLetter.SetLetter(letter)

    def Letters(self):
        return self.Letter(), self.smallLetter.Letter()

    def Draw(self):
        self.image.Place(self.smallLetter, self.allLocations[self.win.Grid()])

    def Save(self, filename):
        self.Draw()
        self.image.Save(filename)

    def ComputeSpacingAndOffset(self, display_size, object_size, n_objects):
        """offset, spacing = ComputeSpacingAndOffset(display_size, object_size, n_objects)

        Computes and returns the offset (external border) between rects
        and the spacing (space between rects)
        """

        offset = np.ceil(object_size / 2.0)
        offset = 0
        spacing = ((display_size - 2 * offset - n_objects * object_size) /
                   (n_objects - 1))
        return offset, spacing

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

if __name__=="__main__":
    if directory is None or not isinstance(directory, str):
        directory = ""
    else:
        if not os.path.exists(directory):
            directory = os.path.normpath(directory)
            os.makedirs(directory)

    letter = HierPy()
    if letters_to_draw is not None:
        for global_letter in letters_to_draw:
            for local_letter in letters_to_draw:
                letter.SetLetters(global_letter, local_letter)
                letter.Save(os.path.join(directory,
                                             "{}-{}{}.png".format(global_letter, local_letter,
                                                                      file_suffix)))
