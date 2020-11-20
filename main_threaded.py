from Library import iter0, iter1
from PIL import Image
from PuzzlePiece import PuzzlePiece 
import numpy as np
import os
import time
from multiprocessing import Process, Lock, Manager

numThreads = 10

def match(side1, side2):
	a = side1.offsets
	b = side2.offsets[::-1]
	trials = []
	for offset in range(-int(len(max(a, b))/2), int(len(max(a, b))/2)):
		diff = 0
		for i in range(len(b)):
			aInd = i + offset
			if aInd < 0 or aInd >= len(a):
				diff += 10
			else:
				diff += abs(a[aInd][1] + b[i][1])
		trials.append(diff)
	trials.sort()
	return trials[0]

def analyzePiece(identifier, pieces, lock, semaphore):
	with lock:
		print("Starting %d" % identifier)

	pieces.append(PuzzlePiece(identifier))

	with lock:
		print("Finished %d" % identifier)
	semaphore.release()

if __name__ == '__main__':
	puzzle = Image.open("resources/babyyoda.png")
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

	end = time.time()
	print("{:.2f} seconds".format(end - start))

	PieceEdges = {}

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

	for topLeft in PieceEdges["corner"]:
		break

	topLeft.printEdges()

	while (topLeft.getSide("TOP").classification != PuzzlePiece.EdgeType.FLAT 
		or topLeft.getSide("LEFT").classification != PuzzlePiece.EdgeType.FLAT):
		topLeft.rotatePiece()

	topLeft.printEdges()

	row = 0
	col = 1
	current = topLeft
	puzzle = [[current]]
	pieces.remove(current)
	for type in PieceEdges:
		PieceEdges[type].discard(current)

	while pieces:
		while True:
			corner = False
			if not row:
				above = None
				topType = PuzzlePiece.EdgeType["FLAT"]
			else:
				above = puzzle[row-1][col]
				topType = above.getSide("BOTTOM").classification

			if not col:
				left = None
				leftType = PuzzlePiece.EdgeType["FLAT"]
			else:
				left = puzzle[row][col-1]
				leftType = left.getSide("RIGHT").classification

			matches = []
			toCheck = PieceEdges[topType.name].intersection(PieceEdges[leftType.name])
			for piece in toCheck:
				while piece.getSide("TOP").classification != PuzzlePiece.matchingType(topType):			
					piece.rotatePiece()

				if col and piece in PieceEdges["corner"] and piece.getSide("RIGHT").classification != PuzzlePiece.EdgeType.FLAT:
					for n in range(3):
						piece.rotatePiece()
				left = piece.getSide("LEFT")

				if left.classification != PuzzlePiece.matchingType(leftType):
					continue

				matches.append((match(current.getSide("LEFT"), left), piece))

			matches.sort(key=iter0)
			current = matches[0][1]
			if not col:
				puzzle.append([])
			puzzle[row].append(current)

			pieces.remove(current)
			corner = current in PieceEdges["corner"]
			for type in PieceEdges:
				PieceEdges[type].discard(current)

			if col and corner:
				break
					
			col += 1
		col = 0
		row += 1

	width = sum([piece.open(PuzzlePiece.ImageType.ORIGINAL).size[0] for piece in puzzle[0]])
	for row in puzzle:
		print(row[0].open(PuzzlePiece.ImageType.ORIGINAL).size[1])
	height = sum([row[0].open(PuzzlePiece.ImageType.ORIGINAL).size[1] for row in puzzle])

	assembled = Image.new("RGBA", (width, height))
	where = (0,0)
	for row in puzzle:
		for piece in row: 
			assembled.paste(piece.open(PuzzlePiece.ImageType.ORIGINAL), where)
			where = (where[0] + piece.open(PuzzlePiece.ImageType.ORIGINAL).size[0], where[1])
		where = (0, where[1] + piece.open(PuzzlePiece.ImageType.ORIGINAL).size[1])
	assembled.show()