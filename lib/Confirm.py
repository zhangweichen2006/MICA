# -*- coding: utf-8 -*-
#!/usr/bin/env python
from os import environ
environ['SDL_VIDEO_CENTERED'] = '1'
import os.path
thisrep = os.path.dirname(__file__)
imagesrep = os.path.join(thisrep,'images')

from pygame import *
font.init()

from subprocess import Popen,PIPE
from sys import stdout
import pickle

from Buttons import Button0

from textwrap import wrap
import sys
import text

label,title,mode,fontsize,width,bgcolor,fgcolor = pickle.loads(sys.stdin.buffer.read() if sys.version_info[0]==3 else sys.stdin.read())
try: label = label.decode('utf-8')
except AttributeError: pass
try: title = title.decode('utf-8')
except AttributeError: pass

font = font.Font(os.path.join(thisrep,'MonospaceTypewriter.ttf'),fontsize)
marge = 10
border = 2
linecolor = fgcolor
titlecolor = fgcolor
marge *= 2
border *= 2

char_w,char_h = font.size(' ')
foo = max((3*52,len(title)*char_w))
w = width-marge-border
if w < foo: w = foo
charperline = (w+(char_w-1))//char_w
label = text.Text(label,charperline)
width = charperline*char_w+marge+border
height = char_h*(len(label)+(3 if title else 1))+52+marge+border
scr = display.set_mode((width,height),NOFRAME)
r = scr.get_rect()
scr.fill(bgcolor)
r.inflate_ip(-border,-border)
draw.rect(scr,fgcolor,r,1)
r.inflate_ip(-marge,-marge)

y = r.y
if title:
    title = text.Text(title,charperline)
    title.screen(scr,r.topleft,fgcolor,font)
    y = r.y + 2*char_h
    draw.line(scr,linecolor,(r.left,r.top+char_h*1.5),(r.right,r.top+char_h*1.5),1)

x = r.x
label.screen(scr,(x,y),fgcolor,font)

YES = Button0(image.load(os.path.join(imagesrep,"valid.png")))
YES.midbottom =r.midbottom
NO = Button0(image.load(os.path.join(imagesrep,"cancel.png")))
NO.left = (r.w-104)//3+(marge+border)//2
NO.bottom = r.bottom
back = Button0(image.load(os.path.join(imagesrep,"back.png")))
back.midbottom = r.midbottom

buttons = [YES]
if mode >= 2:
    buttons.append(NO)
    YES.right = width-NO.left
if mode == 3:
    buttons.append(back)
    NO.bottomleft = r.bottomleft
    YES.bottomright = r.bottomright

for i in buttons: i.screen()
display.flip()

run = True
while run:
    ev = event.wait()
    for button,output in zip(buttons,(True,False,None)):
        if button.update(ev):
            scr.fill(bgcolor,button)
            display.update(button.screen())
            if button.status:
                pickle.dump(output,sys.stdout.buffer if sys.version_info[0]==3 else sys.stdout,protocol=2)
                run = False
                break 
