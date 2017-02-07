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




now  = datetime.datetime.now()
strt_date_temp  = datetime.datetime(now.year, now.month, now.day, hour=14)
#sub_strt_date  = strt_date_temp - datetime.timedelta(days=4)

i = 51
sub_strt_date  = datetime.datetime(2017,1,14)
sub_stp_date = sub_strt_date + datetime.timedelta(days=1)

for j in range(0,7):
    
    withingsD = pd.read_sql('SELECT * FROM withings_get_sleep_summary', conn)
    position_with = -1
    subplot_count = 211
    
    print(sub_strt_date)
    
    
    #for i in sub_int:
    withs = withingsD.loc[(withingsD['subject_id'] == i)]
    with_range = withs['api_start_datetime']
    witht = withs.loc[((with_range >= str(sub_strt_date)) & (with_range <= str(sub_stp_date)))]
    withings_duration_check = pd.concat([witht['metric'], witht['value']], axis=1, keys=['title', 'value'])
    withings_duration_check.sort(columns=['title'], axis=0, ascending=True, inplace=True)
    withings_duration_check.index = range(0,len(withings_duration_check))
    withings_duration_check = withings_duration_check.drop_duplicates(subset='title', keep='first')
    
    with_duration = withings_duration_check['value'].sum(axis=0)
    counter = 0
    position_with = position_with + 1
    
        
    if  with_duration <= 15000 or withings_duration_check.empty:
    #        compliance_list.iloc[position_with,3] = 'FAIL'
            print('*******NO DATA TO PLOT WITHINGS FOR SUBJECT %s*********' % i)
    else:
    #        compliance_list.iloc[position_with,3] = 'PASS'
            
            plt.figure(subplot_count)
            x = range(0,len(withings_duration_check))
            y = withings_duration_check['value']
            colors = ['#624ea7', 'g', 'yellow', 'k', 'maroon']
            plt.bar(x, y, color=colors)
            plt.title('Withings Summary Subject %d' % i)
            my_xticks = withings_duration_check['title']
            plt.xticks(x, my_xticks, rotation=45)
            
            subplot_count = subplot_count + 1
            
            plt.show()
    sub_strt_date  = sub_strt_date + datetime.timedelta(days=1)
    sub_stp_date = sub_strt_date + datetime.timedelta(days=1)