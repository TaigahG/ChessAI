import pygame as p
from const import *
import ChessSettings
import sys
import AIChess
from Button import Button
from stats import Stats

stat = Stats()
command = 0
# notAI = False
#load the image
def loadImg():
    pieces = ['WP','WN','WR','WB','WK','WQ','BP','BN','BR','BB','BK','BQ']
    for i in pieces:
        IMAGES[i] = p.transform.scale(p.image.load("images/"+ i + ".png"), (sqrSize, sqrSize))


def BoardPieces(scrn, gs, valMov, sqSlctd):
    drwBP(scrn,gs)
    MoveHighlight(scrn, gs, valMov, sqSlctd)

def drwBP(scrn, gs):
    colors = [p.Color("#FFFAF0"), p.Color("#333333")]
    for r in range(d):
        for c in range(d):
            color = colors[((r+c)%2)]
            p.draw.rect(scrn, color, p.Rect(c*sqrSize,r*sqrSize,sqrSize,sqrSize))
            piece = gs.board[r][c]
            if piece != "..":
                scrn.blit(IMAGES[piece],p.Rect(c*sqrSize,r*sqrSize,sqrSize,sqrSize))

def MoveHighlight(scrn, gs, valMov, sqSlctd):
    if sqSlctd != ():
        r, c = sqSlctd
        if gs.board[r][c][0] == ("W" if gs.WhiteMove else "B"):
            sqr = p.Surface((sqrSize, sqrSize))
            sqr.set_alpha(150)
            sqr.fill(p.Color('green'))
            scrn.blit(sqr, (c*sqrSize, r*sqrSize))
            sqr.fill(p.Color('red'))
            for i in valMov:
                if i.StrtR == r and i.StrtC == c:
                    scrn.blit(sqr, (sqrSize*i.EndC, sqrSize*i.EndR))
                
def Text(scrn, txt):
    f = p.font.SysFont("Montseratt",32,True,False)
    text = f.render(txt, False, p.Color('black'))
    # txtLoc = p.Rect(0,0,w,h).move(w / 2 - text.get_width() / 2, h / 2 - text.get_height() / 2)
    txtLoc = text.get_rect(center=(w/2, h/2))
    scrn.blit(text, txtLoc.move(1,1))
    text = f.render(txt, False, p.Color('white'))
    scrn.blit(text, txtLoc.move(3,3))

            
def menu(scrn):
    Btn = Button('P V P',(200, 200))
    Btn2 = Button('P V AI',(200, 250))
    Btn.drwBtn(scrn)
    Btn2.drwBtn(scrn)
    if Btn.Clicked():
        command = 1
        stat.notAI = True
        stat.game_active = True
    if Btn2.Clicked():
        command = 2
        stat.notAI = False
        stat.game_active = True
    return Btn.Clicked()


def drawGame(scrn,gs, valMov, sqSlctd):
    BoardPieces(scrn, gs, valMov, sqSlctd)





def main():
    p.init()
    scrn = p.display.set_mode((w, h))
    p.display.set_caption("Chess")
    
    gs = ChessSettings.gamState()
    VMoves = gs.getValMov()
    hasMoved = False
    gameOver = False
    clock = p.time.Clock()
    sqSlctd = ()
    usrclcks = []
    loadImg()
    isRunning = True
    while isRunning:
        if not stat.game_active:
            menu(scrn)
        PlayerTurn = (gs.WhiteMove and Player) or (not gs.WhiteMove and stat.notAI)

        for event in p.event.get():
            if not stat.game_active:
                menu(scrn)
            if event.type == p.MOUSEBUTTONDOWN:
               if not gameOver: 
                loc = p.mouse.get_pos()
                c = loc[0]//sqrSize
                r = loc[1]//sqrSize
                if sqSlctd == (r,c):
                    sqSlctd = ()
                    usrclcks = []
                else:
                    sqSlctd = (r,c)
                    usrclcks.append(sqSlctd)
                if len(usrclcks) == 2:
                    move = ChessSettings.Moves(usrclcks[0], usrclcks[1], gs.board)
                    print(move.ChessNotation())
                    for i in range(len(VMoves)):
                        if move  == VMoves[i]:
                            gs.makesMove(VMoves[i])
                            hasMoved = True
                            sqSlctd = ()
                            usrclcks = []
                    if not hasMoved:
                        usrclcks = [sqSlctd]
            elif event.type == p.KEYDOWN:
                if event.key == p.K_r:
                    gs = ChessSettings.gamState()
                    VMoves = gs.getValMov()
                    sqSlctd = ()
                    usrclcks = []
                    hasMoved = False
                    gameOver = False
            if event.type == p.QUIT:
                isRunning = False
                sys.exit()
        
        if not gameOver and not PlayerTurn:
            compMove = AIChess.BestNegaMaxMove(gs, VMoves)
            gs.makesMove(compMove)
            hasMoved = True


        if hasMoved:
            VMoves = gs.getValMov()
            hasMoved = False
        if gs.Checkm8:
            gameOver = True
            if gs.WhiteMove:
                Text(scrn, "Black Won by checkmate")
            else:
                Text(scrn, "White Won by checkmate")
        elif gs.Stalem8:
            gameOver = True
            Text(scrn, "Game is draw")
        p.display.flip()
        BoardPieces(scrn, gs, VMoves, sqSlctd)













if __name__ == "__main__":
    main()