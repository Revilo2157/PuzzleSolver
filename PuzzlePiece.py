from PIL import Image, ImageFilter, ImageColor, ImageDraw, ImageFont
from Library import *
import numpy as np
from enum import Enum
import pickle

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

		def iterEnum(item):
			return item.side.value

	colors = (ImageColor.getrgb("red"), 	 ImageColor.getrgb("green"), 
						ImageColor.getrgb("yellow"), ImageColor.getrgb("blue"))

	def __init__(self, identifier): 
		self.identifier = identifier
		self.com = None
		self.corners = None
		self.perimeter = []
		self.edges = []
		self.rotations = 0
		self.filePrefix = "pieces/p%02d/p%02d" % (self.identifier, self.identifier)

		if not self.load():

			original = self.open(self.ImageType.ORIGINAL)
			imedge = Image.new("RGBA", (original.size[0], original.size[1]))
			imedge.paste((0,0,0,0), (0,0, original.size[0], original.size[1]))
			imPix = imedge.load()

			width, height = (40, 20)

			self.createEdge()

			textPoints = []

			for edge in self.getEdges():
				offset, loc, char = self.classifyEdge(edge)
				self.edges.append(self.Edge(offset, loc, char))

				for point in edge:
					x, y = point
					imPix[x, y] = self.colors[loc.value]
				
				x = [point[0] for point in edge]
				y = [point[1] for point in edge]

				cx, cy = self.com
				midx = np.mean(x)
				midy = np.mean(y)
				posx, posy = (midx - (midx - cx)/5, midy - (midy - cy)/5)

				textPoints.append(([(posx*5 - width/2, posy*5), 
														(posx*5 + width, posy*5 + height)], 
														(posx*5 - width/4, posy*5 + height/6), char.name))

			self.edges.sort(key=self.Edge.iterEnum)

			imedge = imedge.resize((original.size[0]*5, original.size[1]*5))
			draw = ImageDraw.Draw(imedge)
			for points in textPoints:
				draw.rectangle(points[0], fill=ImageColor.getrgb("white"))
				draw.text(points[1], points[2], 
					ImageColor.getrgb("black"), 
					font=ImageFont.truetype("resources/Roboto-Regular.ttf", 15))
			imedge.save(self.filePrefix + "-char.png")

			self.save()

	def save(self):
		toSave = {"edges" : [(edge.points, edge.side, edge.classification, edge.matched) 
														for edge in self.edges], 
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
			return False

		for var in toLoad.keys():
			if var == "edges":
				for edge in toLoad[var]:
					self.edges.append(self.Edge(edge[0], edge[1], edge[2], edge[3]))
			else:
				exec("self.%s = %s" % (var, str(toLoad[var])))
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
          
	def rotatePiece(self):
		self.rotations = (self.rotations + 1) % 4
		for edge in self.edges:
			edge.side = self.Side(edge.side.value + 1)
			if edge.side.value >= 4:
				edge.side = self.Side(0)

	def getEdges(self):
		self.perimeter = parameterize(self.perimeter)
		self.corners   = findCorners(self.perimeter)	

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

		cx, cy = self.com

		if sign(x1 - cx) == sign(x2 - cx):
			loc = self.Side.LEFT if x1 - cx < 0 else self.Side.RIGHT
			offset = [(point[1], sign(x1 - cx)*(point[0] - closest(x1, x2, cx)))
				for point in points]

			# textx = closest(x1, x2, cx) #x1 + sign(x1 - cx)*25
			# texty = cy

		elif sign(y1 - cy) == sign(y2 - cy):
			loc = self.Side.BOTTOM if y1 - cy > 0 else self.Side.TOP
			offset = [(point[0], sign(y1 - cy)*(point[1] - closest(y1, y2, cy)))
				for point in points]

			# texty = closest(y1, y2, cy) #y1 + sign(y1 - cy)*25
			# textx = cx

		else:
			print("Incorrect Corners")

		mean = np.mean([point[1] for point in offset])
		median = np.median([point[1] for point in offset])

		if abs(mean - median) < 1:
			char = self.EdgeType.FLAT
		else:
			if mean > median:
				char = self.EdgeType.HEAD
			else:
				char = self.EdgeType.HOLE 

		return (offset, loc, char)


	def printEdges(self):
		for edge in self.edges:
			print("\t{:<6}: {:4}".format(
				edge.side.name, 
				edge.classification.name))
