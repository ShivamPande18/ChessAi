import pygame
import chess
import random

from bot import *
from const import *
from piece import *
from conversion import *

class Game:


    def __init__(self):
        # self.chessBoard = chess.Board("rn1qkbnr/2ppppPp/p7/1p6/8/5b2/PPPPPP1P/RNBQKBNR w KQkq - 1 5")
        # print(self.getLegalMoves())
        data = "1r4r1/1p1nk2p/p7/4p3/2B1P1p1/1PN2N2/P1PR1PRP/2K5 b - - 0 22"
        self.chessBoard = chess.Board()
        self.boardState = [[]]
        # self.chessBoard.push_san("gxh8=N")
        # self.chessBoard.push_san(self.chessBoard.san(chess.Move.from_uci("e1g1")))
        self._setBoardState()
        self.conversion = Conversion()
        self.nextMove = []
        self.isWhite = True
        self.bot = Bot(self.boardState,4)
    
    def _setBoardState(self):
        cords = []
        lines = str(self.chessBoard).split("\n")
        for line in range(len(lines)):
            cords.append(lines[line].split(" "))

        self.boardState = cords


    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if([col,row] in self.nextMove):
                    color = NEXT_MOVE_COLOR
                elif((row+col)%2==0):
                    color = LIGHT_TILE
                else:
                    color = DARK_TILE

                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self,surface):

        for row in range(ROWS):
            for col in range(COLS):

                pieceChar = self.boardState[row][col]

                if(pieceChar!="."):
                    pieceColor = "white" if pieceChar.isupper() else "black"

                    if(pieceChar.lower() == "r"): piece = Rook(pieceColor)
                    elif(pieceChar.lower() == "n"): piece = Knight(pieceColor)
                    elif(pieceChar.lower() == "b"): piece = Bishop(pieceColor)
                    elif(pieceChar.lower() == "q"): piece = Queen(pieceColor)
                    elif(pieceChar.lower() == "k"): piece = King(pieceColor)
                    elif(pieceChar.lower() == "p"): piece = Pawn(pieceColor)
                    else: pass
                    


                    img = pygame.image.load(piece.texture)
                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)

                # print(self.boardState[row][col] , end= " ")
                

                # if self.boardState[row][col] != ".":

                #     piece = self.board.squares[row][col].piece
                #     # piece.set_texture(size=80)
                #     img = pygame.image.load(piece.texture)
                #     img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                #     piece.texture_rect = img.get_rect(center=img_center)
                #     surface.blit(img, piece.texture_rect)

    def getLegalMoves(self):
        legalMoves = self.chessBoard.legal_moves
        return legalMoves

    def show_next_move(self, posNotation, surface):
        self.nextMove.clear()
        for move in self.getLegalMoves():
            move = str(move)
            if(move[:2] == posNotation):
                if(len(move) == 5 ): 
                    move = move[:4]
                try:
                    cord = (self.conversion.notationToCords(move[2:]))
                except:
                    print(move)
                self.nextMove.append(cord)

    def make_move(self, posNotation, pieceNotation, cord):
        
        if(cord in self.nextMove):
            if(str(pieceNotation) == "" and cord[1] == 0):
                print(posNotation)
                notation = posNotation[0] + "x" + self.conversion.cordToNotation(cord[0], cord[1]) + "=Q"
                self.chessBoard.push_san(notation)
            else:
                notation = str(posNotation) + self.conversion.cordToNotation(cord[0],cord[1])
                try:
                    moveSan = self.chessBoard.san(chess.Move.from_uci(notation))
                    self.chessBoard.push_san(moveSan)
                    self.evalPos()
                    self._setBoardState()
                    self.nextMove.clear()
                    botSan = (str(self.bot.calcMove(moveSan)))
                    self.chessBoard.push_san(self.chessBoard.san(chess.Move.from_uci(botSan)))
                    self._setBoardState()
                    return
                except Exception as e:
                    print("\n" + notation)
                    print("\nError " + str(e))
                    self.nextMove.clear()
                    return


            

        print("can not move")
        self.nextMove.clear()
            # move = pieceNotation + 
            # self.chessBoard.push_san(move)
            # self._setBoardState()

    def make_bot_move(self):
        legalMoves = self.getLegalMoves()
        if(len(list(legalMoves))<=0): return

        ind = 0
        moveInd = random.randrange(0, len(list(legalMoves)))
        for move in legalMoves:
            move = str(move)
            if(ind == moveInd): 
                cord = self.conversion.notationToCords(move[:2])
                pieceNotation = str(self.boardState[cord[1]][cord[0]]).upper()
                if(pieceNotation.lower() == "p"): pieceNotation = ""
                try:
                    self.chessBoard.push_san(pieceNotation + move[2:])
                    self._setBoardState()
                    self.isWhite = not self.isWhite
                    self.evalPos()
                    return
                except Exception as e:
                    print("\n"+move[2:])
                    print("\n"+ str(e))
                    return
                
                
            ind+=1

    def evalPos(self):
        if(self.chessBoard.is_checkmate()): 
            winner = "black"
            if(self.isWhite): winner  = "white"
            print(f"Won by {winner}")
        pass