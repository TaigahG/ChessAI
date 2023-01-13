import random

PiecesValues = {"K":0, "Q":10 , "R":5, "B":3, "N":3, "P":1}
mate = 1000
stale = 0
DEPTH = 1


knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]


positionScore = {"WN": knight_scores,
                         "BN": knight_scores[::-1],
                         "WB": bishop_scores,
                         "BB": bishop_scores[::-1],
                         "WQ": queen_scores,
                         "BQ": queen_scores[::-1],
                         "WR": rook_scores,
                         "BR": rook_scores[::-1],
                         "WP": pawn_scores,
                         "BP": pawn_scores[::-1]}




def RandMove(VMoves):
    return VMoves[random.randint(0, len(VMoves)-1)]

# def BestMove(gs, VMoves):
#     turnToPlay = 1 if gs.WhiteMove else -1
#     oppminmax = mate
#     recommendMove = None
#     random.shuffle(VMoves)
#     for m in VMoves:
#         gs.makesMove(m)
#         oppmoves = gs.getValMov()
#         if gs.Stalem8:
#             oppMax = stale
#         elif gs.Checkm8:
#             oppMax = -mate
#         else:
#             oppMax = -mate
#             gs.getValMov()
#             for i in oppmoves:
#                 gs.makesMove(i)
#                 if gs.Checkm8:
#                     score = -turnToPlay * mate
#                 elif gs.Stalem8:
#                     score = stale
#                 else:
#                     score = -turnToPlay * scoreBoard(gs.board)
#                 if score > oppMax:
#                     oppMax = score
#                 gs.debug()
#             if oppMax < oppminmax:
#                 oppminmax = oppMax
#                 recommendMove = m
#         gs.debug()
#     return recommendMove
# def BestMiniMax(gs, VMoves):
#     global nextMove
#     nextMove = None
#     minMax(gs, VMoves, DEPTH, mate, -mate, gs.WhiteMove)
#     return nextMove

# def minMax(gs, VMoves, depth,alpha,beta,WhiteMove):    
#     global nextMove

#     if depth == 0:
#         return scoreBoard(gs.board)
    
#     if gs.WhiteMove:
#         maxScore = -mate
#         for move in VMoves:
#             gs.makesMove(move)
#             nextMoves = gs.getValMov()
#             eval = minMax(gs, VMoves, depth-1, alpha, beta, False)
#             if eval > maxScore:
#                 maxScore = eval
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.debug()
#             if maxScore > alpha:
#                 alpha = maxScore
#             if beta <= alpha:
#                 break
#         return maxScore
#     else:
#         minScore = mate
#         for move in VMoves:
#             gs.makesMove(move)
#             nextMoves = gs.getValMov()
#             eval = minMax(gs, VMoves, depth-1, alpha, beta, True)
#             if eval < minScore:
#                 min = eval
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.debug()
#             if minScore < beta:
#                 beta = minScore
#             if beta <= alpha:
#                 break
#         return minScore
def BestNegaMaxMove(gs, VMoves):
    global nextMove
    nextMove = None
    random.shuffle(VMoves)
    NegaMax(gs, VMoves, DEPTH, -mate, mate, 1 if gs.WhiteMove else -1)
    return nextMove

def NegaMax(gs, VMoves, depth, alpha, beta, turnToPlay):
    global nextMove
    if depth == 0:
        return turnToPlay * scoreBoard(gs)

    MaxScore = -mate
    for move in VMoves:
        gs.makesMove(move)
        nextMoves = gs.getValMov()
        eval = -NegaMax(gs, nextMoves, depth-1, -alpha, -beta, -turnToPlay)
        if eval > MaxScore:
            MaxScore = eval
            if depth == DEPTH:
                nextMove = move
        gs.debug()
        
        if MaxScore > alpha:
            alpha = MaxScore
        if beta <= alpha:
            break
    return MaxScore

def scoreBoard(gs):
    if gs.Checkm8:
        if gs.WhiteMove:
            return -mate
        else:
            return mate
    elif gs.Stalem8:
        return stale

    eval = 0
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            pieces = gs.board[r][c]
            if pieces != "..":
                positionScores = 0
                if pieces[1] != "K":
                    positionScores = positionScore[pieces][r][c]
                if pieces[0] == 'W':
                    eval += PiecesValues[pieces[1]] + positionScores
                elif pieces[0] == 'B':
                    eval -= PiecesValues[pieces[1]] + positionScores
    return eval