from Library import *
from PIL import Image

def edges(row, col):
	sorted = parameterize(row, col)
	corners = findCorners(row, col)
	
	NW = sorted.index(0)
	SW = sorted.index(1)
	SE = sorted.index(2)
	NE = sorted.index(3)
	