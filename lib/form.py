# -*- coding: utf-8 -*-
from sys import stdout
import pygame
pygame.font.init()
try: import pyca
except: pass
try: from reader import Lister
except ImportError: from .reader import Lister

class Form(pygame.Rect,object):

    def __init__(self,pos,width,fontsize,height=None,font=None,bg=(250,250,250),fgcolor=None,hlcolor=(180,180,200),curscolor=(0xff0000),maxlen=0,maxlines=0):
        pygame.scrap.init()
        if not font: self.FONT = pygame.font.Font(pygame.font.match_font('mono',1),fontsize)
        elif type(font) == str: self.FONT = pygame.font.Font(font,fontsize)
        else: self.FONT = font
        try: self.BG = pygame.Color(*bg)
        except:self.BG = bg
        if not fgcolor:
            self.FGCOLOR = (255,255,255) if (self.BG.r*299 + self.BG.g*587 + self.BG.b*114) / 1000 < 125 else (0,0,0)
            try: self.FGCOLOR = (255,255,255) if (self.BG.r*299 + self.BG.g*587 + self.BG.b*114) / 1000 < 125 else (0,0,0)
            except: self.FGCOLOR = (0,0,0)
        else: self.FGCOLOR = fgcolor
        self.HLCOLOR = hlcolor
        self.CURSCOLOR = curscolor
        self._line = 0
        self._index = 0
        self.MAXLINES = maxlines
        self.MAXLEN = maxlen
        self._splitted = ['']
        if not height: pygame.Rect.__init__(self,pos,(width,self.FONT.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        self._x,self._y = pos
        self._src = pygame.display.get_surface()
        self._select = self._line,self._index
        self.TAB = 4
        self._adjust()
        self._cursor = True
    
    @property   
    def INDEX(self):
        return self._line,self._index
    @INDEX.setter
    def INDEX(self,value):
        line,colum = value
        self._line,self._index = self._select = line,colum
        self._adjust()

    @property   
    def CURSOR(self):
        return self._cursor
    @CURSOR.setter
    def CURSOR(self,value):
        self._cursor = value
    
    @property
    def HLCOLOR(self):
        return None
    @HLCOLOR.setter
    def HLCOLOR(self,color):
        self._hlsurface = pygame.Surface((self._w,self._h),pygame.SRCALPHA)
        self._hlsurface.fill(color)
    
    @property
    def OUTPUT(self):
        return '\n'.join(self._splitted)
    @OUTPUT.setter
    def OUTPUT(self,string):
        self._splitted = string.split('\n')
        
    
    @property
    def FONT(self):
        return self._font
    @FONT.setter
    def FONT(self,font):
        self._font = font
        self._w,self._h = self._font.size(' ')
    
    @property
    def SELECTION(self):
        p1,p2 = sorted(((self._line,self._index),self._select))
        if p1 != p2:
            selection = [len(i) for i in self._splitted[:p2[0]]]
            return self.OUTPUT[sum(selection[:p1[0]]) + p1[0] + p1[1]:sum(selection) + p2[0] + p2[1]:]
        return ''
                
    def _adjust(self):
        if self._index < len(self._splitted[self._line]):
            rcurs = pygame.Rect(self._x+self._index*self._w,self._y+self._line*self._h,self._w,self._h)
        else:
            rcurs = pygame.Rect(self._x+len(self._splitted[self._line])*self._w,self._y+self._line*self._h,1,self._h)
        
        self._rcursor = rcurs.clamp(self)
        self._x += self._rcursor.x - rcurs.x
        self._y += self._rcursor.y - rcurs.y
    
    def screen(self):
        clip = self._src.get_clip()
        self._src.set_clip(self.clip(clip))
        try: self._src.fill(self.BG,self)
        except: self._src.blit(self.BG,self)
        
        start = (self.top - self._y) // self._h
        end = (self.bottom - self._y) // self._h + 1

        p1,p2 = sorted(((self._line,self._index),self._select))

        y = self._y + start * self._h
        for py,i in enumerate(self._splitted[start:end],start):
            x = self._x
            for px,j in enumerate(i):
                if p1<=(py,px)<p2:
                    self._src.blit(self._hlsurface,(x,y))
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                else:
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                x += self._w
            y += self._h
        if self._cursor:
            pygame.draw.line(self._src,self.CURSCOLOR,self._rcursor.topleft,self._rcursor.bottomleft,1)
        self._src.set_clip(clip)
    
    def show(self):
        self.screen()
        pygame.display.update(self)
        
    def wakeup(self,ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: pyca.focus(self)
        self.update(ev)
        
    def clear(self):
        p1,p2 = sorted(((self._line,self._index),self._select))
        if p1 != p2:
            selection = [len(i) for i in self._splitted[:p2[0]]]
            self.OUTPUT = self.OUTPUT[:sum(selection[:p1[0]]) + p1[0] + p1[1]] + self.OUTPUT[sum(selection[:p2[0]]) + p2[0] + p2[1]:]
            self._select = self._line,self._index = p1
            return True
            
    def update(self,ev):
        
        line,index = self._line,self._index
        shift = pygame.key.get_pressed()
        shift = shift[pygame.K_RSHIFT]|shift[pygame.K_LSHIFT]
        ret = False

        if ev.type == pygame.KEYDOWN:
            ret = True
            if ev.key == pygame.K_ESCAPE: ret = False
            elif ev.key == pygame.K_RIGHT:
                if self._index < len(self._splitted[self._line]):
                    self._index += 1
                elif self._line < len(self._splitted)-1:
                    self._index = 0
                    self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_LEFT:
                if self._index > len(self._splitted[self._line]):
                    self._index = len(self._splitted[self._line])
                if self._index:
                    self._index -= 1
                elif self._line:
                    self._line -= 1
                    self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
            
            elif ev.key == pygame.K_UP:
                if self._line: self._line -= 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
                
            elif ev.key == pygame.K_DOWN:
                if self._line < len(self._splitted)-1: self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
                
            elif ev.key == pygame.K_DELETE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]):
                        self._index = len(self._splitted[self._line])
                        self._select = self._line + 1,0
                    else:
                        self._select = self._line,self._index + 1
                self.clear()
                
            elif ev.key == pygame.K_END:
                self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_HOME:
                self._index = 0
                if not pygame.mouse.get_pressed()[0] and not shift and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_BACKSPACE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                    if self._index == 0:
                        if self._line: self._select = self._line - 1,len(self._splitted[self._line - 1])
                    else: self._select = self._line,self._index - 1
                self.clear()

            elif ev.key == pygame.K_TAB:
                self.clear()
                sp = self.TAB-self._index%self.TAB
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ' '*sp + self._splitted[self._line][self._index:]
                self._index += sp
                self._select = self._line,self._index

            elif ev.key == pygame.K_RETURN or ev.key == pygame.K_KP_ENTER or ev.unicode == '\n':
                self.clear()
                if not self.MAXLINES or self.OUTPUT.count('\n') < self.MAXLINES - 1:
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + '\n' + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._line += 1
                    self._index = 0
                    self._select = self._line,self._index
                
            elif ev.unicode and (not self.MAXLEN or len(self.OUTPUT) < self.MAXLEN):
                self.clear()
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ev.unicode + self._splitted[self._line][self._index:]
                self._index += 1
                self._select = self._line,self._index
                
        elif ev.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(ev.pos):
            if ev.button < 3:
                self._line = (ev.pos[1] - self._y) // self._h
                self._index = (ev.pos[0] - self._x) // self._w
                if ((ev.pos[0] - self._x) % self._w) > (self._w // 2): self._index += 1
                if self._line > len(self._splitted)-1:
                    self._line = len(self._splitted)-1
                    self._index = len(self._splitted[self._line])
                if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                if self._index < 0: self._index = 0
                if ev.button == 2:
                    pygame.scrap.set_mode(pygame.SCRAP_SELECTION)
                    if not pygame.scrap.contains('UTF8_STRING'):
                        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
                        if pygame.scrap.contains('UTF8_STRING'):
                            txt = pygame.scrap.get('UTF8_STRING')
                        else: txt = ''
                    else: txt = pygame.scrap.get('UTF8_STRING')
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + txt + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._index += len(self.SELECTION)
                
                if self._select != (self._line,self._index): ret = True
                self._select = self._line,self._index
            
            elif ev.button == 4:
                y = self._y
                if self._y + self._h*3 > self.top: self._y = self.top
                else: self._y += self._h*3
                self._rcursor.move_ip(0,self._y-y)
                ret = True
                
            elif ev.button == 5:
                y = self._y
                h = len(self._splitted) * self._h
                if h > self.height:
                    if self._y - self._h*3 < self.bottom - h: self._y = self.bottom - h
                    else: self._y -= self._h*3
                    self._rcursor.move_ip(0,self._y-y)
                ret = True
        
        elif ev.type == pygame.MOUSEMOTION and ev.buttons[0] and self.collidepoint(ev.pos):
            self._line = (ev.pos[1] - self._y) // self._h
            self._index = ((ev.pos[0] - self._x) // self._w)
            if ((ev.pos[0] - self._x) % self._w) > (self._w // 2): self._index += 1
            if self._line > len(self._splitted)-1:
                self._line = len(self._splitted)-1
                self._index = len(self._splitted[self._line])
            if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
            if self._index < 0: self._index = 0
            pygame.scrap.put('UTF8_STRING',self.SELECTION)

        if (line,index) != (self._line,self._index):
            self._adjust()
            ret = True

        return ret

class NumForm(Form):
    def __init__(self,pos,fontsize,digit=1,font=None):
        Form.__init__(self,pos,0,fontsize,maxlines=1,maxlen=digit+2,bg=(255,255,255),font=font)
        self.width = self._w * (digit + 2)
        self._x = self.right
        self.CURSOR = 1
        self.OUTPUT = '0'
        self.digit = digit
        self.INDEX = 0,len(self.OUTPUT)

    def update(self,ev):
        if ev.type == pygame.KEYDOWN:
            if ev.key in (pygame.K_SPACE,pygame.K_TAB): return False
            if ev.key == pygame.K_ESCAPE: self.OUTPUT = ''
            if ev.unicode.isdigit() and len(self.OUTPUT)-('-'in self.OUTPUT)-('.'in self.OUTPUT) == self.digit and not self.SELECTION: return False
            elif ev.unicode == '-':
                if self.OUTPUT.startswith('-'): self.OUTPUT = self.OUTPUT[1:]
                else: self.OUTPUT = '-' + self.OUTPUT
                return True
            rem = self.OUTPUT
            super(NumForm,self).update(ev)
            try:
                float(self.OUTPUT)
                if ev.key != pygame.K_BACKSPACE:
                    if self.OUTPUT.startswith('0') and self.OUTPUT[1] != '.': self.OUTPUT = ev.unicode
                    elif self.OUTPUT.startswith('-0') and self.OUTPUT[2] != '.': self.OUTPUT = '-' + ev.unicode
                    self.OUTPUT = self.OUTPUT
                return True
            except:
                if not self.OUTPUT:
                    self.OUTPUT = '0'
                    self.INDEX = 0,len(self.OUTPUT)
                    return True
                elif self.OUTPUT == '-':
                    self.OUTPUT = '-0'
                    return True
                elif self.OUTPUT == '.':
                    self.OUTPUT = '0.'
                    return True
                self.OUTPUT = rem
                return False
        elif super(NumForm,self).update(ev): return True

    @property
    def OUTPUT(self):
        return '\n'.join(self._splitted)
    @OUTPUT.setter
    def OUTPUT(self,string):
        self._splitted = string.split('\n')
        self._x = self.right-len(self.OUTPUT)*self._w
        self._adjust()

class MenuForm(Form):
    
    def __init__(self,pos,width,fontsize,nblines,fontname=None,bg=(250,250,250),fgcolor=None,hlcolor=(180,180,200),curscolor=(0xff0000),maxlen=0,menu=[],label=''):
        Form.__init__(self,pos,width,fontsize,height=None,font=fontname,bg=bg,fgcolor=fgcolor,hlcolor=hlcolor,curscolor=curscolor,maxlen=maxlen,maxlines=1)
        self.OUTPUT = label
        self._index = len(label)
        self.scr = pygame.display.get_surface()
        self.box = Lister(menu,self.bottomleft,(self.width,self._h*nblines),fontsize,font=fontname)
        self.openbox = 0
        self.just_now = 0
    
    def update(self,ev):
        self.just_now = 0
        ret = super(MenuForm,self).update(ev)
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.openbox and not self.box.collidepoint(ev.pos):
                self.openbox = 0
                self.just_now = 1
                return True
            elif self.collidepoint(ev.pos):
                self.openbox = 1
                self.just_now = 1
                return True
        if self.openbox:
            if self.box.update(ev):
                self.OUTPUT = self.box.LINE[1:]
                self.INDEX = 0,len(self.OUTPUT)
                ret = True
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.box.collidepoint(ev.pos):
                self.openbox = 0
                self.just_now = 1
                ret = True
        return ret
    
    def close(self):
        self.openbox = 0
        self.just_now = 1
        
    def screen(self):
        super(MenuForm,self).screen()
        if self.openbox:
            if self.just_now:
                self._bg = self.scr.subsurface(self.box).copy()
            self.box.screen()
            pygame.draw.rect(self.scr,(0,0,0),self.box,1)
        elif self.just_now:
            self.scr.blit(self._bg,self.box)
            
    def show(self):
        self.screen()
        if self.openbox or self.just_now: pygame.display.update((self,self.box))
        else: pygame.display.update(self)

if __name__ == '__main__':
    import os.path
    thisrep = os.path.dirname(__file__)
    pygame.display.set_mode((650,300))
    pygame.key.set_repeat(100,25)
    txt = Form((10,10),630,fontsize=15,height=80,bg=pygame.image.load(os.path.join(thisrep,'bg.jpg')),fgcolor=(250,250,250),hlcolor=(250,190,150,50),curscolor=(190,0,10))
    txt.OUTPUT = unicode("""This new version is simpler to use and faster with the great texts,
the constraint being that it only supports monospaced fonts.

There is still plenty of improvement to do.
You can modify this text ...""","utf8")
    txt.show()
    while True:
        if pygame.event.peek(pygame.QUIT): break
        evs = pygame.event.get()
        if evs:
            for ev in evs:
                txt.update(ev)
            txt.show()
    stdout.write(txt.OUTPUT)
    
