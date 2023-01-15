import pygame
class Button():
    def __init__(self, txt, pos):
        self.game_active = False
        self.game_mode = 0 
        self.text = txt
        self.pos = pos
        self.btn = pygame.rect.Rect((self.pos[0], self.pos[1]), (130,40))
        # self.pvai = False ato True
    def drwBtn(self, scrn):
        pygame.draw.rect(scrn, 'lightgray', self.btn, 0, 5)
        pygame.draw.rect(scrn, 'black', self.btn, 5,5)
        f = pygame.font.SysFont("Montseratt",32,True,False)
        text = f.render(self.text, True, 'black')
        scrn.blit(text, (self.pos[0]+35, self.pos[1]+10))
    
    def Clicked(self):
        if self.btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False