from pygame import time,event,init,mouse,display
from pygame.locals import *

time.Clock()

class Pyca(list):
    ''
    def __init__(self,Item=[]):
        if hasattr(Item, '__iter__'): self.extend(Item)
        else: self.append(Item)
        self._Last_over = None
    
    @property
    def ITEM(self): return self._Last_over

MOUSEOVER = USEREVENT
LOSEFOCUS = USEREVENT+1

_Clic = [0,0,0,0,0,0]
_Ticks = [0,0,0,0,0,0]
_Pos = Rect(mouse.get_pos(),(0,0))

_FOCUSED = None

def wait(l):
    e=event.wait()
    _foo(l,e)
    return e

def poll(l):
    e=event.poll()
    _foo(l,e)
    return e

def get(l):
    ev=event.get()
    for e in ev: _foo(l,e)
    return ev


def _foo(l,e):
    global _Clic,_Ticks
    if e.type==MOUSEBUTTONDOWN:
        t = time.get_ticks()
        if e.button!=_Clic[0] or t-_Ticks[e.button]>200: _Clic=[e.button,0,0,0,0,0]
        _Ticks[e.button] = t
    elif e.type==MOUSEBUTTONUP:
        t = time.get_ticks()
        if t-_Ticks[e.button]>200: _Clic=[e.button,0,0,0,0,0]
        else:
            _Clic[e.button]+=1
            _Ticks[e.button] = t
        e.dict.update({'clic':_Clic})
    if e.type in (MOUSEBUTTONDOWN,MOUSEBUTTONUP) and  hasattr(l._Last_over,'wakeup'): l._Last_over.wakeup(e)
    else: process(l,e)

def process(l,e):
    global _FOCUSED
    def find_new_over(l):
        for i in l:
            try:
                if i.collidepoint(_Pos.topleft):
                    try:
                        if i.MASK.get_at(_Pos.move(-i.left,-i.top).topleft): return i
                        else: return None
                    except: return i
            except:
                i = find_new_over(i[::-1])
                if i: return i
        return None
    
    if e.type == MOUSEMOTION: _Pos.topleft = e.pos
    elif e.type in (KEYDOWN,KEYUP) and hasattr(_FOCUSED,'wakeup'): _FOCUSED.wakeup(e)
    if e.type not in (KEYDOWN,KEYUP) and hasattr(l._Last_over,'wakeup'): l._Last_over.wakeup(e)

    if not l._Last_over or not l._Last_over.collidepoint(_Pos.topleft):
        if hasattr(l._Last_over,'wakeup'): l._Last_over.wakeup(event.Event(MOUSEOVER,{'over':0}))
        l._Last_over = find_new_over(l[::-1])
        if hasattr(l._Last_over,'wakeup'): l._Last_over.wakeup(event.Event(MOUSEOVER,{'over':1}))
    '''
    new_over = find_new_over(l[::-1])
    if id(new_over) != id(l._Last_over):
        try: l._Last_over.wakeup(event.Event(MOUSEOVER,{'over':0,pos:_Pos.topleft}))
        except: pass
        l._Last_over = new_over
        try: new_over.wakeup(event.Event(MOUSEOVER,{'over':1,pos:_Pos.topleft}))
        except: pass
    '''
def focus(item):
    global _FOCUSED
    if not(item is _FOCUSED) and hasattr(_FOCUSED,'wakeup'): _FOCUSED.wakeup(event.Event(LOSEFOCUS))
    _FOCUSED = item

def unfocus(item):
    global _FOCUSED
    if not(item is _FOCUSED):
        _FOCUSED = None

#------------------------------------------------------------------
#------------------------------------------------------------------

import thread
_lock = thread.allocate_lock()

_Items = []
Bg = None
_Clock = time.Clock()

def show(item):
    if hasattr(item,'__iter__'):
        for i in item: show(i)
    elif not item in _Items: _Items.append(item)
    if not _lock.locked():
        _lock.acquire()
        thread.start_new_thread(update,())

def update():
    global _Items
    Screen = display.get_surface()
    while _Items:
        S = _Items
        _Items = []
        _Update = []
        for i in S:
            Screen.blit(Bg,i,i)
            if hasattr(i,'Img'): Screen.blit(i.Img,i)
            _Update.append(i)
        display.update(_Update)
        _Clock.tick(30)
    _lock.release()
#------------------------------------------------------------------
#------------------------------------------------------------------

import thread
shed_lock = thread.allocate_lock()
shed_id = None
shed_dict = {}

def shed_it():
    shed_lock.acquire()
    global shed_id
    shed_id = this_id = thread.get_ident()
    while shed_dict:
        t,proc = min(zip(shed_dict.values(),shed_dict.keys()))
        if t-time.get_ticks() <= 0:
            new_t = proc()
            if not new_t: del(shed_dict[proc])
            elif proc in shed_dict: shed_dict[proc] = new_t + t
        else:
            shed_lock.release()
            time.wait(t-time.get_ticks())
            if this_id != shed_id: break
            shed_lock.acquire()
    if this_id == shed_id: shed_lock.release()

def timeit(proc,delay=0):
    if delay >= 0:
        shed_dict[proc] = time.get_ticks()+delay
        if not shed_lock.locked():
            thread.start_new_thread(shed_it,())
    elif proc in shed_dict: del(shed_dict[proc])
