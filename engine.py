class GameState:
    def __init__(self):
        self.board = [['br', 'bh', 'bb', 'bq', 'bk', 'bb', 'bh', 'br'],
                 ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['--', '--', '--', '--', '--', '--', '--', '--'],
                 ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                 ['wr', 'wh', 'wb', 'wq', 'wk', 'wb', 'wh', 'wr']]
        self.whiteMove=True
        self.Log=[]
        self.whiteKing=(7,4)
        self.blackKing=(0,4)
        self.pins=[]
        self.checks=[]
        self.inCheck=False
        self.rightWhiteCastlingPossible=True
        self.leftWhiteCastlingPossible = True
        self.rightBlackCastlingPossible=True
        self.leftBlackCastlingPossible = True
        self.checkmate = False
        self.stalemate = False

    def makeMove(self,Move):
        self.board[Move.startRow][Move.startCol] = "--"
        self.board[Move.endRow][Move.endCol] = Move.pieceMoved
        self.Log.append(Move)
        self.whiteMove = not self.whiteMove

        if Move.pieceMoved == 'wk':
            self.whiteKing=(Move.endRow,Move.endCol)
            self.rightWhiteCastlingPossible=False
            self.leftWhiteCastlingPossible=False
        elif Move.pieceMoved == 'bk':
            self.blackKing = (Move.endRow, Move.endCol)
            self.rightBlackCastlingPossible=False
            self.leftBlackCastlingPossible=False
        if Move.pieceMoved == "wr":
            if Move.startRow==7 and Move.startCol==0:
                self.leftWhiteCastlingPossible=False
            elif Move.startRow==7 and Move.startCol==7:
                self.rightWhiteCastlingPossible=False
        if Move.pieceMoved == "br":
            if Move.startRow==0 and Move.startCol==0:
                self.leftBlackCastlingPossible=False
            elif Move.startRow==0 and Move.startCol==7:
                self.rightBlackCastlingPossible=False
        if Move.enpassantCapture:
            captured = Move.enpassantSquareCaptured
            self.board[captured[0]][captured[1]] = "--"
        if Move.castlingSquare!=():
            castle= Move.castlingSquare
            if castle[1] == 7:
                self.board[castle[0]][5] = self.board[castle[0]][7]
            elif castle[1] == 0:
                self.board[castle[0]][3] = self.board[castle[0]][0]
            self.board[castle[0]][castle[1]]="--"


        if Move.pawnPromotion:
            return True
        return False

    def promotePawn(self,r,c,choice):
        color = "b" if self.whiteMove else "w"
        self.board[r][c] = color +choice

    def undo(self):
        if len(self.Log) !=0:
            Move=self.Log.pop()
            self.board[Move.startRow][Move.startCol] = Move.pieceMoved
            self.board[Move.endRow][Move.endCol] = Move.pieceCaptured
            self.whiteMove = not self.whiteMove
            if Move.pieceMoved == 'wk':
                self.whiteKing = (Move.startRow, Move.startCol)
                self.leftWhiteCastlingPossible=Move.castlingStatusLeft
                self.rightWhiteCastlingPossible=Move.castlingStatusRight
            elif Move.pieceMoved == 'bk':
                self.blackKing = (Move.startRow, Move.startCol)
                self.leftBlackCastlingPossible = Move.castlingStatusLeft
                self.rightBlackCastlingPossible = Move.castlingStatusRight
            if Move.enpassantCapture:
                captured = Move.enpassantSquareCaptured
                self.board[captured[0]][captured[1]] = "bp" if  Move.pieceMoved == "wp" else "wp"

            if Move.pieceMoved == "wr":
                if Move.startRow == 7 and Move.startCol == 0 and Move.castlingStatusLeft:
                    self.leftWhiteCastlingPossible = True
                elif Move.startRow == 7 and Move.startCol == 7 and Move.castlingStatusRight:
                    self.rightWhiteCastlingPossible = True
            if Move.pieceMoved == "br":
                if Move.startRow == 0 and Move.startCol == 0 and Move.castlingStatusLeft:
                    self.leftBlackCastlingPossible = True
                elif Move.startRow == 0 and Move.startCol == 7 and Move.castlingStatusRight:
                    self.rightBlackCastlingPossible = True

            if Move.castlingSquare != ():
                castle = Move.castlingSquare
                if castle[1] == 7:
                    self.board[castle[0]][7]= self.board[castle[0]][5]
                    self.board[castle[0]][5] = "--"
                elif castle[1] == 0:
                    self.board[castle[0]][0] =self.board[castle[0]][3]
                    self.board[castle[0]][3] = "--"
            self.checkmate = False
            self.stalemate = False



    def getPawnMoves(self, r, c, moves):
        pinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1]==c:
                pinned=True
                pinDirection =(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        square = (-1,-1)
        if len(self.Log)>0:
            if self.Log[-1].enpassantSquare != ():
                square = self.Log[-1].enpassantSquare
        if self.whiteMove:
            if self.board[r-1][c] == "--" and (not pinned or pinDirection==(-1,0)) :
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c <7:
                if self.board[r-1][c+1][0] == 'b' and (not pinned or pinDirection==(-1,1)):
                    moves.append(Move((r, c), (r - 1, c+1), self.board))
            if c >0:
                if self.board[r-1][c-1][0] == 'b'and (not pinned or pinDirection==(-1,-1)):
                    moves.append(Move((r, c), (r - 1, c-1), self.board))

            if (square[1] == c-1 or square[1] == c+1) and square[0] == r-1:
                moves.append(Move((r, c), (square[0], square[1]), self.board, True))



        if not self.whiteMove:
            if self.board[r + 1][c] == "--" and (not pinned or pinDirection==(1,0)):
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c < 7:
                if self.board[r + 1][c + 1][0] == 'w' and (not pinned or pinDirection==(-1,1)):
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if c > 0:
                if self.board[r + 1][c - 1][0] == 'w' and (not pinned or pinDirection==(-1,-1)):
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if (square[0] == r+1 )and( square[1] == c-1 or square[1] == c+1):
                moves.append(Move((r, c), (square[0], square[1]), self.board,True))


    def getRookMoves(self, r, c, moves):
        pinned = False
        pinDirection = ()
        if len(self.pins)>0:
            for i in range(len(self.pins) - 1, -1, -1):
                if self.pins[i][0] == r and self.pins[i][1] == c:
                    pinned = True
                    pinDirection = (self.pins[i][2], self.pins[i][3])
                    if self.board[r][c][1]!= 'q':
                        self.pins.remove(self.pins[i])
                    break
        directions = ((1,0),(-1,0),(0,1),(0,-1))

        if self.whiteMove:
            CR=self.rightWhiteCastlingPossible
            CL = self.leftWhiteCastlingPossible
        else:
            CR=self.rightBlackCastlingPossible
            CL=self.leftBlackCastlingPossible

        if not pinned or pinDirection in directions[2:]:
            i=c+1
            while i<8:
                if self.board[r][i] == "--":
                    moves.append(Move((r, c), (r, i), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))
                    i += 1
                else:
                    break
            if i<8:
                if(self.board[r][i][0] == "b" and self.whiteMove) or (self.board[r][i][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (r, i), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))


            i = c-1
            while i>=0:
                if self.board[r][i] == "--":
                    moves.append(Move((r, c), (r, i), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))
                    i-=1
                else:
                    break
            if i>=0:
                if (self.board[r][i][0] == "b" and self.whiteMove) or (self.board[r][i][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (r, i), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))

        if not pinned or pinDirection in directions[:2]:
            i = r + 1

            while i < 8:
                if self.board[i][c] == "--":
                    moves.append(Move((r, c), (i, c), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))
                    i += 1
                else:
                    break

            if i < 8:
                if (self.board[i][c][0] == "b" and self.whiteMove) or (self.board[i][c][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (i, c), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))
            i = r-1

            while i>=0:
                if self.board[i][c] == "--":
                    moves.append(Move((r, c), (i, c), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))
                    i-=1
                else:
                    break
            if i>=0:
                if (self.board[i][c][0] == "b" and self.whiteMove) or  (self.board[i][c][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (i, c), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))


    def getBishopMoves(self, r, c, moves):
        pinned = False
        pinDirection = []
        if len(self.pins)>0:
            for i in range(len(self.pins) - 1, -1, -1):
                if self.pins[i][0] == r and self.pins[i][1] == c:
                    pinned = True
                    pinDirection = (self.pins[i][2], self.pins[i][3])
                    if self.board[r][c][1]!= 'q':
                        self.pins.remove(self.pins[i])
                    break
        directions = ((1,1),(-1,-1),(-1,1),(1,-1))

        if not pinned or pinDirection in directions[:2]:

            i = r - 1
            j = c - 1
            while i >= 0 and j >= 0:
                if self.board[i][j] == "--":
                    moves.append(Move((r, c), (i, j), self.board))
                    i -= 1
                    j -= 1
                else:
                    break
            if i >= 0 and j >= 0:
                if (self.board[i][j][0] == "b" and self.whiteMove) or (self.board[i][j][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (i, j), self.board))

            i = r + 1
            j= c+1
            while i < 8 and j <8:
                if self.board[i][j] == "--":
                    moves.append(Move((r, c), (i, j), self.board))
                    i += 1
                    j+=1
                else:
                    break
            if i < 8 and j<8:
                if (self.board[i][j][0] == "b" and self.whiteMove) or (self.board[i][j][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (i, j), self.board))
        if not pinned or pinDirection in directions[2:]:

            i = r - 1
            j = c + 1
            while i >= 0 and j < 8:
                if self.board[i][j] == "--":
                    moves.append(Move((r, c), (i, j), self.board))
                    i -= 1
                    j += 1
                else:
                    break
            if i >= 0 and j < 8:
                if (self.board[i][j][0] == "b" and self.whiteMove) or (self.board[i][j][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (i, j), self.board))
            i = r + 1
            j = c - 1
            while i < 8 and j >= 0:
                if self.board[i][j] == "--":
                    moves.append(Move((r, c), (i, j), self.board))
                    i += 1
                    j -= 1
                else:
                    break
            if i < 8 and j >= 0:
                if (self.board[i][j][0] == "b" and self.whiteMove) or (self.board[i][j][0] == "w" and not self.whiteMove):
                    moves.append(Move((r, c), (i, j), self.board))



    def getHorseMoves(self, r, c, moves):

        if len(self.pins) > 0:
            for i in range(len(self.pins) - 1, -1, -1):
                if self.pins[i][0] == r and self.pins[i][1] == c:
                    return
                    pinned = True
                    self.pins.remove(self.pins[i])
                    break

        for i in range(r-2,r+3):
            for j in range(c-2,c+3):
                if abs(i-r) + abs(j-c)==3 and i>=0 and j <8 and j>=0 and i <8:
                    if self.board[i][j] == "--" or (self.board[i][j][0] == "b" and self.whiteMove) or (self.board[i][j][0] == "w" and not self.whiteMove):
                        moves.append(Move((r, c), (i, j), self.board))

    def getKingMoves(self, r, c, moves):
        if self.whiteMove:
            CR=self.rightWhiteCastlingPossible
            CL =self.leftWhiteCastlingPossible
        else:
            CR = self.rightBlackCastlingPossible
            CL = self.leftBlackCastlingPossible
        for i in range(r-1,r+2):
            for j in range(c-1,c+2):
                if  i >= 0 and j < 8 and j >= 0 and i < 8:
                    if self.board[i][j] == "--" or (self.board[i][j][0] == "b" and self.whiteMove) or (self.board[i][j][0] == "w" and not self.whiteMove):
                        if self.whiteMove:
                            self.whiteKing = (i,j)
                        else:
                            self.blackKing = (i,j)
                        _,_,incheck = self.checkPinsChecks()
                        if not incheck:
                            moves.append(Move((r, c), (i, j), self.board,castlingStatusRight=CR,castlingStatusLeft=CL))

        #castling
        #check castling possibe
        #check free squares
        #check squares are not under attack
        # if self.whiteMove and (self.rightWhiteCastlingPossible or self.leftWhiteCastlingPossible):
        #     if self.board[7][1:4] == ("--","--","--"):
        #         checkFlag=False
        #         for i in range(1,4):
        #             self.whiteKing = (7, i)
        #             _, _, incheck = self.checkPinsChecks()
        #             if incheck:
        #                 checkFlag=True
        #         if not checkFlag:
        #             moves.append(Move((r, c), (i, j), self.board,False,(7,0),castlingStatusRight=CR,castlingStatusLeft=CL))
        #     if self.board[7][5:7] == ("--", "--"):
        #         checkFlag = False
        #         for i in range(5, 7):
        #             self.whiteKing = (7, i)
        #             _, _, incheck = self.checkPinsChecks()
        #             if incheck:
        #                 checkFlag = True
        #         if not checkFlag:
        #             moves.append(Move((r, c), (i, j), self.board, False, (7, 7),castlingStatusRight=CR,castlingStatusLeft=CL))
        row=7 if self.whiteMove else 0
        if (self.whiteMove and (self.rightWhiteCastlingPossible or self.leftWhiteCastlingPossible)) \
                or (not self.whiteMove and (self.rightBlackCastlingPossible or self.leftBlackCastlingPossible)):
            if self.board[row][1:4] == ["--","--","--"]:
                checkFlag=False
                for i in range(1,4):
                    if self.whiteMove:
                        self.whiteKing = (row, i)
                    else:
                        self.blackKing = (row,i)
                    _, _, incheck = self.checkPinsChecks()
                    if incheck:
                        checkFlag=True
                if not checkFlag:
                    moves.append(Move((r, c), (row, 2), self.board,False,(row,0),castlingStatusRight=CR,castlingStatusLeft=CL))
            if self.board[row][5:7] == ["--", "--"]:
                checkFlag = False
                for i in range(5, 7):
                    if self.whiteMove:
                        self.whiteKing = (row, i)
                    else:
                        self.blackKing = (row, i)
                    _, _, incheck = self.checkPinsChecks()
                    if incheck:
                        checkFlag = True
                if not checkFlag:
                    moves.append(Move((r, c), (row, 6), self.board, False, (row, 7),castlingStatusRight=CR,castlingStatusLeft=CL))
        if self.whiteMove:
            self.whiteKing = (r, c)
        else:
            self.blackKing = (r, c)





    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)


    def checkPinsChecks(self):
        pins=[]
        checks=[]
        incheck=False
        if self.whiteMove:
            color = "w"
            enemyColor = "b"
            col = self.whiteKing[1]
            row=self.whiteKing[0]
        else:
            color = "b"
            enemyColor = "w"
            col = self.blackKing[1]
            row = self.blackKing[0]

        directions = ((-1,0),(1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1))
        for j in range(len(directions)):
            d=directions[j]
            possiblePin=()
            for i in range(1,8):
                endrow=row+i*d[0]
                endcol=col+i*d[1]
                if 0<=endrow<8 and 0<=endcol<8:
                    endPiece=self.board[endrow][endcol]
                    if  endPiece[0]==color and endPiece[1]!='k':
                        if possiblePin==():
                            possiblePin=(endrow,endcol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0]==enemyColor:
                        type = endPiece[1]
                        if (0<=j<4 and type=="r") or (4<=j<8 and type=='b') or type=='q' or \
                            (i==1 and type=='p' and ((enemyColor=='b' and 6<=j<=7)or (enemyColor=='w' and 4<=j<=5))) \
                             or (i==1 and type =='k'):
                            if possiblePin==():
                                incheck=True
                                checks.append((endrow,endcol,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
        directions = ((-2,-1),(2,-1),(-2,1),(2,1),(-1,-2),(1,-2),(-1,2),(1,2))
        for d in directions:
            endrow = row + d[0]
            endcol = col + d[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endPiece=self.board[endrow][endcol]
                if (enemyColor=='w' and endPiece=='wh') or (enemyColor=='b' and endPiece=='bh'):
                    incheck = True
                    checks.append((endrow, endcol, d[0], d[1]))
        return checks,pins,incheck




    def getValidMoves(self):
        moves = []
        self.checks,self.pins,self.inCheck=self.checkPinsChecks()
        kL = self.whiteKing if self.whiteMove else self.blackKing
        if self.inCheck:
            if len(self.checks)==1:
                moves= self.validMoves()
                check=self.checks[0]
                pieceChecking = self.board[check[0]][check[1]]
                validSquares =[] # check if checks working correctly (and why not
                if pieceChecking[1]=='h':
                    validSquare = [check[0],check[1]]
                else:
                    for i in range(1,8):
                        validSquare = (kL[0] + check[2]*i,kL[1] + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0]==check[0] and validSquare[1] == check[1]:
                            break
                    for i in range(len(moves)-1,-1,-1):
                        if moves[i].pieceMoved[1] !='k':
                            if not (moves[i].endRow ,moves[i].endCol) in validSquares:
                                moves.remove(moves[i])

            else:
                self.getKingMoves(kL[0],kL[1],moves)
        else:
            moves= self.validMoves()
        if moves ==[]:
            if self.inCheck:
                self.checkmate=True
            else:
                self.stalemate=True
        return moves



    def validMoves(self):
        moves =[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    piece = self.board[r][c][1]
                    if piece =='p':
                        self.getPawnMoves(r,c,moves)
                    elif piece == 'r':
                        self.getRookMoves(r,c,moves)
                    elif piece== 'b':
                        self.getBishopMoves(r,c,moves)
                    elif piece== 'q':
                        self.getQueenMoves(r, c,moves)
                    elif piece== 'k':
                         self.getKingMoves(r,c,moves)
                    elif piece== 'h':
                         self.getHorseMoves(r, c,moves)
        return moves






class Move:

    ranksToRows={
        "1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0
    }
    filesToCols = {
        "h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0
    }
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    colstoFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self,startSQ,endSQ,board, enpassantCapture = False, castling = (),castlingStatusRight=False,castlingStatusLeft=False):
        self.startRow=startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.endSQ = endSQ
        self.pawnPromotion=False
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow *1000 + self.startCol*100  + self.endRow*10 + self.endCol
        self.enpassantSquare = ()
        if (self.pieceMoved=='wp' and self.startRow ==6 and self.endRow ==4) or \
                                (self.pieceMoved == 'bp' and self.startRow == 1 and self.endRow == 3):
            newRow = 5 if self.pieceMoved == 'wp' else 2
            self.enpassantSquare = (newRow,self.endCol)
        self.enpassantCapture=enpassantCapture
        self.enpassantSquareCaptured = (3,self.endCol) if self.endRow == 2 else (4,self.endCol)
        self.castlingSquare=castling
        self.castlingStatusRight=castlingStatusRight
        self.castlingStatusLeft = castlingStatusLeft
        self.pawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (
                self.pieceMoved == 'bp' and self.endRow == 7)

    def getChessNotation(self):
        return self.pieceMoved[1]+ self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colstoFiles[c] + self.rowsToRanks[r]

    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False








