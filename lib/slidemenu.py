#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
font.init()
from math import cos,radians

def menu(menu,pos,font1=None,font2=None,color1=(128,128,128),color2=None,interline=5,justify=True,light=5,speed=300,lag=30):
    """
    jmenu(menu,pos,font1=None,font2=None,color1=(128,128,128),color2=None,interline=5,justify=True,light=5)
    
    menu: [str,str,...]
    pos: (int,int)|'topleft'|'topright'|'bottomleft'|'bottomright'|'midtop'|'midleft'|'midright'|'midbottom'|'center': position of menu
    font1: font object (None ==> pygame font): unhighlighted item font
    font2: font object (None ==> font1): highlighted item font
    color1: (int,int,int)|color object: unhighlighted item color
    color2: (int,int,int)|color object: highlighted item color (None => calculated from the light arg)
    interline: int
    justify: boolean: items spacing
    light: 0<=int<=10: use if not color2
    speed: int (0 =>no sliding): anim speed
    lag: int (0<=int<=90)
    
    return: (str,int)|(None,None) if hit escape
    """
    class Item(Rect):
        def __init__(self,menu,label):
            Rect.__init__(self,menu)
            self.label = label
                
    def show():
        i = Rect((0,0),font2.size(menu[idx].label))
        if justify: i.center = menu[idx].center 
        else: i.midleft = menu[idx].midleft
        display.update((scr.blit(bg,menu[idx],menu[idx]),scr.blit(font2.render(menu[idx].label,1,(255,255,255)),i)))
        time.wait(50)
        scr.blit(bg,r2,r2)
        [scr.blit(font1.render(item.label,1,color1),item) for item in menu if item!=menu[idx]]
        r = scr.blit(font2.render(menu[idx].label,1,color2),i)
        display.update(r2)
        return r
    
    def anim():
        clk = time.Clock()
        a = [menu[0]] if lag else menu[:]
        c = 0
        while a:
            for i in a:
                display.update(i)
                i.x = i.animx.pop(0)
                r = scr.blit(font1.render(i.label,1,color1),i)
                display.update(r)
                scr.blit(bg,r,r)
            c +=1
            if not a[0].animx:
                a.pop(0)
                if not lag: break
            if lag:
                foo,bar = divmod(c,lag)
                if not bar and foo < len(menu):
                    a.append(menu[foo])
            clk.tick(speed)
        
    
    events = event.get()
    scr = display.get_surface()
    scrrect = scr.get_rect()
    bg = scr.copy()
    if not font1: font1 = font.Font(None,scrrect.h//len(menu)//3)
    if not font2: font2 = font1
    if not color1: color1 = (128,128,128)
    if not color2: color2 = list(map(lambda x:x+(255-x)*light//10,color1))
    m = max(menu,key=font1.size)
    r1 = Rect((0,0),font1.size(m))
    ih = r1.size[1]
    r2 = Rect((0,0),font2.size(m))
    r2.union_ip(r1)
    w,h = r2.w-r1.w,r2.h-r1.h
    r1.h = (r1.h+interline)*len(menu)-interline
    r2 = r1.inflate(w,h)
    
    try: setattr(r2,pos,getattr(scrrect,pos))
    except: r2.topleft = pos
    if justify: r1.center = r2.center
    else : r1.midleft = r2.midleft
    
    menu = [Item(((r1.x,r1.y+e*(ih+interline)),font1.size(i)),i) for e,i in enumerate(menu)if i]
    if justify:
         for i in menu: i.centerx = r1.centerx
         
    if speed:
        for i in menu:
            z = r1.w-i.x+r1.x
            i.animx = [cos(radians(x))*(i.x+z)-z for x in list(range(90,-1,-1))]
            i.x = i.animx.pop(0)
        anim()
        for i in menu:
            z = scrrect.w+i.x-r1.x
            i.animx = [cos(radians(x))*(-z+i.x)+z for x in list(range(0,-91,-1))]
            i.x = i.animx.pop(0)
        
    
    mpos = Rect(mouse.get_pos(),(0,0))
    event.post(event.Event(MOUSEMOTION,{'pos': mpos.topleft if mpos.collidelistall(menu) else menu[0].center}))
    idx = -1
    while True:
        ev = event.wait()
        if ev.type >= USEREVENT: events.append(ev)
        elif ev.type == MOUSEMOTION:
            idx_ = Rect(ev.pos,(0,0)).collidelist(menu)
            if idx_ > -1 and idx_ != idx:
                idx = idx_
                r = show()
        elif ev.type == MOUSEBUTTONUP and r.collidepoint(ev.pos):
            ret = menu[idx].label,idx
            break
        elif ev.type == KEYDOWN:
            try:
                idx = (idx + {K_UP:-1,K_DOWN:1}[ev.key])%len(menu)
                r = show()
            except:
                if ev.key in (K_RETURN,K_KP_ENTER):
                    ret = menu[idx].label,idx
                    break
                elif ev.key == K_ESCAPE:
                    ret = None,None
                    break
    scr.blit(bg,r2,r2)
    
    if speed:
        [scr.blit(font1.render(i.label,1,color1),i) for i in menu]
        display.update(r2)
        time.wait(50)
        scr.blit(bg,r2,r2)
        anim()
    else: display.update(r2)
    
    for ev in events: event.post(ev)
    return ret

if __name__ == '__main__':
    scr = display.set_mode((600,560))
    print(menu.__doc__)
    f = font.Font('321impact.ttf',35)
    mainmenu = f.render('Main Menu',1,(200,200,200))
    r = mainmenu.get_rect()
    r.centerx,r.top = 300,120
    scr.blit(image.load('bg.png'),(0,0)) if time.get_ticks()&1 else scr.fill(-1)
    bg = scr.copy()
    scr.blit(mainmenu,r)
    display.flip()
    
    resp = "re-show"
    while resp == "re-show":
        resp = menu(['one player','','two players','options','re-show','next'],'center',color1=(150,100,150),light=6,speed=200,lag=20)[0]
        print(resp)
    display.update(scr.blit(bg,r,r))
    display.update(scr.blit(f.render('other example',1,(200,200,200)),(10,10)))
    print(menu(['one player','two players','options','credits','next'],(50,250),justify=0,font2=f,color1=(50,100,150),light=5,speed=0))
    print(menu(['one player','two players','options','credits','exit'],'bottomright',justify=0,font2=f,color1=(250,100,50),color2=(50,100,40)))
