from subprocess import Popen,PIPE
from os.path import dirname,join,abspath
lib = join(dirname(__file__),'lib')
import pickle
Entry = join(lib,'Entry.py')
Confirm = join(lib,'Confirm.py')
PathGetter = join(lib,'PathGetter.py')
Choice = join(lib,'Choice.py')
from sys import path

def entry(label='<1,1>',title='',fontsize=16,width=320,frame=True,bgcolor=(200,200,200),fgcolor=(0,0,0)):
    #return list of string
    p = Popen(["python", Entry],stdout=PIPE,stdin=PIPE)
    p.stdin.write(pickle.dumps([label,title,fontsize,width,frame,bgcolor,fgcolor],protocol=2))
    return pickle.loads(p.communicate()[0])

def confirm(label='...',title='',mode=3,fontsize=16,width=320,bgcolor=(250,250,250),fgcolor=(0,0,0)):
    p = Popen(["python", Confirm],stdout=PIPE,stdin=PIPE)
    p.stdin.write(pickle.dumps([label,title,mode,fontsize,width,bgcolor,fgcolor],protocol=2))
    return pickle.loads(p.communicate()[0])

def pathgetter(path='',mode=0,caption=''):
    if not mode in (1,2): mode = 0
    p = Popen(["python", PathGetter],stdout=PIPE,stdin=PIPE)
    p.stdin.write(pickle.dumps([path,mode,caption],protocol=2))
    return pickle.loads(p.communicate()[0])

def choice(label='YOUR CHOICE',menu=[],mode=1,fontsize=16,width=320,height=None,frame=True,bgcolor=(250,250,250),fgcolor=(0,0,0)):
    """choice([label][,menu][,mode][,fontsize][,width][,height][,frame][,bgcolor][,fgcolor])
    label='YOUR CHOICE'
    menu=[]
    mode=1 not used
    fontsize=16
    width=320
    height=None
    frame=True
    bgcolor=(250,250,250)
    fgcolor=(0,0,0)
    
    returns tuple (int,unicode) ==> (entry numbers,entry)
    if no entry was selected, returns (len(menu),u'')"""
    p = Popen(["python", Choice],stdout=PIPE,stdin=PIPE)
    p.stdin.write(pickle.dumps([label,menu,mode,fontsize,width,height,frame,bgcolor,fgcolor],protocol=2))
    return pickle.loads(p.communicate()[0])
