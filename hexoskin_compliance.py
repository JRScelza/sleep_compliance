
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


i = 51
sub_strt_date  = datetime.datetime(2017,1,15)
sub_stp_date = sub_strt_date + datetime.timedelta(days=1)


for j in range(0,7):
    hexoskinD = pd.read_sql('SELECT * FROM hexoskin_summary_metrics', conn)
    position_hex = 0
    subplot_count = 0
    time.sleep(1)
    
    
    
    hexs = hexoskinD.loc[(hexoskinD['subject_id'] == i)]
    hex_range = hexs['timerange_start_datetime']
    hext = hexs.loc[((hex_range >= str(sub_strt_date)) & (hex_range <= str(sub_stp_date)))]
    
    hexoskin_Nulls_check = pd.concat([hext['metric_name'], hext['value']], axis=1, keys=['title', 'value'])
    #    hexoskin_Nulls_check.sort_index(inplace=True)
    hexoskin_Nulls_check['title'] = hexoskin_Nulls_check['title'].str.lower()
    hexoskin_Nulls_check.sort(columns=['title'], axis=0, ascending=True, inplace=True)
    #    hexoskin_Nulls_check.drop('title', axis=1, inplace=True)
    hexoskin_Nulls_check.index = range(0,len(hexoskin_Nulls_check))
    
    
    
    
    if hexoskin_Nulls_check.empty:
        print('*******NO DATA TO PLOT HEXOSKIN FOR SUBJECT %s*********' % i)
    #    compliance_list.iloc[position_hex,2] = 'FAIL'
    else:
        hexoskin_metrics = hexoskin_Nulls_check.loc[[0,8,18,14,88],['title']]
        hexoskin_values = hexoskin_Nulls_check.loc[[0,8,18,14,88],['value']]
        plt.figure(subplot_count)
        x = range(0,len(hexoskin_values))
        y = hexoskin_values['value']
        colors = ['#624ea7', 'g', 'yellow', 'k', 'maroon']
        plt.bar(x, y, color=colors)
        plt.title('Hexoskin Summary Subject %d' % i)
        my_xticks = hexoskin_metrics['title']
        plt.xticks(x, my_xticks, rotation=45)
        subplot_count = subplot_count + 1
        plt.show()
        
    #    compliance_list.iloc[position_hex,2] = 'PASS'
    
    #compliance_list.iloc[position_hex,0] = '%d' % i
    
    
    #    nanFloat = float('nan')
    #    is_it_nan = math.isnan(nanFloat)
    counter = 0
    position_hex = position_hex + 1
    subplot_count = 1
    sub_strt_date  = sub_strt_date + datetime.timedelta(days=1)
    sub_stp_date = sub_strt_date + datetime.timedelta(days=1)