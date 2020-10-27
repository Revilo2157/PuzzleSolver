import EdgeType
import Edge

class EdgeCreator:
  
  def __init__(self, edgeType): 
    self.edgeType = edgeType

  # This function will return the four edges for the given puzzle Piece as a list 
  def retrieveEdges(puzzlePieceFile):
    # puzzlePieceFile will be the file we determine the edges for
    listOfEdges = [Edge(EdgeType.HEAD), Edge(EdgeType.FLAT)] 
    return listOfEdges

  