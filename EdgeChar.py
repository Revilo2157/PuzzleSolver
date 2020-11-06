import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
#---------------------------------
def distance(a, b):
	return np.sqrt((a[1] - b[1])**2 + (a[0] - b[0])**2)

def EdgeConvert(img):
  matplotlib.use('Agg')

  #mg = Image.open("pieces/1-3edge.png")
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
  count = 0
  sum = [0, 0]
  edges = img.load()
  #avg = [sum[0]/count, sum[1]/count]


  #r, theta = sortPol(r, theta)

#the good shit:
  plt.polar(theta, r, "b")
  plt.savefig("polar.png")
  plt.clf()
  plt.plot(theta, r, "b")
  plt.savefig("cart.png")
  plt.clf()

  
  z1 = []
  z2 = []
  z3 = []
  z4 = []
  z1t = []
  z2t = []
  z3t = []
  z4t = []
  #plt.plot(x, y, "g")
  #plt.savefig("xy.png")
  i = 0
  for sweep in theta:
    #ZONE 1
    if (sweep > -np.pi/4 and sweep < 0) or (sweep < np.pi/4 and sweep > 0):
      z1.append(r[i])
      z1t.append(theta[i])
      #Z.append(r[i])
    #ZONE 2
    elif sweep > np.pi/4 and sweep < 3*np.pi/4:
      z2.append(r[i])
      #Z.append(r[i])
      z2t.append(theta[i])
    #ZONE 3
    elif sweep > 3*np.pi/4 or sweep < -3*np.pi/4:
      z3.append(r[i])
      z3t.append(theta[i])
    #ZONE 4
    elif sweep > -3*np.pi/4 and sweep < -np.pi/4:
      z4.append(r[i])
      z4t.append(theta[i])
    i += 1
  #print(theta)
  #print(z1)
  charZone(z1,z1t)
  charZone(z2,z2t)
  charZone(z3,z3t)
  charZone(z4,z4t)
  #print(z2)
  #plt.polar(z2t, z2, "r")
  #plt.polar(z3t, z3, "k")
  #plt.savefig("polar.png")
def charZone(zone,theta):
  cornR = []
  cornT = []
  #put corner r, theta into lists
  cornR.append(zone[0])
  cornR.append(zone[len(zone) - 1])  
  cornT.append(theta[0])
  cornT.append(theta[len(theta) - 1])  

  cornCart = []
  (x,y) = pol2cart(cornR,cornT)
  cX = x
  cY = y

  (x,y) = pol2cart(zone,theta)
  zX = x
  zY = y

  vert = 0
  horiz = 0

  i = 0
  while True:
    
    if zX[i] == zX[i + 1] and zY[i] != zY[i + 1]:
      vert = 1
      break
    elif zX[i] != zX[i + 1] and zY[i] == zY[i + 1]:
      horiz = 1
      break
    i += 1
    if i > len(zX):
      print("fuck")
      break
  
  delta = 20

  xmax = np.amax(zX)
  xmin = np.amin(zX)
  xAv = np.average(zX)
  ymax = np.amax(zY)
  ymin = np.amin(zY)
  yAv = np.average(zY)

  if vert == 1 and ymax > yAv + delta:
    print("vHEAD")
  elif vert == 1 and ymin < yAv - delta:
    print("vHOLE")
  elif horiz == 1 and xmax > xAv + delta:
    print("hHEAD")
  elif horiz == 1 and xmin < xAv - delta:
    print("hHole")
  else:
    print("EDGE")
  

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

EdgeConvert(Image.open("pieces/2-2edge.png"))