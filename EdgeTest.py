import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
matplotlib.use('Agg')

def EdgeConvert(img):
  count = 0
  sum = [0, 0]
  edges = img.load()
	xpix = []
	ypix = []

  for x in range(img.size[0]):
    for y in range(img.size[1]):
      if (edges[x,y]):
        sum[0] += x
        sum[1] += y
				xpix.append(x)
				ypix.append(y)
        count += 1
  avg = [sum[0]/count, sum[1]/count]

	xsorted = []
	ysorted =[]
	for i in range(len(xpix)):
		dist = []
		for j in range(len(xpix)):
			if ((x[i] != x[j]) && (y[j] != y[i])):
				dist.append(np.sqrt((x[j] - x[i])**2 + (y[j] - y[i])**2))


  r = []
  theta = []

  for n in range(len(xpix)):
		thisr, thistheta = (cart2pol(xpix[n]-avg[0], ypix[n]-avg[1]))
		r.append(thisr)
		theta.append(thistheta)

  plt.plot(theta, r, "b")
  plt.savefig("polarPlot.png")


def cart2pol(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(r, theta)

def pol2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

EdgeConvert(Image.open("pieces/1-1edge.png"))