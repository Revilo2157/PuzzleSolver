import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
matplotlib.use('Agg')

def EdgeConvert(img):
  count = 0
  sum = [0, 0]
  edges = img.load()
  for x in range(img.size[0]):
    for y in range(img.size[1]):
      if (edges[x,y]):
        sum[0] += x
        sum[1] += y
        count += 1
  avg = [sum[0]/count, sum[1]/count]

  r = []
  theta = []
  for x in range(img.size[0]):
    for y in range(img.size[1]):
      if (edges[x,y]):
        thisr, thistheta = (cart2pol(x-avg[0], y-avg[1]))
        r.append(thisr)
        theta.append(thistheta)

  plt.plot(theta, r, "bo")
  plt.savefig("polar.png")



def cart2pol(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(r, theta)

def pol2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

EdgeConvert(Image.open("pieces/1-1edge.png"))