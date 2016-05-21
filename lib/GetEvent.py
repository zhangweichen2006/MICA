from pygame import time,event,MOUSEBUTTONDOWN,MOUSEBUTTONUP

_Clic = [0,0,0,0,0,0]
_Ticks = [0,0,0,0,0,0]
LAPS = 200
time.Clock()

def wait():
    ev=event.wait()
    _foo(ev)
    return ev

def poll():
    ev=event.poll()
    _foo(ev)
    return ev

def get():
    ev=event.get()
    for e in ev: _foo(e)
    return ev

def _foo(e):
    global _Clic,_Ticks
    if e.type==MOUSEBUTTONDOWN:
        t = time.get_ticks()
        if e.button!=_Clic[0] or t-_Ticks[e.button]>LAPS: _Clic=[e.button,0,0,0,0,0]
        _Ticks[e.button] = t
    elif e.type==MOUSEBUTTONUP:
        t = time.get_ticks()
        if t-_Ticks[e.button]>LAPS: _Clic=[e.button,0,0,0,0,0]
        else:
            _Clic[e.button]+=1
            _Ticks[e.button] = t
        e.dict.update({'click':_Clic})
