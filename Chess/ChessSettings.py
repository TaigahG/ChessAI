from const import *
class gamState():
    def __init__(self):
        self.board = [
        ["BR","BN","BB","BQ","BK","BB","BN","BR"],
        ["BP","BP","BP","BP","BP","BP","BP","BP"],
        ["..","..","..","..","..","..","..",".."],
        ["..","..","..","..","..","..","..",".."],
        ["..","..","..","..","..","..","..",".."],
        ["..","..","..","..","..","..","..",".."],
        ["WP","WP","WP","WP","WP","WP","WP","WP"],
        ["WR","WN","WB","WQ","WK","WB","WN","WR"]
        ]
        self.WhiteMove = True
        self.WKLoc = (7,4)
        self.BKLoc = (0,4)
        self.isCheck = False
        self.check = []
        self.pin = []
        self.moveLog = []
        self.movesFunc = {"P": self. PawnM, "R": self. RookM, "N": self. KnightM, 
                        "B": self. BishopM, "Q": self. QueenM, "K": self. KingM}
        self.CurrentCastle = Castle(True, True, True, True)
        self.CastleLog = [Castle(self.CurrentCastle.WK, self.CurrentCastle.BK,self.CurrentCastle.WQ,self.CurrentCastle.BQ)]
        self.Checkm8 = False
        self.Stalem8 = False
    def makesMove(self, move):
        self.board[move.StrtR][move.StrtC] = '..'
        self.board[move.EndR][move.EndC] = move.Moved
        self.moveLog.append(move)
        self.WhiteMove = not self.WhiteMove
        if move.Moved == 'WK':
            self.WKLoc = (move.EndR, move.EndC)
        elif move.Moved == "BK":
            self.BKLoc = (move.EndR, move.EndC)
        if move.isCastle:
            if move.EndC - move.StrtC == 2:
                self.board[move.EndR][move.EndC-1] = self.board[move.EndR][move.EndC+1]#this line and next line is to move the rook and remove the rook from the old square
                self.board[move.EndR][move.EndC+1] = ".."
            else:
                    self.board[move.EndR][move.EndC+1] = self.board[move.EndR][move.EndC-2]
                    self.board[move.EndR][move.EndC-2] = ".."
        self.updateCastle(move)
        self.CastleLog.append(Castle(self.CurrentCastle.WK, self.CurrentCastle.BK, self.CurrentCastle.WQ, self.CurrentCastle.BQ))
    def debug(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.StrtR][move.StrtC] = move.Moved
            self.board[move.EndR][move.EndC] = move.Capt
            self.WhiteMove = not self.WhiteMove
            if move.Moved == "WK":
                self.WKLoc = (move.StrtR, move.StrtC)
            elif move.Moved == "BK":
                self.BKLoc = (move.StrtR, move.StrtC)
        
    def PosMov(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                toMove = self.board[r][c][0]
                if (toMove == 'B' and not self.WhiteMove) or (toMove == 'W' and self.WhiteMove):
                    piece = self.board[r][c][1]
                    self.movesFunc[piece](r,c,moves)
        return moves
    def getValMov(self):
        moves = []
        tmpCastle = Castle(self.CurrentCastle.WK, self.CurrentCastle.BK,self.CurrentCastle.WQ,self.CurrentCastle.BQ)
        self.isCheck, self.pin, self.check = self.scanKingSqr()
        if self.WhiteMove:
            KR = self.WKLoc[0]
            KC = self.WKLoc[1]
        else:
            KR = self.BKLoc[0]
            KC = self.BKLoc[1]
        if self.isCheck:
            if len(self.check) == 1:
                moves = self.PosMov()
                checks = self.check[0]
                CRow = checks[0]
                CCol = checks[1]
                pieceThatChecks = self.board[CRow][CCol]
                valSqr = []
                if pieceThatChecks[1] == "N":
                    valSqr = [(CRow,CCol)]
                else:
                    for i in range(1,8):
                        valSqrs = (KR + checks[2]*i, KC + checks[3]*i)
                        valSqr.append(valSqrs)
                        if valSqrs[0] == CRow and valSqrs[1] == CCol:
                            break
                for i in range(len(moves) -1,-1,-1):
                    if moves[i].Moved[1] != "K":
                        if not(moves[i].EndR, moves[i].EndC) in valSqr:
                            moves.remove(moves[i])
            else:
                self.KingM(KR,KC,moves)
        else:
            moves = self.PosMov()
            if self.WhiteMove:
                self.CastleMove(self.WKLoc[0], self.WKLoc[1], moves)
            else:
                self.CastleMove(self.BKLoc[0], self.BKLoc[1], moves)
        if len(moves) == 0:
            if self.ifInCheck():
                self.Checkm8 = True
            else:
                self.Stalem8 = True
        self.CurrentCastle = tmpCastle
        return moves

    def scanKingSqr(self):
        pin = []
        check = [] 
        isCheck = False
        if self.WhiteMove:
            opp = "B"
            ally = "W"
            sRow = self.WKLoc[0]
            sCol = self.WKLoc[1]
        else:
            opp = "W"
            ally = "B"
            sRow = self.BKLoc[0]
            sCol = self.BKLoc[1]

        dir = ((-1,0), (0,-1), (1,0), (0,1), (1,1), (1,-1), (-1,1), (-1,-1))
        for col in range(len(dir)):
            k = dir[col]
            posPin = ()
            
            for row in range(1,8):
                EndR = sRow + k[0]*row
                EndCol = sCol + k[1]*row
                if (0<=EndR<8) and (0<=EndCol<8):
                    Pos = self.board[EndR][EndCol]
                    if Pos[0] == ally and Pos[1]!="K":
                        if posPin == ():
                            posPin = (EndR, EndCol, k[0], k[1])
                        else:
                            break
                    elif Pos[0] == opp:
                        piece = Pos[1] 

                        if(0<=col<=3 and piece == "R") or (
                            row == 1 and piece == "P" and ((opp == "W" and 4<=col<=5) or (opp == "B" and 6<=col<=7))) or (
                                4<=col<=7 and piece == "B") or (piece == "Q") or (row == 1 and piece == "K"):
                            if posPin == ():
                                isCheck = True
                                check.append((EndR, EndCol, k[0], k[1]))
                                break
                            else:
                                pin.append(posPin)
                                break
                        else:
                            break
                else:
                    break

        KDir = ((-2,-1), (-2,1), (-1,2), (1,2), (2,-1),(2,1), (-1,-2),(1,-2))
        for i in KDir:
            EndR = sRow + i[0]
            EndCol =  sCol + i[1]
            if 0<=EndR<8 and 0<=EndCol<8:
                Pos = self.board[EndR][EndCol]
                if Pos[0] == opp and Pos[1] == "N":
                    isCheck = True
                    check.append((EndR, EndCol, i[0], i[1]))
        
        return isCheck, pin, check


    def ifInCheck(self):
        if self.WhiteMove:
            return self.KingGetAttack(self.WKLoc[0], self.WKLoc[1])
        else:
            return self.KingGetAttack(self.BKLoc[0], self.BKLoc[1])






    def KingGetAttack(self,r,c):
        self.WhiteMove = not self.WhiteMove
        opp = self.PosMov()
        self.WhiteMove = not self.WhiteMove
        for i in opp:
            if i.EndR == r and i.EndC == c:
                return True
        return False



        
    def PawnM(self,r,c,moves):
        isPinned = False
        pinDir = ()
        for i in range(len(self.pin)-1,-1,-1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                isPinned = True
                pinDir = (self.pin[i][2], self.pin[i][3])
                self.pin.remove(self.pin[i])
                break

        if self.WhiteMove:
            if self.board[r-1][c] == "..":
                if not isPinned or pinDir == (-1,0):
                    moves.append(Moves((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "..":
                        moves.append(Moves((r,c),(r-2,c),self.board))
            if c-1 >= 0:        
                if self.board[r-1][c-1][0] == 'B':
                    if not isPinned or pinDir == (-1,-1):
                        moves.append(Moves((r,c),(r-1,c-1),self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'B':
                    if not isPinned or pinDir == (-1,1):
                        moves.append(Moves((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c] == "..":
                if not isPinned or pinDir == (1,0):
                    moves.append(Moves((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == "..":
                        moves.append(Moves((r,c),(r+2,c),self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'W':
                    if not isPinned or pinDir == (1,-1):
                        moves.append(Moves((r,c),(r+1,c-1),self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'W':
                    if not isPinned or pinDir == (1,1):
                        moves.append(Moves((r,c),(r+1,c+1),self.board))           


    def RookM(self,r,c,moves):
        isPinned = False
        pinDir = ()
        for i in range(len(self.pin)-1,-1,-1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                isPinned = True
                pinDir = (self.pin[i][2], self.pin[i][3])
                if self.board[r][c][1] != "Q":
                    self.pin.remove(self.pin[i])
                break
        dir = ((-1,0), (0,-1), (1,0), (0,1))
        enemy = 'B' if self.WhiteMove else "W"
        for i in dir:
            for j in range(1,8):
                endRow = r + i[0]*j
                endCol = c + i[1]*j
                
                if 0<=endRow<8 and 0<=endCol<8:
                    if not isPinned or pinDir == i or pinDir == (-i[0], -i[1]):
                        Pos = self.board[endRow][endCol]
                        if Pos == '..':
                            moves.append(Moves((r,c),(endRow,endCol),self.board))
                        elif Pos[0] == enemy:
                            moves.append(Moves((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def KnightM(self,r,c,moves):
        isPinned = False
        for i in range(len(self.pin)-1,-1,-1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                isPinned = True
                self.pin.remove(self.pin[i])
                break

        dir = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2),(1,2), (2,-1),(2,1))
        ally = 'W' if self.WhiteMove else "B"
        for i in dir:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0<=endRow<8 and 0<=endCol<8:
                if not isPinned:
                    Pos = self.board[endRow][endCol]
                    if Pos == '..':
                        moves.append(Moves((r,c),(endRow,endCol),self.board))
                    elif Pos[0] != ally:
                        moves.append(Moves((r,c),(endRow,endCol),self.board))


            
    def  BishopM(self,r,c,moves):
        isPinned = False
        pinDir = ()
        for i in range(len(self.pin)-1,-1,-1):
            if self.pin[i][0] == r and self.pin[i][1] == c:
                isPinned = True
                pinDir = (self.pin[i][2], self.pin[i][3])
                self.pin.remove(self.pin[i])
                break
        dir = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemy = 'B' if self.WhiteMove else "W"
        for i in dir:
            for j in range(1,8):
                endRow = r + i[0]*j
                endCol = c + i[1]*j
                
                if 0<=endRow<8 and 0<=endCol<8:
                    if not isPinned or pinDir == i or pinDir == (-i[0], -i[1]):
                        Pos = self.board[endRow][endCol]
                        if Pos == '..':
                            moves.append(Moves((r,c),(endRow,endCol),self.board))
                        elif Pos[0] == enemy:
                            moves.append(Moves((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def  QueenM(self,r,c,moves):
        self. RookM(r,c,moves)
        self. BishopM(r,c,moves)

    def  KingM(self,r,c,moves):
        dir = ((-1,0), (0,-1), (1,0), (0,1),(-1,-1), (-1,1), (1,-1), (1,1))
        ally = 'W' if self.WhiteMove else "B"
        for i in dir:
            for j in range(1,8):
                endRow = r + i[0]
                endCol = c + i[1]
                
                if 0<=endRow<8 and 0<=endCol<8:
                    Pos = self.board[endRow][endCol]
                    if Pos[0] != ally:
                        if ally == "W":
                            self.WKLoc = (endRow,endCol)
                        else:
                            self.BKLoc = (endRow,endCol)
                        isCheck, pin, check = self.scanKingSqr()
                        if not isCheck:
                            moves.append(Moves((r,c),(endRow,endCol),self.board))
                        if  ally == "W":
                            self.WKLoc = (r,c)
                        else:
                            self.BKLoc = (r,c)



    def CastleMove(self, row, col, moves):
        if self.KingGetAttack(row, col):
            return
        if (self.WhiteMove and self.CurrentCastle.WK) or (not self.WhiteMove and self.CurrentCastle.BK):
            if self.board[row][col+1] == '..' and self.board[row][col+2] == '..':
                if not self.KingGetAttack(row, col+1) and not self.KingGetAttack(row, col+2):
                    moves.append(Moves((row,col), (row,col+2), self.board, isCastle=True))
        if (self.WhiteMove and self.CurrentCastle.WQ) or (not self.WhiteMove and self.CurrentCastle.BQ):
            if self.board[row][col-1] == '..' and self.board[row][col-2] == '..' and self.board[row][col-3] == '..':
                if not self.KingGetAttack(row, col-1) and not self.KingGetAttack(row, col-2):
                    moves.append(Moves((row,col), (row,col-2), self.board, isCastle=True))

    def updateCastle(self, move):
        if move.Moved == "BK":
            self.CurrentCastle.BK = False
            self.CurrentCastle.BQ = False
        elif move.Moved == "WK":
            self.CurrentCastle.WK = False
            self.CurrentCastle.WQ = False
        elif move.Moved == "BR":
            if move.StrtR == 0:
                if move.StrtC == 0:
                    self.CurrentCastle.BQ = False
                elif move.StrtC == 7:
                    self.CurrentCastle.BK = False
        elif move.Moved == "WR":
            if move.StrtR == 7:
                if move.StrtC == 7:
                    self.CurrentCastle.WK = False
                elif move.StrtC == 0:
                    self.CurrentCastle.WQ = False

class Moves():
    rToRow = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    RowTor = {v: i for i,v in rToRow.items()} 
    fToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    ColsTof = {v: i for i,v in fToCols.items()}
    def __init__(self, StrtSq, EndSq, board, isCastle = False):
        self.StrtR = StrtSq[0]
        self.StrtC = StrtSq[1]
        self.EndR = EndSq[0]
        self.EndC = EndSq[1]
        self.Moved = board[self.StrtR][self.StrtC]
        self.Capt = board[self.EndR][self.EndC]
        self.ID = self.StrtR*1000+self.StrtC*100+self.EndR*10+self.EndC
        self.isCastle = isCastle
    def __eq__(self, other):
        if isinstance(other, Moves):
            return self.ID == other.ID
        return False
    def  ChessNotation(self):
        return self. RankFiles(self.StrtR, self.StrtC)+self. RankFiles(self.EndR, self.EndC)
    def  RankFiles(self,r,c):
        return self.ColsTof[c] + self.RowTor[r]



class Castle():
    def __init__(self, WK, BK, WQ, BQ):
        self.WK = WK
        self.BK = BK
        self.WQ = WQ
        self.BQ = BQ
        