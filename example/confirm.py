# -*- coding: utf-8 -*-
#!/usr/bin/env python
from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))




from EasyGame import confirm

label = """<centered <+b>this <+u>is<-b> <+i>a test<-u> with <-i>mode =%i >"""

r = confirm(label%1,fontsize=16,width=660,mode=1,fgcolor=(200,100,10),bgcolor=(20,20,20))
r = confirm(label%2+'\nyou have clicked '+{True:'valid',False:'cancel',None:'back'}[r],'Confirm Example',fontsize=16,width=360,mode=2)
r = confirm(label%3+'\nyou have clicked '+{True:'valid',False:'cancel',None:'back'}[r],'Confirm Example',fontsize=16,width=360,mode=3)
confirm('you have clicked '+{True:'valid',False:'cancel',None:'back'}[r]+'\nnow quit','Confirm Example',fontsize=16,width=360,mode=1)
