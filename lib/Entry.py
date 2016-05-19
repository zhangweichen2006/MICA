# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os.path
thisrep = os.path.dirname(__file__)

from pygame import *
font.init()

from subprocess import Popen,PIPE
from sys import stdout

from form import Form

from textwrap import wrap
import sys
import pickle
import re
regex0 = re.compile('<([+-])([biu])>|<(#)([0-9a-f]{0,6})>')
regex1 = re.compile('<(\d+), ?(\d+)>')
import text

def get(label='<1,1>',title='',fontsize=16,position=(0,0),frame=True,bgcolor=(200,200,200),fgcolor=(0,0,0)):
    marge = 10
    border = 2
    linecolor = fgcolor
    titlecolor = fgcolor
    marge *= 2
    border *= 2
    Font = font.Font(os.path.join(thisrep,'MonospaceTypewriter.ttf'),fontsize)
    char_w,char_h = Font.size('X')
    label_copy = label
    while 1:
        gr = regex1.search(label_copy)
        if gr:
            pos = gr.span()[0]
            spacelen = int(gr.groups()[0])
            label_copy = regex1.sub(' '*spacelen,label_copy,count=1)
            continue
        break
    foo = text.Text(label_copy)
    n_ = 0
    if title: n_ += 2
    if not len(foo): n_ += 1
    height = (char_h+2)*(len(foo)+n_)+marge+border
    key.set_repeat(100,50)
    scr = display.get_surface()
    
    foo.screen(scr,position,fgcolor,Font,interline=2)
    char_h += 2
    
    label = regex0.sub('',label)
    field_positions = []
    while 1:
        gr = regex1.search(label)
        if gr:
            pos = gr.span()[0]
            spacelen,maxlen = gr.groups()
            spacelen,maxlen = int(spacelen),int(maxlen)
            field_positions.append((pos,spacelen,maxlen))
            label = regex1.sub(' '*spacelen,label,count=1)
            continue
        break
    
    def set_field(pos):
        if field_positions and pos == field_positions[0][0]: 
            _,spacelen,maxlen = field_positions.pop(0)
            fields.append(Form((x,y),spacelen*char_w if spacelen else r.right-x,fontsize,height=None,font=Font,bg=(250,250,250),fgcolor=(0,0,0),hlcolor=(180,180,200),curscolor=(0xff0000),maxlines=1,maxlen=maxlen))
        
    fields = []
    x,y = position#r.left
    pos = 0
    set_field(0)
    for line in label.splitlines():
        for char in line:
            x += char_w
            pos += 1
            set_field(pos)
        y += char_h
        x = position[0]#r.left
        pos += 1
        set_field(pos)
    
    for i in fields:
        i.CURSOR = 0
        i.screen()
    fields[0].CURSOR = 1
    fields[0].screen()
    index = 0
    display.flip()
    run = True
    while run:
        ev = event.wait()
        if ev.type == KEYDOWN:
            if ev.key in(K_RETURN,K_KP_ENTER):
                fields[index].CURSOR = 0
                fields[index].show()
                index += 1
                if index == len(fields):
                    return [i.OUTPUT for i in fields]
                    pickle.dump([i.OUTPUT for i in fields],sys.stdout.buffer if sys.version_info[0]==3 else sys.stdout,protocol=2)
                    break
                fields[index].CURSOR = 1
            elif ev.key == K_TAB:
                fields[index].CURSOR = 0
                fields[index].show()
                index = (index+1)%len(fields)
                fields[index].CURSOR = 1
                continue
        elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            i = Rect(ev.pos,(0,0)).collidelist(fields)
            if i>-1 and i != index:
                fields[index].CURSOR = 0
                fields[index].show()
                fields[i].CURSOR = 1
                index = i
        elif ev.type == QUIT:
            return None
            pickle.dump(None,sys.stdout.buffer if sys.version_info[0]==3 else sys.stdout,protocol=2)
            break
        fields[index].update(ev)
        fields[index].show()
    
if __name__ == "__main__":
    from os import environ
    environ['SDL_VIDEO_CENTERED'] = '1'
    label,title,fontsize,width,frame,bgcolor,fgcolor = pickle.loads(sys.stdin.buffer.read() if sys.version_info[0]==3 else sys.stdin.read())
    try: label = label.decode('utf-8')
    except AttributeError: pass
    try: title = title.decode('utf-8')
    except AttributeError: pass
    pickle.dump(get(label,title,fontsize,width,frame,bgcolor,fgcolor),sys.stdout.buffer if sys.version_info[0]==3 else sys.stdout,protocol=2)
