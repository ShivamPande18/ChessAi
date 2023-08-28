class Conversion:

    def __init__(self):
        pass

    def cordToNotation(self, x, y):
        notationAlpha = ["a", "b", "c", "d", "e", "f", "g", "h"]
        notation = str(notationAlpha[x]) + str(8-y)
        return notation

    def notationToCords(self,notation):
        notation = str(notation)
        notationAlpha = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if(len(notation) == 3): notation = notation[1:]
        cordX = int(notationAlpha.index(notation[0]))
        cordY = 8 - int(notation[1])

        cord = [cordX,cordY]

        return cord
