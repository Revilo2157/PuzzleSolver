from PIL import Image, ImageFilter
from PuzzlePiece import PuzzlePiece 
# import cv2
from EdgeConvert import EdgeConvert


puzzle = Image.open("resources/transparent.png")
pPix = puzzle.load()

# Do Not Delete
# mask = Image.new("RGBA", (puzzle.size[0], puzzle.size[1]))
# blackWhite = mask.load()
# for x in range(puzzle.size[0]):
#   for y in range(puzzle.size[1]):
#     if pPix[x, y] != pPix[0, 0]:
#       blackWhite[x, y] = (255, 255, 255, 255)
#     else:
#       blackWhite[x, y] = (0, 0, 0, 0)
#   print(x)

# edges = mask.filter(ImageFilter.FIND_EDGES).convert("L")
# edges.save("resources/edges.png")
# mask.save("resources/mask.png")

mask = Image.open("resources/mask.png")
mPix = mask.load()

rowOf0 = True
colOf0 = True
all0 = True
pieces = []
colBoundaries = []
rowBoundaries = []
for x in range(puzzle.size[0]):
  all0 = True
  for y in range(puzzle.size[1]):
    if(mPix[x, y] != (0, 0, 0, 0)):
      all0 = False

  if(all0):
    if(not colOf0):
      colBoundaries.append(x)
    colOf0 = True

  else:
    if(colOf0):
      colBoundaries.append(x)
    colOf0 = False


for y in range(puzzle.size[1]):
  all0 = True
  for x in range(puzzle.size[0]):
    if(mPix[x, y] != (0, 0, 0, 0)):
      all0 = False

  if(all0):
      if(not rowOf0):
        rowBoundaries.append(y)
      rowOf0 = True
  else:
    if(rowOf0):
      rowBoundaries.append(y)
    rowOf0 = False


for x in range(0, len(colBoundaries), 2):
  left = colBoundaries[x]
  right = colBoundaries[x+1]
  for y in range(0, len(rowBoundaries), 2):
    top = rowBoundaries[y]
    bottom = rowBoundaries[y+1]

    print("left:%d, right:%d, top:%d, bottom:%d" % (left, right, top, bottom))
    cropBox = (left, top, right, bottom)
    # toAdd = Image.new("RGBA", (right - left, bottom - top))
    toAdd = puzzle.crop(cropBox)
    toAdd.save("pieces/%d-%d.png" % (x/2 + 1, y/2 + 1))
    pieces.append(PuzzlePiece("pieces/%d-%d.png" % (x/2 + 1, y/2 + 1)))


EdgeConvert(Image.open("pieces/1-1edge.png"))
  





