from PIL import Image, ImageFilter
import cv2
from enum import Enum

def piece()

puzzle = Image.open("puzzle3.png")
pPix = puzzle.load()

mask = Image.new("RGBA", (puzzle.size[0], puzzle.size[1]))
blackWhite = mask.load()
for x in range(puzzle.size[0]):
  for y in range(puzzle.size[1]):
    if pPix[x, y] != pPix[0, 0]:
      blackWhite[x, y] = (255, 255, 255)
    else:
      blackWhite[x, y] = (0, 0, 0)
  print(x)

edges = mask.filter(ImageFilter.FIND_EDGES).convert("L")
edges.save("edges.png")
mask.save("mask.png")
