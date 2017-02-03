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

np.set_printoptions(threshold=sys.maxsize)

conn = pymysql.connect(host='127.0.0.1', port=3000, user='markshervey', passwd='sher2$$$', db='device_ingest')

cur = conn.cursor()
#cur.execute("SELECT * FROM fitbit_sleep_logs")

#View all TABLE names in MySQL db
cur.execute('USE device_ingest')
cur.execute("SHOW TABLES")
tables = cur.fetchall()
#print(tables)


sub_int = 50
sub_strt_date  = datetime.date(2017,1,12)
sub_stp_date = sub_strt_date + datetime.timedelta(days=1)


#Query all tables of interest
hexoskinD = pd.read_sql('SELECT * FROM hexoskin_summary_metrics', conn)
fitbitD = pd.read_sql('SELECT * FROM fitbit_sleep_logs', conn)
hc4pwD = pd.read_sql('SELECT * FROM hc4pw_color_test', conn)
withingsD = pd.read_sql('SELECT * FROM withings_get_sleep_summary', conn)
ouraD = pd.read_sql('SELECT * FROM oura_sleep_summary', conn)


#Isolate hexoskin table by Subject Id and Start-Stop date(year-month-day)

hexs = hexoskinD.loc[(hexoskinD['subject_id'] == sub_int)]
hex_range = hexs['timerange_start_datetime']
hext = hexs.loc[((hex_range >= str(sub_strt_date)) & (hex_range <= str(sub_stp_date)))]

#Is it NaN or None. Loops through entire data set.

hexoskin_Nulls_check = pd.concat([hext['metric_name'], hext['value']], axis=1, keys=['title', 'value'])

nanFloat = float('nan')
is_it_nan = math.isnan(nanFloat)
counter = 0

for j in hexoskin_Nulls_check['value']:
    if math.isnan(j)  or j==None or j==0:
        counter = counter + 1
    else:
        break

    if counter <= 20:
    print('Subject is compliant!')
else:
    print('Subject is NOT compliant!')
    
cur.close()
conn.close()

                #Isolate fitbit table by Subject Id and Start-Stop date(year-month-day)

#fits = fitbitD.loc[(fitbitD['subject_id'] == sub_int)]
#fit_tyrange  = fits['start_time_datetime']
#fitt = fits.loc[((fit_range >= str(sub_strt_date)) & (fit_range <= str(sub_stp_date)))]
#
##Isolate hc4pw table by Subject Id and Start-Stop date(year-month-day)
#
#hc4s = hc4pwD.loc[(hc4pwD['subject_id'] == sub_int)]
#hc_range = hc4s['start_datetime']
#hc4t = hc4s.loc[((hc_range >= str(sub_strt_date)) & (hc_range <= str(sub_stp_date)))]
#
##Isolate withings table by Subject Id and Start-Stop date(year-month-day)
#
#withs = withingsD.loc[(withingsD['subject_id'] == sub_int)]
#with_range = withs['key_date']
#witht = withs.loc[((with_range >= str(sub_strt_date)) & (with_range <= str(sub_stp_date)))]
#
##Isolate oura table by Subject Id and Start-Stop date(year-month-day)
#
#ouras = ouraD.loc[(ouraD['subject_id'] == sub_int)]
#oura_range = ouras['bedtime_start_datetime']
#ourat = ouras.loc[((oura_range >= str(sub_strt_date)) & (oura_range <= str(sub_stp_date)))]


#this is checking to see if there is an unusually large amount of Null values in the value column of data




    

#sleep_compliance = data['subject_id']



