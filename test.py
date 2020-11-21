from Library import iter0, iter1
from PIL import Image
from PuzzlePiece import PuzzlePiece 
import numpy as np
import os
import time
from multiprocessing import Process, Lock, Manager
import matplotlib
from matplotlib import pyplot as plt

numThreads = 10

def match(a, b):
	b = b[::-1]
	trials = []
	for offset in range(-int(len(max(a, b))/2), int(len(max(a, b))/2)):
		diff = 0
		for i in range(len(b)):
			aInd = i + offset
			if aInd < 0 or aInd >= len(a):
				diff += 10
			else:
				diff += abs(a[aInd][1] + b[i][1])
		trials.append((offset, diff))
	return trials

def analyzePiece(identifier):
	return PuzzlePiece(identifier)

if __name__ == '__main__':
	puzzle = Image.open("resources/medpuzzle.png")
	pPix = puzzle.load()

	# Do Not Delete
	mask = Image.new("RGBA", (puzzle.size[0], puzzle.size[1]))
	mPix = mask.load()
	for x in range(puzzle.size[0]):
	  for y in range(puzzle.size[1]):
	    if pPix[x, y] != pPix[0, 0]:
	      mPix[x, y] = (255, 255, 255, 255)
	    else:
	      mPix[x, y] = (0, 0, 0, 0)



	# mask = Image.open("resources/mask.png")

	rowOf0 = True
	colOf0 = True
	all0 = True
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

	x, y = (2, 0)
	identifier = int((x + y*len(colBoundaries)/2)/2) + 1
	print(identifier)

	try:
		os.mkdir("pieces")
	except:
		pass

	try:
		os.mkdir("pieces/p%02d" % identifier)
	except:
		pass

	top = rowBoundaries[y]
	bottom = rowBoundaries[y+1]
	left = colBoundaries[x]
	right = colBoundaries[x+1]

	cropBox = (left, top, right, bottom)

	piece = puzzle.crop(cropBox)
	piece.save("pieces/p%02d/p%02d.png" % (identifier, identifier))

	pieceMask = mask.crop(cropBox)
	pieceMask.save("pieces/p%02d/p%02d-mask.png" % (identifier, identifier))
	
	corner = analyzePiece(identifier)


	x, y = (0, 0)
	identifier = int((x + y*len(colBoundaries)/2)/2) + 1
	print(identifier)

	try:
		os.mkdir("pieces")
	except:
		pass

	try:
		os.mkdir("pieces/p%02d" % identifier)
	except:
		pass

	top = rowBoundaries[y]
	bottom = rowBoundaries[y+1]
	left = colBoundaries[x]
	right = colBoundaries[x+1]

	cropBox = (left, top, right, bottom)

	piece = puzzle.crop(cropBox)
	piece.save("pieces/p%02d/p%02d.png" % (identifier, identifier))

	pieceMask = mask.crop(cropBox)
	pieceMask.save("pieces/p%02d/p%02d-mask.png" % (identifier, identifier))

	next = analyzePiece(identifier)

	vals = match(corner.getSide("RIGHT").offsets, next.getSide("TOP").offsets)

	plt.figure(0)
	plt.clf()

	x1 = [point[0] for point in corner.getSide("RIGHT").offsets]
	y1 = [point[1] for point in corner.getSide("RIGHT").offsets]
	plt.plot(x1, y1[::-1])

	x2 = [point[0] for point in next.getSide("TOP").offsets]
	y2 = [point[1] + 10 for point in next.getSide("TOP").offsets]
	plt.plot(x2, y2)

	plt.figure(1)
	plt.clf()

	x3 = [point[0] for point in vals]
	y3 = [point[1] for point in vals]
	plt.plot(x3, y3)

	plt.show()
