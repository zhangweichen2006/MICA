from textwrap import wrap
import re
import os.path
thisrep = os.path.dirname(__file__)
from pygame import font,Color,Rect
font.init()

class Text(list):
    defaultfont = font.Font(os.path.join(thisrep,'MonospaceTypewriter.ttf'),16)
    regex = re.compile('<([+-])([biu])>|<(#)([0-9a-f]{0,6})>')
    regex_centered = re.compile('<(centered) (.+) >')
    
    def __init__(self,text='',width=None):
        self._text = ''
        self._width = width
        self.baliz = []
        self.text = text
        self.width = width
    
    @property
    def width(self): return self._width
    @width.setter
    def width(self,width):
        self._width = width
        while self: self.pop()
        if not width:
            self.extend([self.text.splitlines()])
        else:
            self.extend([wrap(line,width,drop_whitespace=True) if line else [''] for line in self._text.expandtabs(4).splitlines()])
    
    @property
    def text(self): return self._text
    @text.setter
    def text(self,text):
        try: self._text = text.decode('UTF-8')
        except: self._text = text
        if self.width:
            while 1:
                gr = Text.regex_centered.search(self._text)
                if gr:
                    b1,b2 = gr.groups()
                    if b1 == 'centered':
                        rawtext = Text.regex.sub('',b2)
                        lenght = (self.width-len(rawtext))//2
                        self._text = Text.regex_centered.sub(' '*lenght+b2+' '*lenght,self._text,count=1)
                    continue
                break
        while 1:
            gr = Text.regex.search(self._text)
            if gr:
                self.baliz.append((gr.span()[0],)+gr.groups())
                self._text = Text.regex.sub('',self._text,count=1)
                continue
            break
        self.width = self._width
    
    
    def __len__(self):
        return len(sum(self,[]))
    
    def screen(self,surface,pos,fgcolor=(128,128,125),font=None,interline=0):
        fgcolor = [fgcolor]
        px,y = pos
        mono = True
        if not font: font = Text.defaultfont
        if font.size('i')!=font.size('x'): mono = False
        char_w,char_h = font.size(' ')
        char_h += interline
        style_cmd = {'+':True,'-':False,'b':font.set_bold,'i':font.set_italic,'u':font.set_underline}
        bz = self.baliz
        def set_style(pos):
            while True:
                if bz and pos == bz[0][0]: 
                    _,mode,style,color,value = bz.pop(0)
                    if mode: style_cmd[style](style_cmd[mode])
                    elif color:
                        if value: fgcolor.append(Color(int(value,16)<<8))
                        else: fgcolor.pop()
                else: break
        rec = Rect(pos,(0,0))
        pos = 0
        set_style(pos)
        if mono:
            for lines in self:
                for line in lines:
                    x = px
                    for char in line:
                        rec = rec.unionall([(surface.blit(font.render(char,1,fgcolor[-1]),(x,y))),rec])
                        x += char_w
                        pos += 1
                        set_style(pos)
                    y += char_h
                pos += 1
                set_style(pos)
            return rec
        for lines in self:
            for line in lines:
                x = px
                for char in line:
                    x = surface.blit(font.render(char,1,fgcolor[-1]),(x,y))
                    rec = rec.unionall([x,rec])
                    x = x.right
                    pos += 1
                    set_style(pos)
                y += char_h
            pos += 1
            set_style(pos)
        return rec
    
if __name__ == "__main__":
    from pygame import *
    scr = display.set_mode((500,500))
    t = Text('<centered hello world >\n',50)
    display.update(t.screen(scr,(0,0),(200,200,200)))
    display.flip()
    while 1: pass
    
