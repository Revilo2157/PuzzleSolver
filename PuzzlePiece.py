from PIL import Image, ImageFilter
from Library import *
import numpy as np
from enum import Enum
import pickle
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')

class PuzzlePiece:
	class ImageType(Enum):
		ORIGINAL = 0
		MASK     = 1
		EDGE     = 2

	class EdgeType(Enum):
		FLAT = 0
		HEAD = 1
		HOLE = 2

	class Side(Enum):
		BOTTOM = 0
		RIGHT  = 1
		TOP	 	 = 2
		LEFT   = 3

	class Edge:
		def __init__(self, points, side, classification, matched = False):
			self.points = points
			self.side = side
			self.classification = classification
			self.matched = matched

	def __init__(self, identifier): 
		self.identifier = identifier
		self.com = None
		self.corners = None
		self.perimeter = []
		self.edges = []
		self.filePrefix = "pieces/p%d/p%d" % (self.identifier, self.identifier)

		if not self.load():
			self.createEdge()

			plt.clf()
			for edge in self.getEdges():
				offset, loc, char = self.classifyEdge(edge)
				self.edges.append(self.Edge(offset, loc, char))
			print("")
			plt.axis("equal")
			plt.savefig(self.filePrefix + "-char.png")
			self.save()

	def save(self):
		toSave = {"edges" : [(edge.points, edge.side, edge.classification, edge.matched) for edge in self.edges], 
							"corners" : self.corners,
							"com" : self.com,
							"perimeter" : self.perimeter}

		with open(self.filePrefix + ".piece", "wb") as jar:
			pickle.dump(toSave, jar)

	def load(self):
		try:
			with open(self.filePrefix + ".piece" , "rb") as jar:
				toLoad = pickle.load(jar)
		except:
			print("Creating Piece %s" % self.identifier)
			return False

		print("Loaded Piece %s" % self.identifier)
		for var in toLoad.keys():
			if var == "edges":
				for edge in toLoad[var]:
					self.edges.append(self.Edge(edge[0], edge[1], edge[2], edge[3]))
			else:
				exec("self.%s = %s" % (var, str(toLoad[var])))

		for edge in self.edges:
			print("\t\t{:<6}: {:4}".format(edge.side.name, edge.classification.name))
		print("")
		return True

	def createEdge(self):
		maskImg = self.open(self.ImageType.MASK)
		edgeImg = maskImg.filter(ImageFilter.FIND_EDGES).convert("L")
		edgeImg.save(self.filePrefix + "-edge.png")
		edgePix = edgeImg.load()
		for i in range(edgeImg.size[0]):
			for j in range(edgeImg.size[1]):
				if edgePix[i,j]:
					self.perimeter.append((i, j))

	def getEdges(self):
		self.perimeter = parameterize(self.perimeter)
		self.corners = findCorners(self.perimeter)	

		indices = []
		cx, cy = (0,0)
		for point in self.corners:
			cx += point[0]
			cy += point[1]
			indices.append(self.perimeter.index(point))

		cx = cx / 4
		cy = cy / 4

		for n in range(len(indices)):
			second = n+1 if n < len(indices)-1 else 0
			if indices[n] > indices[second]:
				if indices[second] != min(indices):
					self.perimeter.reverse()
					break

		indices = [self.perimeter.index(point) 
			for point in self.corners]

		self.com = (cx, cy)
		mindex = np.min(indices)

		edges = []
		for n in range(len(indices)):
			first = indices[n]
			x1, y1 = self.corners[n]

			if n == len(indices) - 1:
				second = indices[0]
				x2, y2 = self.corners[0]

			else:
				second = indices[n + 1]
				x2, y2 = self.corners[n + 1]

			if second == mindex:
				edges.append(self.perimeter[first:] 
					+ self.perimeter[:second + 1])
			else:
				edges.append(self.perimeter[first:second + 1])
		return edges

	def open(self, which):
		if which == self.ImageType.ORIGINAL:
			return Image.open(self.filePrefix + ".png")

		elif which == self.ImageType.MASK:
			return Image.open(self.filePrefix + "-mask.png")

		elif which == self.ImageType.EDGE:
			return Image.open(self.filePrefix + "-edge.png")

	# Return the closest number to the center between a and b
	# Input: 
	#		points: the points on an edge to classify
	# Output: 
	#		a tuple containing the location on the piece 
	# 	(top, bottom, left, or right)
	# 	the characterized edge (Flat, Head, or Hole)
	def classifyEdge(self, points):
		x1, y1 = points[0]
		x2, y2 = points[-1]
		print("\t\t", end="")

		cx, cy = self.com

		if sign(x1 - cx) == sign(x2 - cx):
			loc = self.Side.LEFT if x1 - cx < 0 else self.Side.RIGHT
			offset = [sign(x1 - cx)*(point[0] - closest(x1, x2, cx)) 
				for point in points]

			textx = closest(x1, x2, cx) #x1 + sign(x1 - cx)*25
			texty = cy

		elif sign(y1 - cy) == sign(y2 - cy):
			loc = self.Side.BOTTOM if y1 - cy > 0 else self.Side.TOP
			offset = [sign(y1 - cy)*(point[1] - closest(y1, y2, cy))
				for point in points]

			texty = closest(y1, y2, cy) #y1 + sign(y1 - cy)*25
			textx = cx

		else:
			print("Incorrect Corners")

		mean = np.mean(offset)
		median = np.median(offset)

		if abs(mean - median) < 1:
			text = "FLAT"
			char = self.EdgeType.FLAT
		else:
			if mean > median:
				text = "HEAD"
				char = self.EdgeType.HEAD
			else:
				text = "HOLE"
				char = self.EdgeType.HOLE 

		plt.plot([point[0] for point in points], [point[1] for point in points])
		plt.text(textx, texty, text, bbox=dict(fc = "white", alpha=0.5))
		
		print("{:<6}: {:4}".format(loc.name, text))
		return (offset, loc, char)