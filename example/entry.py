# -*- coding: utf-8 -*-
#!/usr/bin/env python
from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))


from EasyGame import entry
fiche = """<#ffffff><+b>n<-b><#>ame :       <20,20>
<#ffffff><+b>f<-b><#>irst <#ffffff><+b>n<-b><#>ame : <20,20>
<#ffffff><+b>o<-b><#>ld :        <3,3> <#ffffff><+b>y<-b><#>ears"""

print(entry(fiche,'<centered <+i>Entry Test<-i> >',fontsize=15,width=450,bgcolor=(20,20,20),fgcolor=(200,100,10)))
