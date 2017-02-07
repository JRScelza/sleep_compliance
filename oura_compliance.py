#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 13:42:12 2017

@author: jeromescelza
"""

import pymysql
import requests
import json
import pprint
import pandas as pd
import datetime
import math
import numpy as np
import sys
import matplotlib.pyplot as plt
from IPython.display import display
import time
import warnings

warnings.filterwarnings("ignore")


#pd.set_option('display.height', 200cd
#pd.set_option('display.max_rows', 800)

conn = pymysql.connect(host='127.0.0.1', port=3000, user='jeroscel', passwd='Defense43*55', db='device_ingest')

cur = conn.cursor()

#View all TABLE names in MySQL db
cur.execute('USE device_ingest')
cur.execute("SHOW TABLES")
tables = cur.fetchall()


#sub_int = [52, 53, 55, 56, 57, 58]
#sub_int = [55]
i = 51
sub_strt_date  = datetime.datetime(2017,1,14)
sub_stp_date = sub_strt_date + datetime.timedelta(days=1)


for j in range(0,7):
    now  = datetime.datetime.now()
    strt_date_temp  = datetime.datetime(now.year, now.month, now.day, hour=14)
    #sub_strt_date  = strt_date_temp - datetime.timedelta(days=4)
    
    
    ouraD = pd.read_sql('SELECT * FROM oura_sleep_summary', conn)
    position_oura = -1
    subplot_count = 211
    
    print(sub_strt_date)
    
    
    #for i in sub_int:
    ouras = ouraD.loc[(ouraD['subject_id'] == i)]
    oura_range = ouras['bedtime_start_datetime']
    ourat = ouras.loc[((oura_range >= str(sub_strt_date)) & (oura_range <= str(sub_stp_date)))]
    ourat.index = range(0,len(ourat))
    
    oura_sleep_metrics = ['rem', 'awake', 'total']
    
    counter = 0
    position_oura = position_oura + 1
    
        
    if ourat.empty:
    #        compliance_list.iloc[position_with,5] = 'FAIL'
            print('*******NO DATA TO PLOT OURA FOR SUBJECT %s*********' % i)
    else:
    #        compliance_list.iloc[position_with,5] = 'PASS'
            
            oura_duration = ourat.iloc[0]['total']
            plt.figure(subplot_count)
            y = ourat.iloc[0][oura_sleep_metrics]
            x = range(0,(len(y)))
            colors = ['#624ea7', 'g', 'yellow', 'k', 'maroon']
            plt.bar(x, y, color=colors)
            plt.title('OURA Summary Subject %d' % i)
            my_xticks = oura_sleep_metrics
            plt.xticks(x, my_xticks, rotation=45)
            
            subplot_count = subplot_count + 1
            
            plt.show()
    sub_strt_date  = sub_strt_date + datetime.timedelta(days=1)
    sub_stp_date = sub_strt_date + datetime.timedelta(days=1)
        
