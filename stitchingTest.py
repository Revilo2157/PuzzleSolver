# from Library import *
from PIL import Image, ImageDraw, ImageColor
from PuzzlePiece import PuzzlePiece
import numpy as np

def stitch(matrix):
    width = 0
    height = 0

    # get width
    for x in range(len(matrix)): # number of cols
        piece = matrix[x][0]
        padded = max(piece.open(PuzzlePiece.ImageType.ORIGINAL).size)
        width += getWidth(piece, (int(np.floor(padded/2)), int(np.floor(padded/2))))

    # get height
    for y in range(len(matrix[0])): # number of rows
        piece = matrix[0][y]
        padded = max(piece.open(PuzzlePiece.ImageType.ORIGINAL).size)
        height += getHeight(piece, (int(np.floor(padded/2)), int(np.floor(padded/2))))

    # create image
    stitched = Image.new('RGBA', [width, height])
    w = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    h = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    # attach pieces
    for x in range(len(matrix)): # x = # of cols
        for y in range(len(matrix[0])): # y = # of rows
            current = matrix[x][y]
            img = current.open(PuzzlePiece.ImageType.ORIGINAL)
            rotations = current.rotations

            # add padding and paste
            square = max(img.size[0], img.size[1])
            resized = Image.new('RGBA', [square, square])
            resized.paste(img, (0,0), img)
            center = (int(np.floor(resized.size[0]/2)), int(np.floor(resized.size[1]/2)))
            rotatedImg = resized.rotate(rotations*90, center=center)

            # get transformed height and width of each piece
            w[x][y] = getWidth(current, center)
            h[x][y] = getHeight(current, center)
            
            # stich by top left corner
            ref = np.subtract((0,0), getTopLeft(current, center, rotations))

            if ((x == 0) and (y == 0)):
                height = 0
                width = [0]
                place = tuple(ref)
            else:
                # check x and y value
                if(x == 0):
                    width.append(0)
                else:
                    width[y] += w[x-1][y]

                if (y == 0):
                    height = 0
                else:
                    height += h[x][y-1]
                
                place = (ref[0] + width[y], ref[1] + height)
            
            # add piece to image
            stitched.paste(rotatedImg, place, rotatedImg)
    print(w)
    print(h)
    stitched.show()

def getHeight(piece, center):
    # subtract the last point of bottom by the first point of top
    rot = piece.rotations
    BL = newPoint(piece.getSide("BOTTOM").points[-1], center, rot)
    TL = newPoint(piece.getSide("TOP").points[0], center, rot)
    return  BL[1] - TL[1]

def getWidth(piece, center):
    # subtract the last point of top by the first point of the top
    rot = piece.rotations
    TR = newPoint(piece.getSide("TOP").points[-1], center, rot)
    TL = newPoint(piece.getSide("TOP").points[0], center, rot)
    return  TR[0] - TL[0]

def newPoint(pt, ref, rot):
    trans = [(1,0), (0,-1), (-1,0), (0,1)]
    x = (pt[0] - ref[0])*trans[rot][0] - (pt[1] - ref[1])*trans[rot][1] + ref[0]
    y = (pt[0] - ref[0])*trans[rot][1] + (pt[1] - ref[1])*trans[rot][0] + ref[1]

    return (x,y)

def getTopLeft(piece, center, rot):
    # get and store corners
    top = piece.getSide("TOP").points
    bot = piece.getSide("BOTTOM").points
    corners = [top[0], bot[-1], bot[0], top[-1]]
    
    return newPoint(corners[0], center, rot)

def rotTest():
    # get original
    piece = PuzzlePiece(1)
    original = piece.open(PuzzlePiece.ImageType.ORIGINAL)

    # add padding and paste
    square = max(original.size[0], original.size[1])
    print(original.size)
    print(square)
    resized = Image.new('RGBA', [square, square])
    resized.paste(original, (0,0), original)
    (cx, cy) = (int(np.floor(resized.size[0]/2)), int(np.floor(resized.size[1]/2)))
    rotated = resized.rotate(90, center=(cx, cy))

    # get point coordinates
    top = piece.getSide("TOP").points
    bot = piece.getSide("BOTTOM").points

    # store corners: TL, BL, BR, TR
    names = ["TL", "BL", "BR", "TR"]
    colors = ["red", "green", "blue", "yellow"]
    corners = [top[0], bot[-1], bot[0], top[-1]]

    # get original coordinates
    print("*** original position ***")
    print("center: (%d, %d)\n" % (cx, cy))
    orig_draw = ImageDraw.Draw(resized)

    i = 0
    for coord in corners:
        print("%s: " % (names[i]), end="")
        print(coord)
        orig_draw.point(coord, fill=ImageColor.getrgb(colors[i]))
        i+=1
    orig_draw.point((cx, cy), fill=ImageColor.getrgb("white"))
    del orig_draw
    resized.show()

    # rotate resized image
    print("\n*** rotated position ***")
    rot_draw = ImageDraw.Draw(rotated)

    i=0
    for coord in corners:
        print("%s: " % (names[i]), end="")
        new = newPoint(coord, (cx, cy), 1)
        print(new)
        rot_draw.point(new, fill=ImageColor.getrgb(colors[i]))
        i+=1
    rot_draw.point((cx, cy), fill=ImageColor.getrgb("white"))
    print("(%d, %d)" % (cx, cy))

    del rot_draw
    rotated.show()

def testTopLeft(piece, number):
    rot = piece.rotations
    img = piece.open(PuzzlePiece.ImageType.ORIGINAL)

    # add padding and paste
    square = max(img.size[0], img.size[1])
    resized = Image.new('RGB', [square, square])
    resized.paste(img, (0,0), img)
    # resized.show()
    c = int(np.floor(square/2))
    center = (c, c)
    rotatedImg = resized.rotate(rot*90, center=center)

    rot_draw = ImageDraw.Draw(rotatedImg)
    rot_draw.point(getTopLeft(piece, piece.com, rot), fill=ImageColor.getrgb("red"))

    text = "#" + str(number) + " rotations: " + str(rot)
    rot_draw.text((0, c), text)

    del rot_draw
    rotatedImg.show()

# # puzzle = [[PuzzlePiece(5), PuzzlePiece(3)], [PuzzlePiece(4), PuzzlePiece(2)], [PuzzlePiece(6), PuzzlePiece(1)]]
piece = [[1, 3, 7], [8, 6, 4], [9, 5, 2]]
rots = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
puzzle = [[], [], []]

for y in range(len(piece)): # x = # of cols
    for x in range(len(piece[0])): # y = # of rows
        current = PuzzlePiece(piece[x][y])
        for r in range(rots[x][y]):
            current.rotatePiece()
        puzzle[x].append(current)
stitch(puzzle)