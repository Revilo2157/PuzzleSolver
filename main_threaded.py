from Library import iter0, iter1
from PIL import Image, ImageDraw, ImageColor
from PuzzlePiece import PuzzlePiece 
import numpy as np
import os
import shutil
import time
from multiprocessing import Process, Lock, Manager
import pickle

numThreads = 10
whichPuzzle = "bigpuzzle"

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
    return stitched

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

def match(side1, side2):

	dx1, dy1 = (side1.points[0][0] - side1.points[-1][0], side1.points[0][1] - side1.points[-1][1])
	dx2, dy2 = (side2.points[0][0] - side2.points[-1][0], side2.points[0][1] - side2.points[-1][1])

	if min(abs(abs(dx1) - abs(dx2)), abs(abs(dx1) - abs(dy2))) > 15 or min(abs(abs(dy1) - abs(dy2)), abs(abs(dy1) - abs(dx2))) > 15:
		return 100000000

	a = side1.offsets
	b = side2.offsets[::-1]

	trials = []
	for offset in range(-int(len(max(a, b))/2), int(len(max(a, b))/2)):
		diff = 0
		for i in range(len(b)):
			aInd = i + offset
			if aInd < 0 or aInd >= len(a):
				diff += 50
			else:
				n = 0
				for color in a[aInd][0]:
					diff += abs(color - b[i][0][n])
					n += 1
				diff += abs(a[aInd][1] + b[i][1])
		trials.append((diff, offset))
	trials.sort(key=iter0)
	return trials[0][0]

def analyzePiece(identifier, pieces, lock, semaphore):
	with lock:
		print("Starting %d" % identifier)

	pieces.append(PuzzlePiece(identifier))

	with lock:
		print("Finished %d" % identifier)
	semaphore.release()

if __name__ == '__main__':
	puzzle = Image.open("resources/%s.png" % whichPuzzle)
	pPix = puzzle.load()

	try:
		with open("puzzle.cache", "rb") as cache:
			last = pickle.load(cache)
		if last != whichPuzzle:
			shutil.rmtree("pieces")
	except:
		pass

	with open("puzzle.cache", "wb") as cache:
		pickle.dump(whichPuzzle, cache)

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


	while (topLeft.getSide("TOP").classification != PuzzlePiece.EdgeType.FLAT 
		or topLeft.getSide("LEFT").classification != PuzzlePiece.EdgeType.FLAT):
		topLeft.rotatePiece()

	row = 0
	col = 1
	current = topLeft
	puzzle = [[current]]
	pieces.remove(current)
	for type in PieceEdges:
		PieceEdges[type].discard(current)

	while pieces:
		while True:
			print(row, col)
			for r in puzzle:
				for c in r:
					print("{:3}".format(c.identifier), end=" ")
				print("")
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

			print("Top: %s, Left: %s" % (topType.name, leftType.name))

			print("\n{:10} | {:10} | {:10}".format("Identifier", "Difference",  "Rotations"))
			print("{:10}_|_{:10}_|_{:10}".format("_"*10, "_"*10,  "_"*10))

			matches = []
			toCheck = PieceEdges[PuzzlePiece.matchingType(topType).name].intersection(PieceEdges[PuzzlePiece.matchingType(leftType).name])
			for piece in toCheck:
				for n in range(4):

					leftSide = piece.getSide("LEFT")
					topSide = piece.getSide("TOP")
					
					if leftSide.classification != PuzzlePiece.matchingType(leftType) or topSide.classification != PuzzlePiece.matchingType(topType):
						piece.rotatePiece()
						continue

					if leftSide.classification == PuzzlePiece.EdgeType.FLAT:
						leftMatch = 0
					else:
						leftMatch = match(left.getSide("RIGHT"), leftSide)

					if topSide.classification == PuzzlePiece.EdgeType.FLAT:
						topMatch = 0
					else:
						topMatch = match(above.getSide("BOTTOM"), topSide)

					print("{:10} | {:10} | {:10}".format(piece.identifier, leftMatch + topMatch, piece.rotations))

					matches.append((leftMatch + topMatch, piece, piece.rotations))

					piece.rotatePiece()

			print("\n")
			matches.sort(key=iter0)
			current = matches[0][1]
			while current.rotations != matches[0][2]:
				current.rotatePiece()

			if not col:
				puzzle.append([])

			puzzle[row].append(current)
			pieces.remove(current)

			for type in PieceEdges:
				PieceEdges[type].discard(current)

			if current.getSide("RIGHT").classification is PuzzlePiece.EdgeType.FLAT:
				break
					
			col += 1
		col = 0
		row += 1
		print("New Row")

	for r in puzzle:
		for c in r:
			print("{:3}".format(c.identifier), end=" ")
		print("")

	# width = sum([piece.open(PuzzlePiece.ImageType.ORIGINAL).size[0] for piece in puzzle[0]])
	# height = sum([row[0].open(PuzzlePiece.ImageType.ORIGINAL).size[1] for row in puzzle])

	# assembled = Image.new("RGBA", (width, height))
	# where = (0,0)
	# for row in puzzle:
	# 	for piece in row: 
	# 		assembled.paste(piece.open(PuzzlePiece.ImageType.ORIGINAL), where)
	# 		where = (where[0] + piece.open(PuzzlePiece.ImageType.ORIGINAL).size[0], where[1])
	# 	where = (0, where[1] + piece.open(PuzzlePiece.ImageType.ORIGINAL).size[1])
	# assembled.show()

	# for row in puzzle:
	# 	for col in row:
	# 		for n in range(3):
	# 			col.rotatePiece()

	transpose = []
	for col in puzzle[0]:
		transpose.append([])
	for row in puzzle:
		n = 0
		for col in row:
			transpose[n].append(col)
			n += 1

	for r in transpose:
		for c in r:
			print("{:3}".format(c.identifier), end=" ")
		print("")

	assembled = stitch(transpose)

	assembled.show()
	assembled.save("Assembled.png")