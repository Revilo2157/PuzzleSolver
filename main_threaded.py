from Library import iter0, iter1, iter01
from PIL import Image
from PuzzlePiece import PuzzlePiece 
import numpy as np
import os
import time
from multiprocessing import Process, Lock, Manager

numThreads = 10

# class Puzzle:

# 	def __init__(self):
# 		self.height = 0
# 		self.width = 0
# 		self.board = np.array()

# 	def addNewCol(self):

# 	def addNewRow(self):

def match(side1, side2):
	a = side1.points
	b = side2.points[::-1]
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
	trials.sort(key=iter1)
	return trials[0]

def analyzePiece(identifier, pieces, lock, semaphore):
	with lock:
		print("Starting %d" % identifier)

	pieces.append(PuzzlePiece(identifier))

	with lock:
		print("Finished %d" % identifier)
	semaphore.release()

if __name__ == '__main__':
	puzzle = Image.open("resources/babyYodaPuzzle.png")
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

	try:	
		os.mkdir("pieces")
	except:
		pass

	threads = []
	lock = Lock()
	manager = Manager()
	pieces = manager.list()
	semaphore = manager.Semaphore(numThreads)

	start = time.time()
	for y in range(0, len(rowBoundaries), 2):
		top = rowBoundaries[y]
		bottom = rowBoundaries[y+1]

		for x in range(0, len(colBoundaries), 2):
			identifier = int((x + y*len(colBoundaries)/2)/2) + 1

			try:
				os.mkdir("pieces/p%02d" % identifier)
			except:
				pass

			left = colBoundaries[x]
			right = colBoundaries[x+1]

			cropBox = (left, top, right, bottom)

			piece = puzzle.crop(cropBox)
			piece.save("pieces/p%02d/p%02d.png" % (identifier, identifier))

			pieceMask = mask.crop(cropBox)
			pieceMask.save("pieces/p%02d/p%02d-mask.png" % (identifier, identifier))

			semaphore.acquire()

			thread = Process(target=analyzePiece, args=(identifier, pieces, lock, semaphore))
			threads.append(thread)
			thread.start()

	for thread in threads:
		thread.join()

	# for index in range(len(threads)):
	# 	piece = pieces[index]
	# 	piece.printEdges()
	# 	print("")

	end = time.time()
	print("{:.2f} seconds".format(end - start))

	PieceEdges = {}

	puzzle = []

	for piece in pieces:
		count = 0
		for edge in piece.edges:
			name = edge.classification.name
			if name not in PieceEdges:
				PieceEdges[name] = set()
			PieceEdges[name].add(piece)
			
			if name == "FLAT":
				count += 1

		if count == 2:
			if "corner" not in PieceEdges:
				PieceEdges["corner"] = set()
			PieceEdges["corner"].add(piece)
	

	# print("")
	# for type in PieceEdges:
	# 	print("%d %s pieces" % (len(PieceEdges[type]), type))

	for topLeft in PieceEdges["corner"]:
		break

	topLeft.printEdges()

	while (topLeft.getSide("TOP").classification != PuzzlePiece.EdgeType.FLAT 
		or topLeft.getSide("LEFT").classification != PuzzlePiece.EdgeType.FLAT):
		topLeft.rotatePiece()

	topLeft.printEdges()

	toCheck = PieceEdges["FLAT"].intersection(PieceEdges[topLeft.getSide("RIGHT").classification.name])
	matches = []
	for piece in toCheck:
		while piece.getSide("TOP").classification != PuzzlePiece.EdgeType.FLAT:			
			piece.rotatePiece()

		left = piece.getSide("LEFT")

		if left.classification == PuzzlePiece.EdgeType.FLAT or left.classification == topLeft.getSide("RIGHT").classification:
			continue

		matches.append((match(topLeft.getSide("RIGHT"), left), piece, left, piece.identifier))


	matches.sort(key=iter01)
	piece = matches[0][1]
	pieceSide = matches[0][2]

	for match in matches:
		print(match)

	piece.printEdges()
	topLeft.show()
	piece.show()
	print(pieceSide)