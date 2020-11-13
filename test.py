from Library import iter0, iter1, iter01
from PIL import Image
from PuzzlePiece import PuzzlePiece 

import matplotlib.pyplot as plt
import matplotlib

pieces = []
for n in range(54):
    print("\t%2d" % n, end="\r")
    piece = PuzzlePiece(n + 1)
    for edge in piece.edges:
        x = [point[0] for point in edge.points]
        y = [point[1] for point in edge.points]

        plt.clf()
        plt.plot(x,y)
        plt.savefig("test/%d-%s.png" % (n+1, edge.side.name))
