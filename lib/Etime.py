#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import time

class Etime(object):
    """This class defines a timer"""
    
    def __init__(self,t=0):
        """the t arg is either an int or a tuple defined as follows (hours, minutes, seconds)"""
        self.clock = time.Clock()
        try:
            h,m,s = t
            self._t = h*3600000+m*60000+s*1000
        except:
            self._t = t
        self._susp = True
    
    def start(self):
        """start the timer"""
        self.resume()
    
    def suspend(self):
        """suspend the timer"""
        self._t += self.clock.tick()
        self._susp = True
    
    def resume(self):
        self.clock.tick()
        self._susp = False
    
    def reset(self,t=0):
        try:
            h,m,s = t
            self._t = h*3600000+m*60000+s*1000
        except:
            self._t = t        
        
    def __repr__(self):
        return '%i : %#02i : %#02i <%s>'%(self.h,self.m,self.s,self.state)
        
    @property
    def s(self):
        if not self._susp:
            self._t += self.clock.tick()
        return self._t//1000%60
        
    @property
    def m(self):
        if not self._susp:
            self._t += self.clock.tick()
        return self._t//60000%60
        
    @property
    def h(self):
        if not self._susp:
            self._t += self.clock.tick()
        return self._t//3600000
        
    @property
    def raw(self):
        return self._t
        
    @property
    def state(self):
        return 'suspended'if self._susp else 'running'
