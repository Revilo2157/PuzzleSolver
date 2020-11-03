import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
matplotlib.use('Agg')

def cart2pol(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(r, theta)

def distance(a, b):
	return np.sqrt((a[1] - b[1])**2 + (a[0] - b[0])**2)

img = Image.open("pieces/1-3edge.png")
pix = img.load()

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


avg = (sum[0]/count, sum[1]/count)

current = points.pop()
first = current
sorted = [current]
while(points):
	next = points.pop(np.argmin([distance(current, point) for point in points]))

	if distance(next, current) < 3:
		sorted.append(next) 
		current = next

	

sorted.append(first)



r = []
theta = []
for n in sorted:
	out = cart2pol(n[0] - avg[0], n[1] - avg[1])
	r.append(out[0])
	theta.append(out[1])

plt.plot(theta, r)
plt.savefig("sortedpolcart.png")

plt.clf()
plt.polar(theta, r)
plt.savefig("sortedpolpol.png")