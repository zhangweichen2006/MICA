# -*- coding: utf-8 -*-
#!/usr/bin/env python
from sys import path
import os.path
import os

thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))

from EasyGame import choice

print(choice.__doc__)
lb = '''YOUR CHOICE ...
use wheel and double-click'''
lst = ['Play','Options','Credits','choice 4','choice 5','choice 6','etc ...']
print(choice(label=lb,menu=lst,mode=1,fontsize=16,width=320,height=150,frame=1,bgcolor=(250,250,250),fgcolor=(0,0,0)))

#print(choice('<centered <+b>Selectionnez un tableau<-b> >\n<centered (double-cliquez) >',os.listdir('../../'),width=600,height=300,fgcolor=(250,250,250),bgcolor=(200,60,40)))
