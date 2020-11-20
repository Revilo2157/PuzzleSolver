from Library import *
from PIL import Image, ImageDraw, ImageColor
from PuzzlePiece import PuzzlePiece
import numpy as np

def stitch(matrix):
    width = 0
    height = 0

    # get width
    for x in range(len(matrix)): # number of cols
        width += getWidth(matrix[x][0])

    # get height
    for y in range(len(matrix[0])): # number of rows
        height += getHeight(matrix[0][y])
    
    # create image
    stitched = Image.new('RGB', [width, height])

    # attach pieces
    for x in range(len(matrix)): # x = # of cols
        for y in range(len(matrix[0])): # y = # of rows
            current = matrix[x][y]
            # rotations = current.rotations
            ref = np.subtract((0,0), getTopLeft(current))

            if ((x == 0) and (y == 0)):
                height = 0
                width = [0]
                place = tuple(ref)
            else:
                # check x and y value
                if(x == 0):
                    width.append(0)
                else:
                    width[y] += getWidth(matrix[x-1][y])

                if (y == 0):
                    height = 0
                else:
                    height += getHeight(matrix[x][y-1])
                
                place = (ref[0] + width[y], ref[1] + height)

            # print("\n[%d, %d]" % (x, y))
            # print(ref)
            # print(width[y])
            # print(height)
            # print(place)
            
            # add piece to image
            stitched.paste(current.open(PuzzlePiece.ImageType.ORIGINAL), place, current.open(PuzzlePiece.ImageType.ORIGINAL))
            
    stitched.show()

def getTopLeft(piece):
    return piece.getSide("TOP").points[0]

def getHeight(piece):
    # subtract the last point of bottom by the first point of top
    return piece.getSide("BOTTOM").points[-1][1] - piece.getSide("TOP").points[0][1]

def getWidth(piece):
    # subtract the last point of top by the first point of the top
    return piece.getSide("TOP").points[-1][0] - piece.getSide("TOP").points[0][0]

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
    # get width of both
    top1 = one.getSide("TOP").points
    top41 = forty1.getSide("TOP").points
    width1 = top1[-1][0] - top1[0][0]
    width41 = top41[-1][0] - top41[0][0]
    width = abs(max(width1, width41))

    # test
    bottom36 = thirty6.getSide("BOTTOM").points
    bottom1 = one.getSide("BOTTOM").points
    
    # create image
    stitched = Image.new('RGB', [2*width, 2*height])

    # line up pieces
    stitched.paste(thirty6.open(PuzzlePiece.ImageType.ORIGINAL), (0,0), thirty6.open(PuzzlePiece.ImageType.ORIGINAL)) # img, coordinates, mask
    stitched.paste(one.open(PuzzlePiece.ImageType.ORIGINAL), tuple(np.subtract(bottom36[-1], top41[0])), one.open(PuzzlePiece.ImageType.ORIGINAL)) # img, coordinates, mask
    stitched.paste(forty1.open(PuzzlePiece.ImageType.ORIGINAL), tuple(np.subtract(bottom1[-1], top41[0]) + [0, len36]), forty1.open(PuzzlePiece.ImageType.ORIGINAL))

    stitched.show()

puzzle = [[PuzzlePiece(5), PuzzlePiece(3)], [PuzzlePiece(4), PuzzlePiece(2)], [PuzzlePiece(6), PuzzlePiece(1)]]
stitch(puzzle)

def newPoint(pt, ref, rot):
    trans = [(1,0), (0,1), (-1,0), (0,-1)]
    x = (pt[0] - ref[0])*trans[rot][0] - (pt[1] - ref[1])*trans[rot][1] + ref[0]
    y = (pt[0] - ref[0])*trans[rot][1] + (pt[1] - ref[1])*trans[rot][0] + ref[1]

    return (x,y)

def rotTest():
    current = PuzzlePiece(1)
    top = current.getSide("TOP").points
    bot = current.getSide("BOTTOM").points

    corners = [top[0], bot[-1], bot[0], top[-1]]

    print("*** original position ***")
    original = current.open(PuzzlePiece.ImageType.ORIGINAL)
    (cx, cy) = (int(original.size[0]/2), int(original.size[1]/2))
    print("center: (%d, %d)\n" % (cx, cy))
    orig_draw = ImageDraw.Draw(original)

    for coord in corners:
        print(coord)
        orig_draw.point(coord, fill=ImageColor.getrgb("red"))
    orig_draw.point((cx, cy), fill=ImageColor.getrgb("red"))
    del orig_draw
    original.show()

    print("\n*** rotated position ***")
    rotated = current.open(PuzzlePiece.ImageType.ORIGINAL).rotate(90, center=(cx, cy))
    rot_draw = ImageDraw.Draw(rotated)

    for coord in corners:
        new = newPoint(coord, (cx, cy), 1)
        print(new)
        rot_draw.point(new, fill=ImageColor.getrgb("red"))
    rot_draw.point((cx, cy), fill=ImageColor.getrgb("red"))
    del rot_draw
    rotated.show()
