import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
matplotlib.use('Agg')

def EdgeConvert(img):
  count = 0
  sum = [0, 0]
  edges = img.load()
  x = []
  y = []

  for i in range(img.size[0]):
    for j in range(img.size[1]):
      if (edges[i,j]):
        x.append(i)
        y.append(j)
        sum[0] += i
        sum[1] += j
        count += 1
  avg = [sum[0]/count, sum[1]/count]

  r = []
  theta = []
  for i in range(len(x)):
    thisr, thistheta = (cart2pol(x[i]-avg[0], y[i]-avg[1]))
    r.append(thisr)
    theta.append(thistheta)

  numTheta = len(theta)
  qTheta = numTheta / 4
  offset = int(numTheta / 8)

  r, theta = sortPol(r, theta)

  newR = []
  newTheta = []

  loop = 0
  for i in range(numTheta):
    shift = i + offset
    shiftt = theta[i] + offset
    if shiftt > 360:
      shiftt -= 360
    if shift > numTheta - 1:
      shift = 0
      loop += 1
    newTheta.append(shiftt)
    newR.append(r[shift])

  plt.plot(newTheta, newR, "b")
  plt.savefig("cart.png")

  plt.clf()

  #plt.plot(x, y, "g")
  #plt.savefig("xy.png")

  plt.polar(newTheta, newR, "b")
  plt.savefig("polar.png")

def sortPol(r, theta):
  data = [(r[x], theta[x]) for x in range(len(r))]
  data.sort(key=iter)
  return [n[0] for n in data], [n[1] for n in data]

def iter(item):
  return item[1]

def cart2pol(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(r, theta)

def pol2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

#EdgeConvert(Image.open("pieces/1-1edge.png"))