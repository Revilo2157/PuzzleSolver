import numpy as np
from PIL import Image

def cart2pol(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(r, theta)

def distance(a, b):
	return np.sqrt((a[1] - b[1])**2 + (a[0] - b[0])**2)

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

	