#!/usr/bin/env python
from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))
from random import randint
from pygame import *
from pygame import gfxdraw
from EasyGame import pathgetter,confirm

controls = """hold the left mouse button to draw

d = undo
s = save"""
scr = display.set_mode((800,800))
confirm(controls,fontsize=14,mode=1)
a = []
c = []
color = [randint(0,255) for i in (1,2,3)]+[50]

while 1:
    ev = event.wait()
    if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
        a.append([ev.pos])
        c.append(color)
    if ev.type == MOUSEMOTION and ev.buttons[0]:
        a[-1].append(ev.pos)
        if len(a[-1]) >= 2:
            draw.aaline(scr,color,a[-1][-1],a[-1][-2],1)
            display.flip() 
    if ev.type == MOUSEBUTTONUP and ev.button == 1:
        if len(a[-1]) >= 2:
            draw.aaline(scr,color,a[-1][0],a[-1][-1],1)
            gfxdraw.filled_polygon(scr,a[-1],color)
            display.flip() 
        color = [randint(0,255) for i in (1,2,3)]+[50]
    if ev.type == QUIT: break
    if ev.type == KEYDOWN and ev.key == K_s:
        p = pathgetter()
        if p: image.save(scr,p)
    if ev.type == KEYDOWN and ev.key == K_d and a:
        a.pop()
        c.pop()
        scr.fill(0)
        for lines,color in zip(a,c):
            draw.aalines(scr,color,1,lines,1)
            gfxdraw.filled_polygon(scr,lines,color)
        display.flip()
    if ev.type == KEYDOWN and ev.key == K_p:
        a = [[(x//10*10,y//10*10) for x,y in i] for i in a]
        scr.fill(0)
        for lines,col in zip(a,c):
            if len(lines) > 1:
                draw.aalines(scr,col,1,lines,1)
                gfxdraw.filled_polygon(scr,lines,col)
        display.flip()
         
    
