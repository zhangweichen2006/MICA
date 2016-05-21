#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))
from lib.form import NumForm

from pygame import *

scr = display.set_mode((400,650))

f = NumForm((20,20),15,10,font=None)
f.screen()
display.update(draw.rect(scr,(250,100,200),f.inflate(2,2),1))

while 1:
    ev = event.wait()
    if ev.type == QUIT: break
    if f.update(ev): f.show()
