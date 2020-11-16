from Library import *
from PIL import Image, ImageDraw
from PuzzlePiece import PuzzlePiece
import numpy as np

def stitch(matrix):
    width = 0
    height = 0

    # get width
    for x in range(len(matrix.size[0])):
        top = matrix[x][0].getSide("TOP").points
        width += abs(top[-1][0] - top[0][0])

    # get height
    for y in range(len(matrix.size[1])):
        left = matrix[0][y].getSide("LEFT").points
        height += abs(left[0][y] - left[-1][y])
    
    # create image
    stitched = Image.new('RGB', [2*width, 2*height])

    # attach pieces
    for x in range(len(matrix.size[0])):
        for y in range(len(matrix.size[1])):
            current = PuzzlePiece(x + y*matrix.size[0])
            rotations = current.rotations
            if (y == 0):
                height = 0
                if (x == 0):
                    stitched.paste(current.open(PuzzlePiece.ImageType.ORIGINAL), (0, 0), current.open(PuzzlePiece.ImageType.ORIGINAL))
                else:
                    print()
            else:
                print()
 
            
            # add piece to image
            stitched.paste(current.open(PuzzlePiece.ImageType.ORIGINAL), (height, width), current.open(PuzzlePiece.ImageType.ORIGINAL))


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

def newPoint(pt, rot):
    trans = [(1,0), (0,-1), (-1,0), (0,1)]
    x = pt[0]*trans[rot][1] - pt[1]*trans[rot][0]
    y = pt[0]*trans[rot][0] + pt[1]*trans[rot][1]

    return (x,y)

current = PuzzlePiece(1)
top = current.getSide("TOP").points
bot = current.getSide("BOTTOM").points

corners = [top[0], top[-1], bot[-1], bot[0]]

print("*** original position ***")
original = current.open(PuzzlePiece.ImageType.ORIGINAL)
draw = ImageDraw.Draw(original)
for coord in corners:
    print(coord)
    draw.point(coord, fill="yellow")
original.save("original.png")

print("\n*** rotated position ***")
rotated = current.open(PuzzlePiece.ImageType.ORIGINAL).rotate(90, expand=True)
draw = ImageDraw.Draw(rotated)
for coord in corners:
    new = newPoint(coord, 1)
    print(new)
    draw.point(new, fill="red")
rotated.save("rotated.png")
