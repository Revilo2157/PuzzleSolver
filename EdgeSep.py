import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
matplotlib.use('Agg')

def sortPol(r, theta):
  data = [(r[x], theta[x]) for x in range(len(r))]
  data.sort(key=iter)
  return [n[0] for n in data], [n[1] for n in data]

def iter0(item):
  return item[0]

def iter1(item):
  return item[1]

def iter10(item):
  return item[1][0]

def iter11(item):
  return item[1][1]

def cart2pol(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(r, theta)

def pol2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

def distance(a, b):
	return np.sqrt((a[1] - b[1])**2 + (a[0] - b[0])**2)

def angle(A, B, C):
	c = distance(A, B)
	b = distance(A, C)
	a = distance(B, C)
	cross = np.cross([B[0] - A[0], B[1] - A[1]], [C[0] - B[0], C[1] - B[1]])
	loc = (c**2 + a**2 - b**2)/(2*c*a)
	if loc >= -1:
		theta = np.arccos(loc)
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
	if(abc[0] == np.pi or abd[0] == np.pi):
		return 0
	if(sign(abc[1]) == sign(abd[1])):
		if(abc[0] > abd[0]):
			return abs(det(a, b) + det(b, c) + det(c, d) + det(d, a))/2
		else:
			return abs(det(a, b) + det(b, d) + det(d, c) + det(c, a))/2
	else:
		return calcArea(a, c, b, d)
	

img = Image.open("pieces/1-3edge.png")

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
avg = [sum[0]/count, sum[1]/count]

x = [n[0] for n in points]
y = [n[1] for n in points]

plt.clf()
plt.plot(x, y, "b.")
plt.savefig("test1.png")

hull = []
points.sort(key = iter0)
points.sort(key = iter1)
current = points[0]
hull.append(current)
prev = (0, current[1])
done = False
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

print(len(hull))

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

print(len(hull))

tested = []
sorted = []
for pointA in hull:
	print(pointA)
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

sorted.sort(key=iter1, reverse=True)

for line in sorted[:2]:
	point = line[0]
	print(line)
	print(howRectangular(point[0], point[1], point[2], point[3]))
	print(calcArea(point[0], point[1], point[2], point[3]))

x = [n[0] for n in sorted[0][0]]
y = [n[1] for n in sorted[0][0]]

plt.plot(x, y, "ro")
plt.savefig("test2.png")
