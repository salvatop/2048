#!/usr/bin/env python3

"""
Created on Thu Nov  8 11:53:33 2016

@author: Salvatore Palazzo
"""

"""
print now time formatted
"""
from datetime import datetime

def printNow():
  now = datetime.now() 
  print ('%s/%s/%s %s:%s:%s' % (now.day, now.month, now.year, now.hour, now.minute, now.second))

    

