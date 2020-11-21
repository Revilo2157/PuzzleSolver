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
				diff += 100
			else:
				for n in range(3):
					diff += abs(a[aInd][0][n] - b[i][0][n])
				diff += abs(a[aInd][1] + b[i][1])
		trials.append((diff, offset))
	return trials

def analyzePiece(identifier):
	return PuzzlePiece(identifier)

def getPiece(row, col):
	x, y = (col*2, row*2)
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
	
	return analyzePiece(identifier)

if __name__ == '__main__':
	puzzle = Image.open("resources/bigpuzzle.png")
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

	first = getPiece(0, 0)
	firstSide = "RIGHT"
	firstOff = first.getSide(firstSide).offsets

	r1 = [color[0][0] for color in firstOff]
	g1 = [color[0][1] for color in firstOff]
	b1 = [color[0][2] for color in firstOff]

	plt.figure(2)
	plt.clf()
	plt.plot(r1, "r")
	plt.plot(g1, "g")
	plt.plot(b1, "b")

	second = getPiece(2, 3)
	secondSide = "RIGHT"
	secondOff = second.getSide(secondSide).offsets

	r2 = [color[0][0] for color in secondOff]
	g2 = [color[0][1] for color in secondOff]
	b2 = [color[0][2] for color in secondOff]

	plt.figure(3)
	plt.clf()
	plt.plot(r2, "r")
	plt.plot(g2, "g")
	plt.plot(b2, "b")

	vals = match(firstOff, secondOff)

	plt.figure(0)
	plt.clf()

	y1 = [point[1] for point in firstOff]

	plt.plot(y1)

	y2 = [point[1] for point in secondOff]

	plt.plot(y2)


	# yflip = y1[::-1]
	# try:
	# 	for n in range(len(y1)):
	# 		print("({:4}, {:4}), ({:4}, {:4})".format(x2[n], y2[n], x1[n], yflip[n]))
	# except:
	# 	pass

	# y1.reverse()

	# diff = 0
	# for n in range(len(y2)):
	# 	try:
	# 		diff += abs(y1[n] + y2[n])
	# 		print(y1[n], y2[n], diff)
	# 	except:
	# 		pass

	plt.figure(1)
	plt.clf()

	x3 = [point[1] for point in vals]
	y3 = [point[0] for point in vals]
	plt.plot(x3, y3)

	vals.sort(key=iter0)
	print(vals[0])

	plt.show()