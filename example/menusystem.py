#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))
#import EasyGame

from lib.MenuSystem import Menu,MenuSystem

from pygame import *
scr = display.set_mode((500,500))
font = font.Font(None,25)
scr.blit(font.render('click please',1,(250,250,250)),(10,10))
from os import listdir

frame    = Menu(("red","blue","white","brown"),'frame')
alphabet = Menu("abcdefghijklmnopqrstuvwxyz",'alphabet')
color    = Menu(("sub0","sub1",frame),"color",(0,1))
main     = Menu(("main0",alphabet,color,"exit"),'')

ms       = MenuSystem()

while 1:
    ev = event.wait()
    if ev.type == MOUSEBUTTONDOWN and not ms:# and ev.button == 3:
        ms.set(main,ev.pos,font)
        ms.screen()
    if ms.update(ev): ms.screen()
    if ms.OUTPUT:
        print(ms.OUTPUT,main.items(ms.OUTPUT))
        if ms.OUTPUT == [3]: break
        if ms.OUTPUT[:2] == [2,2]: draw.rect(scr,Color(main.items(ms.OUTPUT)[-1]),scr.get_rect(),10)
    display.flip()
