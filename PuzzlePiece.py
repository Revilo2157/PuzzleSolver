from PIL import Image, ImageFilter
#import EdgeCreator

class PuzzlePiece:

  def __init__(self, fileName): 
    self.fileName = fileName
    self.maskFileName = fileName.replace(".png", "mask.png")
    self.edgeFileName = fileName.replace(".png", "edge.png")
    self.getEdges()
    # self.classifyEdges()
    
  

  topEdge = 0
  leftEdge = 0
  bottomEdge = 0
  rightEdge = 0

  fileName = ""
  maskFileName = ""
  edgeFileName = ""
  opened = False

  def getEdges(self):
    file = self.open()
    fPix = file.load()
    mask = Image.new("RGBA", (file.size[0], file.size[1]))
    blackWhite = mask.load()
    for x in range(file.size[0]):
      for y in range(file.size[1]):
        if fPix[x, y][3] != 0:
          blackWhite[x, y] = (255, 255, 255, 255)
        else:
          blackWhite[x, y] = (0, 0, 0, 0)
    mask.save(self.maskFileName)
    mask.filter(ImageFilter.FIND_EDGES).convert("L").save(self.edgeFileName)
    # edges = mask.filter(ImageFilter.FIND_EDGES).convert("L")

  def open(self):
    self.opened = True
    return Image.open(self.fileName)

  # def classifyEdges(puzzlePieceFile):
  #   # write code here to classify each edge
  #   edgeCreator = EdgeCreator()
  #   edgesList = edgeCreator.retrieveEdges()
  #   topEdge = edgesList.get(0)
  #   leftEdge = edgesList.get(1)
  #   bottomEdge = edgesList.get(2)
  #   rightEdge = edgesList.get(3)
