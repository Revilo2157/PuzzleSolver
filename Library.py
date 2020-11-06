import numpy as np
from PIL import Image
import EdgeType
# from matplotlib import pyplot as plt
# import matplotlib
# matplotlib.use('Agg')

# Given a tuple, return the first element
def iter0(item):
  return item[0]

# Given a tuple, return the second element
def iter1(item):
  return item[1]

# Given a tuple of tuples, 
# return the first element of the second outer element
def iter10(item):
  return item[1][0]

# Given a tuple of tuples, 
# return the second element of the second outer element
def iter11(item):
  return item[1][1]

# Convert cartesian coordinates to polar coordinates
# Input: 
# 	point: a tuple of cartesian coordinates (x, y)
# Output: 
# 	a tuple of polar coordinates (r, theta)
def cart2pol(point):
	x, y = point
	r = distance(point, (0,0))
	theta = np.arctan2(y, x)
	return (r, theta)

# Convert polar coordinates to cartesian coordinates
# Input: 
#		point: a tuple of polar coordinates (r, theta)
# Output: 
#		a tuple of cartesian coordinates (x, y)
def pol2cart(point):
	r, theta = point
	x = r * np.cos(theta)
	y = r * np.sin(theta)
	return (x, y)

# Find the distance between two points
# Input: 
#		point1: a tuple of polar coordinates (x, y)
#		point2: a tuple of polar coordinates (x, y)
# Output: 
#		the distance between point1 and point2
def distance(point1, point2):
	x1, y1 = point1
	x2, y2 = point2
	return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Find the angle between three points with the second being the vertex
# Input: 
#		A: a tuple of cartesian coordinates (x, y)
#		B: a tuple of cartesian coordinates (x, y)
#		C: a tuple of cartesian coordinates (x, y)
# Output: 
#		a tuple of containing the angle, in radians, 
#		and the cross product of AB and BC (theta, cross)
def angle(A, B, C):
	c = distance(A, B)
	b = distance(A, C)
	a = distance(B, C)
	cross = np.cross([B[0] - A[0], B[1] - A[1]], [C[0] - B[0], C[1] - B[1]])
	loc = (c**2 + a**2 - b**2)/(2*c*a)
	if loc >= -1:
		if loc <= 1:
			theta = np.arccos(loc)
		else:
			theta = 0
	else:
		theta = np.pi
	return (theta, cross)

# How far the polygon drawn by the four 
# points deviates from a rectangle. 0 being 
# perfectly rectangular
# Input: 
# 	points: a tuple containing four cartesian coordinates 
# Output: 
#		a measure of rectangularness
def howRectangular(points):
	a, b, c, d = points
	cx = (a[0] + b[0] + c[0] + d[0])/4
	cy = (a[1] + b[1] + c[1] + d[1])/4
	com = (cx, cy)
	da = distance(a, com)
	db = distance(b, com)
	dc = distance(c, com)
	dd = distance(d, com)
	avgD = (da + db + dc + dd)/4
	return np.sqrt(((da - avgD)**2 + (db - avgD)**2 + (dc - avgD)**2 + (dd - avgD)**2)/4)

# Find determinant of two points
# Input: 
#		A: a tuple of cartesian coordinates (x, y)
#		B: a tuple of cartesian coordinates (x, y)
# Output: 
#		the determinant of the two points
def det(a, b):
	return a[0]*b[1] - a[1]*b[0]

# Find the sign of a value
# Input: 
#		A: a numeric value
# Output: 
#		The sign of the value, zero if a is zero
def sign(a):
	if(not a): return 0
	return (a > 0)*2 - 1

# Sort the input points in right hand order
# Input: 
#		points: a tuple containing four cartesian coordinates 
# Output: 
# 	a tuple containing the four points 
# 	in right hand order
def rightHand(points):
	first = points[0]
	for vertex in points[1:]:
		orientations = []
		angles = []
		handles = []
		for handle in points[1:]:
			if(vertex == handle):
				continue
			theta, cross = angle(first, vertex, handle)
			orientations.append(sign(cross))
			angles.append(theta)
			handles.append(handle)
		if -1 not in orientations and 1 in orientations:
			if angles[0] > angles[1]:
				return (first, vertex, handles[0], handles[1])
			else:
				return (first, vertex, handles[1], handles[0])

# Find the area enclosed by the polygon 
# drawn by four points
# Input: 
#		points: a tuple containing four cartesian coordinates 
# Output: 
#		the area enclosed by the four points
def calcArea(points):
	a, b, c, d = rightHand(points)
	return abs(det(a, b) + det(b, c) + det(c, d) + det(d, a))/2
	
# Find the subset of points that creates the largest concave shape
# drawn by four points
# Input: 
#		points: a list containing cartesian coordinates of a polygon
# Output: 
#		a list of points making up the convex hull
def convexHull(points):

	points = points[:]

	hull = []
	points.sort(key = iter0)
	points.sort(key = iter1)
	current = points[0]
	hull.append(current)
	prev = (0, current[1])
	first = current

	while(1):
		potential = []
		for next in points:
			if(current == next):
				continue
		
			theta, cross = angle(prev, current, next)
			if(cross >= 0):
				potential.append((next, (theta, distance(current, next))))

		potential.sort(key = iter11)
		potential.sort(key = iter10, reverse = True)

		prev = current
		current = potential.pop(0)[0]
		points.remove(current)
		if(current == first):
			break
		hull.append(current)

	return hull


# Find the subset of points corresponding 
# to the four corners of a shape
# Input: 
#		points from which to find the corners from
# Output: 
#		a tuple of the coordinates of the four corners 
def findCorners(points):
	print("\tAnalyzing", end="\r")

	hull = convexHull(points)

	n = 0
	while n < len(hull):
		start = hull[n]
		sx = start[0]
		sy = start[1]
		end = -1
		for j in range(n + 1, len(hull)):
			point = hull[j]
			if sx == point[0] or sy == point[1]:
				end = j
			else:
				break
		
		if(end != -1):
			toRemove = hull[n+1: end]
			for point in toRemove:
				hull.remove(point)
		n = n+1

	toCheck = len(hull)
	n = 0

	tested = []
	sorted = []
	for pointA in hull:
		print("\tAnalyzing: %3d%%" % (n/toCheck * 100), end="\r")
		n = n+1
		for pointB in hull:
			if pointA is pointB:
				continue
			if distance(pointA, pointB) < 10:
				continue

			for pointC in hull:
				if pointC is pointB or pointC is pointA:
					continue
				if distance(pointA, pointC) < 10 :
					continue
				if distance(pointC, pointB) < 10:
					continue 

				for pointD in hull:
					if pointD is pointC:
						continue
					if pointD is pointB:
						continue
					if pointD is pointA:
						continue
					if distance(pointD, pointC) < 10 :
						continue
					if distance(pointD, pointB) < 10:
						continue 
					if distance(pointA, pointD) < 10 :
						continue

					points = (pointD, pointC, pointB, pointA)
					setOfPoints = set(points)
					if setOfPoints in tested:
						continue

					tested.append(setOfPoints)
					points = rightHand(points)

					rectangularness = howRectangular(points)
					area = calcArea(points)

					sorted.append((points, area/(rectangularness + 10)))

	print("\tAnalyzing: 100%")
	sorted.sort(key=iter1, reverse=True)

	return sorted[0][0]

# Sort the points based on how a parameterized line would visit them
# Input: 
#		points: a list of points
# Output: 
#		a list of coordinates sorted by the parameterizing function 
def parameterize(points):

	points.sort(key=iter1, reverse=True)
	current = points.pop()
	thresh = len(points)/2
	first = current
	sorted = [current]
	inserted = False

	while(points):

		if(len(points) < thresh and not inserted):
			inserted = True
			points.append(first)
		next = points.pop(np.argmin([distance(current, point) for point in points]))

		#if distance(next, current) < 2:
		sorted.append(next) 
		current = next

		if(inserted and current == first):
			break

	return sorted

# Return the closest number to the center between a and b
# Input: 
#		a: number
#		b: number
# 	center: number to compare the others to
# Output: 
#		a if it is closest to the center, otherwise b 
def closest(a, b, center):
	if abs(a - center) < abs(b - center):
		return a
	else:
		return b

# Return the closest number to the center between a and b
# Input: 
#		edge: the points on an edge to classify
# Output: 
#		starting from the bottom, the characterized edge 
# 	and its corresponding points 
def classifyEdge(edge, com):
	# sorted = parameterize(points)
	# corners = findCorners(sorted)

	# # x = [point[0] for point in sorted]
	# # y = [point[1] for point in sorted]	

	# indices = []
	# cx, cy = (0,0)
	# for point in corners:
	# 	cx += point[0]
	# 	cy += point[1]
	# 	indices.append(sorted.index(point))

	# cx = cx / 4
	# cy = cy / 4

	# mindex = np.min(indices)

	# edges = []
	# characterized = []
	# for n in range(len(indices)):
	# 	first = indices[n]
	# 	x1, y1 = corners[n]

	# 	if n == len(indices) - 1:
	# 		second = indices[0]
	# 		x2, y2 = corners[0]

	# 	else:
	# 		second = indices[n + 1]
	# 		x2, y2 = corners[n + 1]


	# 	if second == mindex:
	# 		edge = sorted[first:] + sorted[:second + 1]
	# 	else:
	# 		edge = sorted[first:second + 1]

		#print(x1, x2, y1, y2, cx, cy)

	x1, y1 = edge[0]
	x2, y2 = edge[-1]
	print("\t\t", end="")

	if sign(x1 - cx) == sign(x2 - cx):
		loc = "Left" if x1 - cx < 0 else "Right"
		edges.append(
			[sign(x1 - cx)*(point[0] - closest(x1, x2, cx)) 
			for point in edge])

		# textx = closest(x1, x2, cx) #x1 + sign(x1 - cx)*25
		# texty = cy

	elif sign(y1 - cy) == sign(y2 - cy):
		loc = "Bottom" if y1 - cy < 0 else "Top"
		offset = [sign(y1 - cy)*(point[1] - closest(y1, y2, cy))
							for point in edge]

			# texty = closest(y1, y2, cy) #y1 + sign(y1 - cy)*25
			# textx = cx

	else:
		print("Incorrect Corners")

	offset = edges	
	mean = np.mean(offset)
	median = np.median(offset)

	if abs(mean - median) < 1:
		text = "Flat"
		char = EdgeType.FLAT
	else:
		if mean > median:
			text = "Head"
			char = EdgeType.HEAD
		else:
			text = "Hole"
			char = EdgeType.HOLE 
	
	

	print("{:<6}: {:4}".format(loc, text))
	return characterized

# for col in range(9):
# 	for row in range(6):

# 		plt.clf()

# 		sorted = parameterize(row, col)
# 		corners = findCorners(row,col)

# 		print("\t\t", corners)

# 		x = [n[0] for n in sorted]
# 		y = [n[1] for n in sorted]

# 		plt.plot(x, y, "b")

# 		x = [n[0] for n in corners]
# 		y = [n[1] for n in corners]

# 		plt.plot(x, y, "ro")
# 		plt.savefig("pieces/%d-%dcorners.png" % (col + 1, row + 1))

# def testParameterize(row, col):
# 	plt.axis('square')
# 	plt.clf()
# 	edges = parameterize(row, col)
# 	x = [n[0] for n in edges]
# 	y = [n[1] for n in edges]

# 	plt.plot(x, y)
# 	plt.savefig("test.png")

# testParameterize(4, 1)