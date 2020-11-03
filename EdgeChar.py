import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
"""matplotlib.use('Agg')

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
"""
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


  """nearest = find_nearest(theta, np.pi/4)
  r2 = r[nearest:]
  r2.extend(r[:nearest])

  plt.plot(theta, r2, "b")
  plt.savefig("cart2.png")

  plt.clf()

  plt.polar(theta, r2, "b")
  plt.savefig("polar2.png")"""

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

  
def charZone(zone,theta):
  cornLen = []
  #r, theta = sortPol(r, theta)
  
  i = 0
  """for j in range(len(theta)):
    while zone[j] not in cornLen and len(cornLen) < 2:
      if theta[j] > -3*np.pi/4: #and j == 0:
        cornLen.append(zone[j])
        break
      elif theta[j] > -1*np.pi/4: #and j == 1:
        cornLen.append(zone[j])
        break
      elif theta[j] > np.pi/4: #and j == 2:
        cornLen.append(zone[j])
        break
      elif theta[j] > 3*np.pi/4: #and j == 3:
        cornLen.append(zone[j])
        break"""
  cornLen.append(zone[0])
  cornLen.append(zone[len(zone) - 1])  
    
  delta = 3
  avCorn = np.average(cornLen)
  av = np.average(zone)
  med = np.median(zone)
  #print(avCorn)
  print(cornLen)
  headLim = avCorn #+ delta
  holeLim = avCorn - delta
  max = np.amax(zone)
  #print(max)
  #print(np.amin(cornLen))
  min = np.amin(zone)
  #print(min)
  cornMin = np.amin(cornLen)
  cornMax = np.amax(cornLen)
  print("AvCorner: " + str(avCorn) + "\navSide: " + str(av) + "\nmedian: " + str(med) + "\nmin: " + str(min) + "\nmax: " + str(max))
  #if min < avSide - delta and max > avSide + delta:
  #  print("EDGE")
  minDif = abs(min - cornMin)
  maxDif = abs(max - cornMax)
  print(minDif)
  print(maxDif)
  if max > np.amax(cornLen) + delta and min == np.amin(cornLen) - delta:
    print("HEAD1")
  elif min < np.amin(cornLen) - delta and max == np.amax(cornLen):
    print("HOLE1")
  elif minDif > maxDif:
    print("HOLE2")
  elif minDif < maxDif:
    print("HEAD2")
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



EdgeConvert(Image.open("pieces/5-5edge.png"))