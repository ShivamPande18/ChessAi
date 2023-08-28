import chess
from evalChart import *
from piece import *

class Bot:

    def __init__(self,boardState,maxDepth):
        self.chessBoard = chess.Board()
        self.maxDepth = maxDepth
        self.boardState = boardState
        self._setBoardState()

        

    def calcMove(self,moveSan):
        self.chessBoard.push_san(moveSan)
        self._setBoardState()
        # botSan = str(self.bestMove())
        botSan = str(self.minMax(None, 1))
        self.chessBoard.push_san(self.chessBoard.san(chess.Move.from_uci(botSan)))
        self._setBoardState()
        return str(botSan)

    # def bestMoveRec(self, candidate, depth):
    #     if(depth == self.maxDepth or self.chessBoard.legal_moves.count() == 0): return self.evalPos()

    #     moveList = list(self.chessBoard.legal_moves)

    #     for i in moveList

    



    def minMax(self, candidate, depth):
        #reached max depth of search or no possible moves
        if (depth == self.maxDepth or self.chessBoard.legal_moves.count() == 0):
            return self.evalPos()

        else:
            moveList = (self.chessBoard.legal_moves)
            newCandidate = None

            if(depth % 2 != 0): newCandidate = float("-inf")
            else:   newCandidate = float("inf")


            for i in moveList:

                self.chessBoard.push(i)
                self._setBoardState()
                value = self.minMax(newCandidate, depth + 1)

                if(value > newCandidate and depth % 2 != 0):
                    if (depth == 1):    move = i
                    newCandidate = value
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value

                #Alpha-beta prunning cuts:
                # (if previous move was made by the engine)
                if (candidate != None and value < candidate and depth % 2 == 0):
                    self.chessBoard.pop()
                    self._setBoardState()
                    break
                #(if previous move was made by the human player)
                elif (candidate != None and value > candidate and depth % 2 != 0):
                    self.chessBoard.pop()
                    self._setBoardState()
                    break

                self.chessBoard.pop()
                self._setBoardState()

            #Return result
            if (depth > 1): return newCandidate
            else: return move


    def evalPos(self):  
        blackEval = 0
        whiteEval = 0
        col = "white"
        for i in range(8):
            for j in range(8):
                curPiece = str(self.boardState[i][j])
                curPnts = 0
                if(curPiece != "."):
                    if(curPiece.islower()):
                        if(curPiece.lower() == "p"): curPnts = Pawn(col).value      +  EvalChart().pawnChart[7-i][7-j]
                        elif(curPiece.lower() == "r"): curPnts = Rook(col).value    +  EvalChart().rookChart[7-i][7-j]
                        elif(curPiece.lower() == "n"): curPnts = Knight(col).value  +  EvalChart().knightChart[7-i][7-j]
                        elif(curPiece.lower() == "b"): curPnts = Bishop(col).value  +  EvalChart().bishopChart[7-i][7-j]
                        elif(curPiece.lower() == "q"): curPnts = Queen(col).value   +  EvalChart().queenChart[7-i][7-j]
                        elif(curPiece.lower() == "k"): curPnts = King(col).value    +  EvalChart().kingChart[7-i][7-j]
                        blackEval += curPnts
                    else:
                        if(curPiece.lower() == "p"): curPnts = Pawn(col).value      + EvalChart().pawnChart[i][j]
                        elif(curPiece.lower() == "r"): curPnts = Rook(col).value    + EvalChart().rookChart[i][j]
                        elif(curPiece.lower() == "n"): curPnts = Knight(col).value  + EvalChart().knightChart[i][j]
                        elif(curPiece.lower() == "b"): curPnts = Bishop(col).value  + EvalChart().bishopChart[i][j]
                        elif(curPiece.lower() == "q"): curPnts = Queen(col).value   + EvalChart().queenChart[i][j]
                        elif(curPiece.lower() == "k"): curPnts = King(col).value    + EvalChart().kingChart[i][j]
                        whiteEval += curPnts

        return float(blackEval - whiteEval)


    def _setBoardState(self):
        cords = []
        lines = str(self.chessBoard).split("\n")
        for line in range(len(lines)):
            cords.append(lines[line].split(" "))

        self.boardState = cords