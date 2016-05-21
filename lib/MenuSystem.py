#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame as pg
from pygame.gfxdraw import filled_polygon,aapolygon
pg.font.init()

class MenuSystem(list,object):
    
    class Menu_(pg.Rect,object):
        
        def __init__(self,items,pos,font):
            
            self.scr               = pg.display.get_surface()
            self.items             = items
            self.exc               = items.exc
            self.font              = font
            w,h                    = max([font.size(' %s '%(i.label if type(i)==Menu else i)) for i in items])
            self.margin            = int(h*0.3)
            self.item_h            = h + self.margin
            
            pg.Rect.__init__(self,pos,(w+self.item_h,(self.item_h)*len(items)))
            self.clamp_ip(self.scr.get_rect())
            
            self.itemsrect         = self.copy()
            foo                    = self.clip(self.scr.get_rect())
            self.topleft,self.size = foo.topleft,foo.size
            self.itemsrect.top     = self.top
            self.item_index        = -1
            self.first_opening     = False
            self.offset            = 0
        
        def update(self,ev):
            
            if ev.type == pg.MOUSEMOTION and self.collidepoint(ev.pos):
                x,y             = ev.pos
                self.item_index = (y-self.itemsrect.y)//(self.item_h)-self.offset
                return self.item_index + self.offset
        
        def screen(self):
            
            if not self.first_opening:
                self.bg = self.scr.subsurface(self).copy()
                self.first_opening = True
            self.scr.fill(0x4d4c47,self)
            if self.item_index+self.offset>=0 and self.item_index+self.offset not in self.exc: self.scr.fill(0xe25817,(self.x,self.item_index*(self.item_h)+self.y-(self.top-self.itemsrect.top)%self.item_h,self.w,self.item_h))
            b = self.itemsrect.y+self.margin//2
            for e,i in enumerate(self.items):
                self.scr.blit(self.font.render(' %s '%(i.label if type(i)==Menu else i),1,(250,250,250)if e not in self.exc else(10,10,10)),(self.x,b))
                if type(i)==Menu:
                    r = pg.Rect(self.right-self.item_h,b-self.margin//2,self.item_h,self.item_h).inflate(-self.margin*3,-self.margin*3)
                    filled_polygon(self.scr,(r.topleft,r.midright,r.bottomleft),(250,250,250)if e not in self.exc else(10,10,10))
                    aapolygon(self.scr,(r.topleft,r.midright,r.bottomleft),(250,250,250)if e not in self.exc else(10,10,10))
                b+=self.item_h
            s = self.inflate(-2,-2)
            pg.draw.rect(self.scr,(100,100,100),self,1)
            pg.draw.lines(self.scr,(0,0,0),0,(s.topright,s.bottomright,s.bottomleft),1)
    
    def __init__(self):
        
        self.OUTPUT   = None
        self.todelete = []
        self.boxid  = self.itemid = -1
    
    def update(self,ev):
        
        self.todelete = []
        if ev.type == pg.MOUSEMOTION and self:
            self.foo = True
            boxid = pg.Rect(ev.pos,(0,0)).collidelistall(self)
            if boxid:
                boxid  = boxid[-1]
                itemid = self[boxid].update(ev)
                if (boxid,itemid) != (self.boxid,self.itemid):
                    self.todelete.extend(self[boxid+1:])
                    del(self[boxid+1:])
                    if type(self[boxid].items[itemid]) == Menu and itemid not in self[boxid].exc:
                        px = self[boxid].right
                        py = self[boxid].itemsrect.top + self[boxid].itemsrect.h//len(self[boxid].items)*itemid
                        self.append(MenuSystem.Menu_(self[boxid].items[itemid],(px,py),self.font))
                    self.boxid,self.itemid = boxid,itemid
                    return True
            else:
                self.boxid,self.itemid     = -1,-1
                ret = self[-1].item_index != -1
                self[-1].item_index        = -1
                return ret
        elif ev.type == pg.MOUSEBUTTONUP and self:
            if pg.Rect(ev.pos,(0,0)).collidelistall(self):
                if self[-1].item_index == -1 or ev.button not in (1,4,5) or self.itemid in self[self.boxid].exc: return
                elif ev.button == 1:
                    self.OUTPUT = [i.item_index+i.offset for i in self]
                    self.boxid,self.itemid     = -1,-1
                elif ev.button == 5:
                    if self[-1].itemsrect.bottom - self[-1].bottom >= self[-1].item_h:
                        self[-1].itemsrect.bottom  -= self[-1].item_h
                        self[-1].offset            += 1
                    else: self[-1].itemsrect.bottom = self[-1].bottom
                    return True
                elif ev.button == 4:
                    if self[-1].top - self[-1].itemsrect.top >= self[-1].item_h:
                        self[-1].itemsrect.top  += self[-1].item_h
                        self[-1].offset         -= 1
                    else: self[-1].itemsrect.top = self[-1].top
                    return True
            if self.foo:
                self.todelete.extend(self)
                del(self[:])
                return True
            else: self.foo = True
            
    
    def set(self,menu,pos,font=pg.font.Font(None,20)):
        
        if self:
            self.todelete.extend(self)
            del(self[:])
        self.boxid  = self.itemid = -1
        self.OUTPUT = None
        self.append(MenuSystem.Menu_(menu,pos,font))
        self.font   = font
        self.foo = False
    
    def erase(self):
        
        ret = self.todelete[:]
        for menu in self.todelete[::-1]:
            menu.scr.blit(menu.bg,menu)
        self.todelete = []
        return ret
    
    def draw(self):
        
        for menu in self:
            menu.screen()
        return self
    
    def screen(self):
        
        return self.erase()+self.draw()
    
    @property
    def mouse_over(self): return self.itemid != -1
    

class Menu(list):
    
    def __init__(self,items,label=None,exc=()):
        
        self.extend(items)
        self.label = label
        self.exc   = exc
        
    def items(self,indices):
        
        foo     = self
        output  = []
        for i in indices:
            foo = foo[i]
            output.append(foo if type(foo) == str else foo.label)
        return output
        
# ************* TEST ***************************
if __name__ == "__main__":
    scr = pg.display.set_mode((500,500))
    font = pg.font.Font(None,25)
    scr.fill(-9000000)
    scr.blit(font.render('click please',1,(50,50,50)),(10,10))
    pg.display.flip()
    
    # create the container
    ms       = MenuSystem()
    
    # create the (sub)menus
    # Menu(items,label=None,excudes=())
    # items is an iterable of str/Menu objects
    # excudes are indices of non-reactives items
    frame    = Menu(("red","blue","white","brown"),'frame')
    alphabet = Menu("abcdefghijklmnopqrstuvwxyz",'alphabet')
    color    = Menu(("sub0","sub1",frame),"color",(0,1))
    main     = Menu(("main0",alphabet,color,"exit"),'',(0,))
    
    
    while 1:
        ev = pg.event.wait()
        if ev.type == pg.MOUSEBUTTONDOWN and not ms:
            
            # initializes the container with the main menu
            # MenuSystem.set(Menu,position,font)
            # position = (x,y)
            # font = pygame.font object
            ms.set(main,ev.pos)
            
            # MenuSystem.screen()
            # draws the menus and returns a list of rects(one for each menu displayed or deleted)
            pg.display.update(ms.screen())
        
        # updates
        # MenuSystem.update(pygame.event object)
        # returns True if there has been change
        if ms.update(ev):
            
            pg.display.update(ms.screen())
            
        # MenuSystem.OUTPUT = None
        # when you select an item
        # MenuSystem.OUTPUT contains the numeric path ...
        # [1,2,3] means submenu 1 of main menu, submenu 2 of submenu 1, item 3 of submenu 2
        if ms.OUTPUT:
            print(ms.OUTPUT,main.items(ms.OUTPUT)) # Menu.items(numeric path) returns the path changed to label
            if ms.OUTPUT == [3]: break
            if ms.OUTPUT[:2] == [2,2]: pg.display.update(pg.draw.rect(scr,pg.Color(main.items(ms.OUTPUT)[-1]),scr.get_rect(),10))
