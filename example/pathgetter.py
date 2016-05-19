# -*- coding: utf-8 -*-
#!/usr/bin/env python
from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))

from EasyGame import pathgetter
source = pathgetter()
