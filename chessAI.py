
import random

pieceScore= {"k":0, "q":10,"r":5,"b":3,"h":3,"p":1}
CHECKMATE=1000
STALEMATE=0
DIMENTION=8
def scoreMaterial(board):
    Score=0
    for i in range(DIMENTION):
        for j in range(DIMENTION):
            if board[i][j][0]=="w":
                Score += pieceScore[board[i][j][1]]
            elif board[i][j][0] =="b":
                Score-=pieceScore[board[i][j][1]]
    return Score


def findRandomMove(validMoves):
    move = validMoves[random.randint(0,len(validMoves)-1)]
    return move

def findBestMove(gs,validMoves,steps):
    turnMultiplier=1 if gs.whiteMove else -1
    maxScore= -CHECKMATE
    bestMove=None

    random.shuffle(validMoves)
    for move in validMoves:
        pawnPromoted = gs.makeMove(move)
        if (pawnPromoted):
            gs.promotePawn(move.endRow, move.endCol, "q")
            board = gs.board
        if steps>0:
            newValidMoves = gs.getValidMoves()
            opponentMove,score=findBestMove(gs,newValidMoves,steps-1)
            score = -score
        else:
            score = scoreMaterial(gs.board)*turnMultiplier
        if gs.checkmate:
            score = CHECKMATE
        if gs.stalemate:
            score = STALEMATE
        if score>maxScore:
            maxScore=score
            bestMove=move
        if pawnPromoted:
            gs.board=board
        gs.undo()

    return bestMove,maxScore


#not relevant

