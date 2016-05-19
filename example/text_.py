#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))
from lib.text import Text

from pygame import *
scr = display.set_mode((400,650))

info = Text(width=30) # width = 30 chars width
info.text = """I be low no th ommatic, pealy reselly son of youre colike incry, th annothe m te earat cositicit of nottreame ill exia). Senow mandenclut froplexce; hound hand futich all age the gon ho calgen. The thers ared hase we foursiolun ovene. Bureassin thavid wrighorre Ment of ing dif the Pows, th ing is therals loyese fricand ar Har, arest acticanal quir allich Graor 146, Posommung sly, Joes. Des we scre serclus, ow? I spasing the Trettic ory, go, te in to thark cal prithe noted agan Secit of sone se thaterey chat the bore eard to grad, aske spoinve bits hictend sithe agure come difilms, Paine is flaingern ing tor ther. Rept cal rand thom torcescied"""

r = info.screen(scr,(50,50),fgcolor=(255,255,255),interline=-5)
display.update(draw.rect(scr,(200,100,250),r.inflate(20,20),1))

while event.wait().type != QUIT: pass
