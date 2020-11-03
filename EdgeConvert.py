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


  plt.polar(theta, r, "b")
  plt.savefig("polar.png")
  plt.clf()
  plt.plot(theta, r, "b")
  plt.savefig("cart.png")
  plt.clf()

  newR = []
  for i in range(numTheta):
    newR.append(0)
  newTheta = []

  loop = 0
  for i in range(numTheta):
    shift = i + offset
    shiftt = theta[i] + np.pi/4
    if shiftt > 2*np.pi:
      shiftt -= 2*np.pi
    if shift > numTheta - 1:
      shift = 0
      loop += 1
    newTheta.append(shiftt)
    newR[i] = r[shift]

  plt.plot(newTheta, newR, "b")
  plt.savefig("cart3.png")

  plt.clf()

  nearest = find_nearest(theta, np.pi/4)
  r2 = r[nearest:]
  r2.extend(r[:nearest])

  plt.plot(theta, r2, "b")
  plt.savefig("cart2.png")

  plt.clf()

  plt.polar(theta, r2, "b")
  plt.savefig("polar2.png")

  plt.clf()

  #plt.plot(x, y, "g")
  #plt.savefig("xy.png")

  plt.polar(newTheta, newR, "b")
  plt.savefig("polar3.png")

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

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

#EdgeConvert(Image.open("pieces/1-1edge.png"))