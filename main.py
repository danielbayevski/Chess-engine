
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pygame as pg
import engine
import chessAI
WIDTH=HEIGHT = 512
DIMENTION=8
SQ_SIZE = HEIGHT//DIMENTION
MAX_FPS=15
STEPS=3


light_col = [75,125,75]
dark_col = [0,50,0]
darken_col = [25,0,100]
brighten_col = [100,0,100]
squareSize = 10

IMAGES = {}




def loadImages():
    piece = ['wp','wq','wk','wh','wb','wr','bp','bq','bk','bh','bb','br']
    for i in piece:
        IMAGES[i] = pg.image.load("piece/"+i+".png")



#graphics........................

def drawBoard(screen):
    color = [pg.Color(light_col),pg.Color(dark_col)]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            col = color[(r+c)%2]
            pg.draw.rect(screen,col,pg.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def endgame(gs):
    pass



def drawPieces(screen,board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece!='--':
                screen.blit(IMAGES[piece],pg.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawText(string,screen):
    font = pg.font.SysFont("Helvatica",32,True)
    text = font.render(string,0,pg.Color('black'))
    location = pg.Rect(0,0,WIDTH,HEIGHT).move((WIDTH-text.get_width())/2,(HEIGHT-text.get_height())/2)
    screen.blit(text,location)
    text = font.render(string, 0, pg.Color('grey'))
    location = pg.Rect(0, 0, WIDTH, HEIGHT).move((WIDTH - text.get_width()) / 2 +2, (HEIGHT - text.get_height()) / 2 +2)
    screen.blit(text, location)



def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)

def animateMove(move,screen,board,clock):
    colors = [pg.Color(light_col), pg.Color(dark_col)]
    dR = move.endRow-move.startRow
    dC= move.endCol-move.startCol
    FPS = 10
    frameCount = FPS*(abs(dR) + abs(dC))
    for frame in range(frameCount+1):
        r,c = (move.startRow+dR*frame/frameCount,move.startCol+dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow+move.endCol)%2]
        endSquare = pg.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        moveSquare = pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen,color,endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
        screen.blit(IMAGES[move.pieceMoved],moveSquare)
        pg.display.flip()
        clock.tick(frameCount*10)



#..................................


def main():



    pg.init()

    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = engine.GameState()
    loadImages()
    validMoves=gs.validMoves()
    validMove=False
    sqSelected =()
    playerClicks = []
    gameOver=False
    playerOne=True
    playerTwo=False
    running = True
    while running:
        humanTurn = (playerOne and gs.whiteMove) or (playerTwo and not gs.whiteMove)
        for e in pg.event.get():
            if humanTurn:
                if e.type == pg.QUIT:
                    running=False
                elif e.type == pg.MOUSEBUTTONDOWN:
                    if not gameOver:
                        location = pg.mouse.get_pos() #x,y posiotion
                        col = location[0]//SQ_SIZE
                        row = location[1]//SQ_SIZE

                    if sqSelected == (row,col):
                        sqSelected =()
                        playerClicks=[]
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks)==2: #after 2nd click
                        move = engine.Move(playerClicks[0],playerClicks[1],gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                pawnPromotion=gs.makeMove(validMoves[i])
                                validMove=True
                                print(move.getChessNotation())
                                sqSelected=()
                                playerClicks=[]
                                if pawnPromotion:
                                    gs.promotePawn(move.endRow,move.endCol,"q")
                        if not validMove:
                            playerClicks=[sqSelected]

                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_z:
                        gs.undo()
                        validMoves = gs.getValidMoves()
                    elif e.key==pg.K_r:
                        gs = engine.GameState()
                        validMoves = gs.validMoves()
                        validMove = False
                        sqSelected = ()
                        playerClicks = []

        if not gameOver and not humanTurn:
            AIMove = chessAI.findBestMove(gs,validMoves,STEPS)[0]
            if AIMove==None:
                AIMove = chessAI.findRandomMove(validMoves)
            if gs.makeMove(AIMove):
                gs.promotePawn(move.endRow, move.endCol, "q")
            validMove = True
            move = AIMove

        if validMove:
            animateMove(move,screen,gs.board,clock)
            validMoves=gs.getValidMoves()
            validMove=False
            if validMoves== []:
                endgame(gs)


        drawGameState(screen,gs,validMoves,sqSelected)
        if gs.checkmate:
            gameOver=True
            if gs.whiteMove:
                drawText("black win",screen)
            else:
                drawText("white win",screen)
        elif gs.stalemate:
            gameOver=False
            drawText("stalemate",screen)
        clock.tick(MAX_FPS)
        pg.display.flip()

def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected!=():
        r,c=sqSelected
        if gs.board[r][c][0]==( 'w' if gs.whiteMove else 'b'):
            s = pg.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(pg.Color(darken_col))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(pg.Color(brighten_col))
            for move in validMoves:
                if move.startRow == r and move.startCol==c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


