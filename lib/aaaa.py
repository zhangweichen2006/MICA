from pygame import *
scr = display.set_mode((500,500))
import Entry
fiche = """<#ffffff><+b>n<-b><#>ame :       <20,20>
<#ffffff><+b>f<-b><#>irst <#ffffff><+b>n<-b><#>ame : <20,20>
<#ffffff><+b>o<-b><#>ld :        <3,3> <#ffffff><+b>y<-b><#>ears"""

Entry.get(fiche,'<centered <+i>Entry Test<-i> >',fontsize=15,bgcolor=(20,20,20),fgcolor=(200,100,10))
