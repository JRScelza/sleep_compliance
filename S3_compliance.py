#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 17:13:14 2017

@author: jeromescelza
"""

import os
import datetime

now = datetime.datetime.now()

a = now.year
b = now.month
c = now.day

date = "%d-%d-%d" % (a, b, c)

print(date)

compliance = os.path.isfile('./file.txt')

print(compliance)    # True  

              
