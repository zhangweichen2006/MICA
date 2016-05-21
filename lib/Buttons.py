from pygame import Rect,display
from pygame.locals import *
        
class Button0(Rect):
    def __init__(self,image):
        self.scr = display.get_surface()
        w,h = image.get_size()
        w //= 3
        self.images = [image.subsurface(x,0,w,h).copy() for x in range(0,w*3,w)]
        Rect.__init__(self,0,0,w,h)
        self.ACTIV = True
        self.status = False
        self.over = False
        
    def update(self,ev):
        if ev.type == MOUSEMOTION:
            if self.collidepoint(ev.pos) and not self.over:
                self.over = True
                return self.ACTIV
            elif not self.collidepoint(ev.pos) and self.over:
                self.over = False
                return self.ACTIV
        elif ev.type == MOUSEBUTTONUP and ev.button == 1 and self.collidepoint(ev.pos) and self.ACTIV:
            self.status = True
            return True
        elif ev.type == ACTIVEEVENT:
            self.over = False
            return True
        
    def screen(self):
        self.scr.blit(self.images[self.over if self.ACTIV else 2],self)
        return self  
    
    def show(self):
        display.update(self.screen())
        return self
