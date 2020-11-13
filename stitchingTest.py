from Library import *
from PIL import Image
from PuzzlePiece import PuzzlePiece
import numpy as np

# def stitch(matrix):
#     xlen = 0
#     ylen = 0

#     for x in range(len(matrix.size[0])):
#         piece = 

def tester():
    # get height of 36
    thirty6 = PuzzlePiece(36)
    left36 = thirty6.getSide("LEFT").points
    len36 = left36[0][1] - left36[-1][1]

    # get height of 1
    one = PuzzlePiece(1)
    left1 = one.getSide("LEFT").points #list of tuples
    len1 = left1[0][1] - left1[-1][1]

    # get height of 41
    forty1 = PuzzlePiece(41)
    left41 = forty1.getSide("LEFT").points
    len41 = left41[0][1] - left41[-1][1]

    height = len36 + len1 + len41
    # print("len1 = %d, len41 = %d, height = %d\n" % (len1, len41, height))
    # get width of both
    top1 = one.getSide("TOP").points
    top41 = forty1.getSide("TOP").points
    width1 = top1[-1][0] - top1[0][0]
    width41 = top41[-1][0] - top41[0][0]
    width = abs(max(width1, width41))

    # test
    bottom36 = thirty6.getSide("BOTTOM").points
    bottom1 = one.getSide("BOTTOM").points
    # print("width: %d, height: %d" % (width, height))
    # print("top left: (%d,%d), top right: (%d,%d)\nbottom left: (%d,%d), bottom right: (%d,%d)" %
    # (top1[0][0], top1[0][1], top1[-1][0], top1[-1][1], bottom1[-1][0], bottom1[-1][1], bottom1[0][0], bottom1[0][1]))

    # create image
    stitched = Image.new('RGB', [2*width, 2*height])

    # line up pieces
    stitched.paste(thirty6.open(PuzzlePiece.ImageType.ORIGINAL), (0,0), thirty6.open(PuzzlePiece.ImageType.ORIGINAL)) # img, coordinates, mask
    stitched.paste(one.open(PuzzlePiece.ImageType.ORIGINAL), tuple(np.subtract(bottom36[-1], top41[0])), one.open(PuzzlePiece.ImageType.ORIGINAL)) # img, coordinates, mask
    stitched.paste(forty1.open(PuzzlePiece.ImageType.ORIGINAL), tuple(np.subtract(bottom1[-1], top41[0]) + [0, len36]), forty1.open(PuzzlePiece.ImageType.ORIGINAL))

    stitched.show()