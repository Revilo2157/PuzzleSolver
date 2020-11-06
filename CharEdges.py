from Library import *
import numpy as np

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')

# for col in range(9):
# 	for row in range(6):
def characterizeEdges(row, col):
	plt.clf()

	sorted = parameterize(row, col)
	corners = findCorners(sorted)

	x = [point[0] for point in sorted]
	y = [point[1] for point in sorted]	

	indices = []
	cx, cy = (0,0)
	for point in corners:
		cx += point[0]
		cy += point[1]
		indices.append(sorted.index(point))

	cx = cx / 4
	cy = cy / 4

	mindex = np.min(indices)

	edges = []

	for n in range(len(indices)):
		first = indices[n]
		x1, y1 = corners[n]

		if n == len(indices) - 1:
			second = indices[0]
			x2, y2 = corners[0]

		else:
			second = indices[n + 1]
			x2, y2 = corners[n + 1]


		if second == mindex:
			edge = sorted[first:] + sorted[:second + 1]
		else:
			edge = sorted[first:second + 1]

		#print(x1, x2, y1, y2, cx, cy)
		print("\t\t", end="")

		if sign(x1 - cx) == sign(x2 - cx):
			loc = "Left" if x1 - cx < 0 else "Right"
			edges.append(
				[sign(x1 - cx)*(point[0] - closest(x1, x2, cx)) 
				for point in edge])

			textx = closest(x1, x2, cx) #x1 + sign(x1 - cx)*25
			texty = cy

		elif sign(y1 - cy) == sign(y2 - cy):
			loc = "Bottom" if y1 - cy < 0 else "Top"
			edges.append(
				[sign(y1 - cy)*(point[1] - closest(y1, y2, cy)) 
				for point in edge])

			texty = closest(y1, y2, cy) #y1 + sign(y1 - cy)*25
			textx = cx

		else:
			print("Incorrect Corners")

		offset = edges[n]	
		mean = np.mean(offset)
		median = np.median(offset)

		if abs(mean - median) < 1:
			text = "Flat"
		else:
			text = "Head" if mean > median else "Hole"

		print("{:<6}: {:4}".format(loc, text))

	# 	x = [point[0] for point in edge]
	# 	y = [point[1] for point in edge]	

	# 	plt.plot(x, y)
	# 	plt.axis("equal")
	# 	plt.text(textx, texty, text, bbox=dict(facecolor='white', alpha=0.5))
	# plt.savefig("pieces/%d-%dchar.png" % (col + 1, row + 1))

# for col in range(9):
# 	for row in range(6):
# 		print("%d-%d" % (col + 1, row + 1))
# 		characterizeEdges(row, col)