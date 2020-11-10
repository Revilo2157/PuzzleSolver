from PIL import Image
from PuzzlePiece import PuzzlePiece 
import os
import time
from multiprocessing import Process, Lock, Manager

numThreads = 10

def analyzePiece(identifier, pieces, lock, semaphore):
	with lock:
		print("Starting %d" % identifier)

	pieces.append(PuzzlePiece(identifier))

	with lock:
		print("Finished %d" % identifier)
	semaphore.release()

if __name__ == '__main__':
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

	for index in range(len(threads)):
		piece = pieces[index]
		print("Piece %d" % piece.identifier)
		piece.printEdges()
		print("")

	end = time.time()
	print("{:.2f} seconds".format(end - start))

	PieceEdges = {}

	puzzle = []

	for piece in pieces:
		count = 0
		for edge in piece.edges:
			if edge.classification.name == "FLAT":
				if "flat" not in PieceEdges:
					PieceEdges["flat"] = set()
				PieceEdges["flat"].add(piece)
				count += 1
			elif edge.classification.name == "HEAD":
				if "head" not in PieceEdges:
					PieceEdges["head"] = set()
				PieceEdges["head"].add(piece)
			elif edge.classification.name == "HOLE":
				if "hole" not in PieceEdges:
					PieceEdges["hole"] = set()
				PieceEdges["hole"].add(piece)

		if count == 2:
			if "corner" not in PieceEdges:
				PieceEdges["corner"] = set()
			PieceEdges["corner"].add(piece)
	

	print("")
	for type in PieceEdges:
		print("%d %s pieces" % (len(PieceEdges[type]), type))

	for topLeft in PieceEdges["corner"]:
		break

	topLeft.printEdges()

	while topLeft.getSide("TOP").side != PuzzlePiece.EdgeType.FLAT and topLeft.getSide("LEFT").side != PuzzlePiece.EdgeType.FLAT:
		topLeft.rotatePiece()

	topLeft.printEdges()