import pygame
import sys

from const import *
from game import Game
from conversion import *


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.conversion = Conversion()
        self.canChoosePiece = True

    
    def mainLoop(self):

        screen = self.screen
        game = self.game
        canChoosePiece = self.canChoosePiece
        conversion = self.conversion

        while True:

            game.show_bg(screen)
            game.show_pieces(screen)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()
                    cordX = pos[0]//SQSIZE
                    cordY = pos[1]//SQSIZE

                    if canChoosePiece:
                        currPiece = game.boardState[cordY][cordX]
                        if(currPiece == "."):
                            pass
                        else:
                            pieceNotation = game.boardState[cordY][cordX]
                            if pieceNotation.lower() == "p":pieceNotation = ""

                            # print(pieceNotation)
                            posNotation = conversion.cordToNotation(cordX, cordY)
                            # print(posNotation)
                            game.show_next_move(posNotation, screen)
                            canChoosePiece = False

                    else:
                        currPiece = game.boardState[cordY][cordX]

                        if((currPiece.isupper() and game.isWhite) or (currPiece.islower() and not game.isWhite)):
                            pieceNotation = game.boardState[cordY][cordX]
                            if pieceNotation.lower() == "p":
                                pieceNotation = ""

                            # print(pieceNotation)
                            posNotation = conversion.cordToNotation(
                                cordX, cordY)
                            # print(posNotation)
                            game.show_next_move(posNotation, screen)
                            canChoosePiece = False
                        else:
                            game.make_move(posNotation, pieceNotation, [cordX, cordY])
                            canChoosePiece = True


                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()



main = Main()
main.mainLoop()