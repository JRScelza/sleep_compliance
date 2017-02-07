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
now  = datetime.datetime.now()
strt_date_temp  = datetime.datetime(now.year, now.month, now.day, hour=14)
#sub_strt_date  = strt_date_temp - datetime.timedelta(days=4)


i = 51
sub_strt_date = datetime.datetime(2017,1,20)
sub_stp_date = sub_strt_date + datetime.timedelta(days=1)



for j in range(0,7):
    fitbitD = pd.read_sql('SELECT * FROM fitbit_sleep_logs', conn)
    position_fit = -1
    subplot_count = 111
    
    
    fits = fitbitD.loc[(fitbitD['subject_id'] == i)]
    fit_range = fits['date_of_sleep_datetime']
    fit_duration = fits.loc[((fit_range >= str(sub_strt_date)) & (fit_range <= str(sub_stp_date)))]
    fit_duration.index = range(0,len(fit_duration))
    
    fitbit_sleep_metrics = ['minutes_asleep', 'minutes_awake', 'time_in_bed', 'restless_duration', 'total_minutes_asleep']
    
    fitbit_duration_check = fit_duration['sleep_duration']
    counter = 0
    position_fit = position_fit + 1
        
    if  i in fitbit_duration_check <= 18000000 or fitbit_duration_check.empty:
    #        compliance_list.iloc[position_fit,4] = 'FAIL'
            print('FAIL')
    else:
    #       compliance_list.iloc[position_fit,4] = 'PASS'
            print("PASS")
            x = range(0,len(fitbit_sleep_metrics))
            y = fit_duration.iloc[0][fitbit_sleep_metrics]
            plt.bar(x, y)
            plt.title('Fitbit Summary Subject %d' % i)
            my_xticks = fitbit_sleep_metrics
            plt.xticks(x, my_xticks, rotation=45)
            
            subplot_count = subplot_count + 1
            
            plt.show()
    sub_strt_date = sub_strt_date + datetime.timedelta(days=1)
    sub_stp_date = sub_strt_date + datetime.timedelta(days=1)