#!/usr/bin/env python
import os,os.path
from sys import stdout,path,version_info,stdin
import reader
import GetEvent
import pickle
from os import environ
environ['SDL_VIDEO_CENTERED'] = '1'
import os.path
thisrep = os.path.abspath(os.path.dirname(__file__))
imagesrep = os.path.join(thisrep,'images')
from pygame import *
font.init()
from subprocess import Popen,PIPE
from sys import stdout
from form import Form
from textwrap import wrap
import text

label,menu,mode,fontsize,width,height,frame,bgcolor,fgcolor = pickle.loads(stdin.buffer.read() if version_info[0]==3 else stdin.read())
try: label = label.decode('utf-8')
except AttributeError: pass
try: menu = [i.decode('utf-8') for i in menu]
except AttributeError: pass
except UnicodeEncodeError: pass

font = font.Font(os.path.join(thisrep,'MonospaceTypewriter.ttf'),fontsize)
marge = 10
border = 2
linecolor = fgcolor
titlecolor = fgcolor
marge *= 2
border *= 2

char_w,char_h = font.size(' ')
charperline = (width-marge-border)//char_w
label = text.Text(label,charperline)
width = charperline*char_w+marge+border

if not height:
    foo = char_h*(len(menu)+1)
else:
    foo = height-char_h*(len(label)+(1 if label else 0))-marge-border
    foo = (foo//char_h)*char_h
height = char_h*(len(label)+(1 if label else 0))+marge+border+foo

if frame: frame = 0
else: frame = NOFRAME

scr = display.set_mode((width,height),frame)
key.set_repeat(100,50)
r = scr.get_rect()
scr.fill(bgcolor)
r.inflate_ip(-border,-border)
draw.rect(scr,fgcolor,r,1)
r.inflate_ip(-marge,-marge)

x,y = r.left,label.screen(scr,r.topleft,fgcolor,font).bottom + char_h

m = reader.Lister(menu,(r.left,y),(r.w,foo),fontsize)
m.screen()
display.flip() 

while 1:
    ev = GetEvent.wait()
    m.update(ev)
    m.screen()
    if (ev.type == MOUSEBUTTONUP and ev.click[1] == 2 and m.LINE) or (ev.type == KEYDOWN and ev.key in (K_RETURN,K_KP_ENTER)):
        pickle.dump((m.NLINE,m.LINE[1:]),stdout.buffer if version_info[0]==3 else stdout,protocol=2)
        break
    display.flip()
    if ev.type == QUIT:
        pickle.dump(('',''),stdout.buffer if version_info[0]==3 else stdout,protocol=2)
        break

