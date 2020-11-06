import numpy as np
from PIL import Image

def iter0(item):
  return item[0]

def iter1(item):
  return item[1]

def iter10(item):
  return item[1][0]

def iter11(item):
  return item[1][1]

# Input: A tuple of cartesian coordinates (x, y)
# Output: A tuple of polar coordinates (r, theta)
def cart2pol(point):
	x, y = point
	r = np.sqrt(x**2 + y**2)
	theta = np.arctan2(y, x)
	return (r, theta)

# Input: A tuple of polar coordinates (r, theta)
# Output: A tuple of cartesian coordinates (, theta)
def pol2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return (x, y)

def distance(a, b):
	return np.sqrt((a[1] - b[1])**2 + (a[0] - b[0])**2)

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

def howRectangular(a, b, c, d):
	cx = (a[0] + b[0] + c[0] + d[0])/4
	cy = (a[1] + b[1] + c[1] + d[1])/4
	com = (cx, cy)
	da = distance(a, com)
	db = distance(b, com)
	dc = distance(c, com)
	dd = distance(d, com)
	avgD = (da + db + dc + dd)/4
	return np.sqrt(((da - avgD)**2 + (db - avgD)**2 + (dc - avgD)**2 + (dd - avgD)**2)/4)

def det(a, b):
	return a[0]*b[1] - a[1]*b[0]

def sign(a):
	return (a > 0)*2 - 1

def calcArea(a, b, c, d):
	abc = angle(a, b, c)
	abd = angle(a, b, d)
	if(abc[0] == np.pi and abd[0] == np.pi):
		return 0
	if sign(abc[1]) == sign(abd[1]) or ((abc[1] == 0 and abd[1] != 0) or (abc[1] != 0 and abd[1] == 0)):
		if(abc[0] > abd[0]):
			return abs(det(a, b) + det(b, c) + det(c, d) + det(d, a))/2
		else:
			return abs(det(a, b) + det(b, d) + det(d, c) + det(c, a))/2
	else:
		return calcArea(a, c, b, d)

# Input: A tuple of four points (a, b, c, d)
#				 Each point is a tuple of ints (x, y)
#
# Output: The four points in right hand order
def rightHand(points):
	abc = angle()

	return 

# EdgeConvert(Image.open("pieces/1-1edge.png"))


def saveTxtFile(row, column, fourCorners):
  index = 1
  f = open("PieceCorners/Piece" + str(index) + "Corners.txt", "w+")
  for coordinate in fourCorners[0]:
    print(coordinate[0])
    f.write(str(coordinate[0]) + "," + str(coordinate[1]) + "\n")
  f.close()
    
	
def findCorners(row, column):
	print("Analyzing %d-%d" % (column + 1, row + 1), end="\r")
	img = Image.open("pieces/%d-%dedge.png" % (column + 1, row + 1))
	edges = img.load()
	points = []
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			if (edges[i,j]):
				points.append((i, j))

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
		hull.append(current)

		if(current == first):
			break

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
		print("Testing %d-%d: %d%%" % (column + 1, row + 1, n/toCheck * 100), end="\r")
		n = n+1
		for pointB in hull:
			if pointA is pointB:
				continue
			for pointC in hull:
				if pointC is pointB or pointC is pointA:
					continue
				for pointD in hull:
					if pointD is pointC or pointD is pointB or pointD is pointA:
						continue

					setOfPoints = set((pointD, pointC, pointB, pointA))

					if setOfPoints in tested:
						continue

					tested.append(setOfPoints)

					rectangularness = howRectangular(pointA, pointB, pointC, pointD)

					area = calcArea(pointA, pointB, pointC, pointD)

					sorted.append(((pointA, pointB, pointC, pointD), area/(rectangularness + 10)))

	print("Testing %d-%d: 100%%" % (column + 1, row + 1))
	sorted.sort(key=iter1, reverse=True)
	saveTxtFile(row, column, sorted[0])
	return sorted[0]

def parameterize(row, column):
	img = Image.open("pieces/%d-%dedge.png" % (column + 1, row + 1))
	count = 0
	sum = [0, 0]
	edges = img.load()
	x = []
	y = []
	points = []
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			if (edges[i,j]):
				x.append(i)
				y.append(j)
				points.append((i, j))
				sum[0] += i
				sum[1] += j
				count += 1

	current = points.pop()
	first = current
	sorted = [current]
	while(points):
		next = points.pop(np.argmin([distance(current, point) for point in points]))

		if distance(next, current) < 3:
			sorted.append(next) 
			current = next

	sorted.append(first)

	return sorted

findCorners(1, 1)