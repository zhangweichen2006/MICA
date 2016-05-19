from pygame import *
from base64 import b64encode,b64decode
from io  import StringIO
#import numpy

def applies_alpha(surface1,surface2):
    output = surface2.copy().convert_alpha()
    surfarray.pixels_alpha(output)[:] = surfarray.array_alpha(surface1)
    return output
    
def applies_alpha_ip(surface1,surface2):
    surfarray.pixels_alpha(surface2)[:] = surfarray.array_alpha(surface1)

def min_alpha(surface1,surface2):
    output = surface2.copy().convert_alpha()
    output_alpha = surfarray.pixels_alpha(output)
    S1_alpha = surfarray.array_alpha(surface1)
    output_alpha[S1_alpha < output_alpha] = S1_alpha[S1_alpha < output_alpha]
    return output
    
def min_alpha_ip(surface1,surface2):
    S2_alpha = surfarray.pixels_alpha(surface2)
    S1_alpha = surfarray.array_alpha(surface1)
    S2_alpha[S1_alpha < S2_alpha] = S1_alpha[S1_alpha < S2_alpha]

def crop_alpha(surface):
    s = surfarray.array_alpha(surface)
    a = []
    for i in '    ':
        c = 0
        while not any(s[c]): c+=1
        a.append(c)
        s = s.transpose()[::-1]
    x,yy,xx,y = a
    #output = Surface((surface.get_width()-x-xx,surface.get_height()-y-yy),SRCALPHA)
    #output.fill((0,0,0,0))
    #output.blit(surface,(-x,-y))
    #return output
    return surface.subsurface((x,y,surface.get_width()-x-xx,surface.get_height()-y-yy)).copy()

def autocrop(surf,distance=0):
    color = surf.get_at((0,0))
    Pxarray = PixelArray(surf).extract (color,distance,(0.299, 0.587, 0.114))
    a = []
    for i in '    ':
        c = 0
        while all(Pxarray[c]): c+=1
        a.append(c)
        Pxarray = zip(*Pxarray)[::-1]
    x,yy,xx,y = a
    #output = Surface((surf.get_width()-x-xx,surf.get_height()-y-yy),SRCALPHA)
    #output.fill((0,0,0,0))
    #output.blit(surf,(-x,-y))
    #return output
    return surface.subsurface((x,y,surface.get_width()-x-xx,surface.get_height()-y-yy)).copy()

def mrange(start,stop,step,type_=None):
    if hasattr(start,'__iter__'): return list(zip(*[mrange(x,y,step,type_) for x,y in zip(start,stop)]))
    s,v = stop-start,step-1.
    if (not type_ and type(stop-start) is int) or (type_ is int): return [int(round((s*i)/v+start)) for i in range(step)]
    return [(s*i)/v+start for i in range(step)]

def scroll(surface,x,y):
    sx,sy = surface.get_size()
    output = surface.copy()
    if x<0:
        output.scroll(x)
        output.fill((0,0,0,0),(sx+x,0,-x,sy))
        output.blit(surface,(sx+x,0),(0,0,-x,sy))
    elif x>0:
        output.scroll(x)
        output.fill((0,0,0,0),(0,0,x,sy))
        output.blit(surface,(0,0),(sx-x,0,x,sy))
    if y<0:
        output.scroll(0,y)
        output.fill((0,0,0,0),(0,sy+y,sx,-y))
        output.blit(surface,(0,sy+y),(0,0,sx,-y))
    elif y>0:
        output.scroll(0,y)
        output.fill((0,0,0,0),(0,0,sx,y))
        output.blit(surface,(0,0),(0,sy-y,sx,y))
    return output


def scroll_ip(surface,x,y):
    sx,sy = surface.get_size()
    y = y%sy
    x = x%sx
    if x<0:
        cp = surface.subsurface(sx+x,0,-x,sy).copy()
        surface.scroll(x)
        #surface.fill((0,0,0,0),(sx+x,0,-x,sy))
        surface.blit(cp,(sx+x,0))
    elif x>0:
        cp = surface.subsurface(sx-x,0,x,sy).copy()
        surface.scroll(x)
        #surface.fill((0,0,0,0),(0,0,x,sy))
        surface.blit(cp,(0,0))
    if y<0:
        cp = surface.subsurface(0,0,sx,-y).copy()
        surface.scroll(0,y)
        #surface.fill((0,0,0,0),(0,sy+y,sx,-y))
        surface.blit(cp,(0,sy+y))
    elif y>0:
        cp = surface.subsurface(0,sy-y,sx,y).copy()
        surface.scroll(0,y)
        #surface.fill((0,0,0,0),(0,0,sx,y))
        surface.blit(cp,(0,0))

def img_to_b64string(imgpath):
    return b64encode(open(imgpath).read())

def img_from_b64string(string):
    return image.load(StringIO(b64decode(string)))
