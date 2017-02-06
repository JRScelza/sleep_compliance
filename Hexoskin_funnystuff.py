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


sub_int = [52, 53, 55, 56, 57, 58]
now  = datetime.datetime.now()
strt_date_temp  = datetime.datetime(now.year, now.month, now.day, hour=14)
sub_strt_date  = strt_date_temp - datetime.timedelta(days=4)
sub_stp_date = sub_strt_date + datetime.timedelta(days=1)


#Query all tables of interest
compliance_list = pd.DataFrame(np.zeros((len(sub_int), 6)))
compliance_head = ['Subject_id' ,'Hc4pw' , 'Hexoskin', 'Withings', 'FitBit', 'OURA' ]
compliance_list.columns = compliance_head
compliance_list.applymap(str)



print('-------------------------------------------------------------------------')
print('-------------------------------------------------------------------------')
print('------------------------COMPLIANCE REPORT--------------------------------')
print('---------------------------SLEEP STUDY-----------------------------------')
print('-------------%s----%s-------------------' % (str(sub_strt_date), str(sub_stp_date)))
print('-------------------------------------------------------------------------')
print('-------------------------------------------------------------------------')



#****************************HEXOSKIN*******************************************
#****HEXOSKIN COMPLIANCE BASED ON NUMBER OF NAN'S / NULL'S & SLEEP DURATION*****
#*******************************************************************************

hexoskinD = pd.read_sql('SELECT * FROM hexoskin_summary_metrics', conn)
position_hex = 0

time.sleep(1)

for i in sub_int:
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
        compliance_list.iloc[position_hex,2] = 'FAIL'
    else:
        hexoskin_metrics = hexoskin_Nulls_check.loc[[0,8,18,14,88],['title']]
        hexoskin_values = hexoskin_Nulls_check.loc[[0,8,18,14,88],['value']]
        plt.figure(subplot_count)
        x = range(0,len(hexoskin_values))
        y = hexoskin_values['value']
        plt.bar(x, y)
        plt.title('Hexoskin Summary Subject %d' % i)
        my_xticks = hexoskin_metrics['title']
        plt.xticks(x, my_xticks, rotation=45)
        subplot_count = subplot_count + 1
        plt.show()
        
        compliance_list.iloc[position_hex,2] = 'PASS'

    compliance_list.iloc[position_hex,0] = '%d' % i

#    nanFloat = float('nan')
#    is_it_nan = math.isnan(nanFloat)
    counter = 0
    position_hex = position_hex + 1
    subplot_count = 1
#    hexoskin_values = hexoskin_values.astype(float).fillna(0.0)
    
#    
#    for j in hexoskin_Nulls_check['value']:
#        if math.isnan(j)  or j==None or j==0:
#            counter = counter + 1
#    
#    
#    if counter >= 20 or hexoskin_Nulls_check.empty:
#        compliance_list.iloc[position_hex,2] = 'FAIL'
#    else:
#        compliance_list.iloc[position_hex,2] = 'PASS' 
        

            
   
#****************************FITBIT*******************************************
#****FITBIT COMPLIANCE BASED ON NUMBER OF NAN'S / NULL'S & SLEEP DURATION*****
#*******************************************************************************

fitbitD = pd.read_sql('SELECT * FROM fitbit_sleep_logs', conn)
position_fit = -1
subplot_count = 111

for i in sub_int:
    fits = fitbitD.loc[(fitbitD['subject_id'] == i)]
    fit_range = fits['date_of_sleep_datetime']
    fitt = fits.loc[((fit_range >= str(sub_strt_date)) & (fit_range <= str(sub_stp_date)))]
    
    
    fitbit_duration_check = fitt['sleep_duration']
    counter = 0
    position_fit = position_fit + 1
    
    if  i in fitbit_duration_check <= 18000000 or fitbit_duration_check.empty:
        compliance_list.iloc[position_fit,4] = 'FAIL'
    else:
        compliance_list.iloc[position_fit,4] = 'PASS'
        x = range(0,len(fitt))
        y = fitbit_duration_check['value']
        plt.bar(x, y)
        plt.title('Fitbit Summary Subject %d' % i)
        my_xticks = withings_duration_check['title']
        plt.xticks(x, my_xticks, rotation=45)
        
        subplot_count = subplot_count + 1
        
        plt.show()
        
        

#****************************WITHINGS*******************************************
#****WITHINGS COMPLIANCE BASED ON NUMBER OF NAN'S / NULL'S & SLEEP DURATION*****
#*******************************************************************************


    withingsD = pd.read_sql('SELECT * FROM withings_get_sleep_summary', conn)
    position_with = -1
    subplot_count = 211
    
for i in sub_int:
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
            compliance_list.iloc[position_with,3] = 'FAIL'
            print('*******NO DATA TO PLOT WITHINGS FOR SUBJECT %s*********' % i)
    else:
            compliance_list.iloc[position_with,3] = 'PASS'
            
            plt.figure(subplot_count)
            x = range(0,len(withings_duration_check))
            y = withings_duration_check['value']
            plt.bar(x, y)
            plt.title('Withings Summary Subject %d' % i)
            my_xticks = withings_duration_check['title']
            plt.xticks(x, my_xticks, rotation=45)
            
            subplot_count = subplot_count + 1
            
            plt.show()

#*********************************HC4PW****************************************
#***********QUESTIONS AND HOW MANY HAVE BEEN ANSWERED IN ENTIRETY**************
#*******************************************************************************


hc4pwD = pd.read_sql('SELECT * FROM hc4pw_questionnaire', conn)
position_hc4pw = -1


for i in sub_int:
    hc4pws = hc4pwD.loc[(hc4pwD['subject_id'] == i)]
    hc4pw_range = hc4pws['questionnaire_datetime']
    hc4pwt = hc4pws.loc[((hc4pw_range >= str(sub_strt_date)) & (hc4pw_range <= str(sub_stp_date)))]
    hc4pw_check = hc4pwt['question']
    hc4pw_check.index = range(0,len(hc4pw_check))
    
    position_hc4pw = position_hc4pw + 1

    if  len(hc4pw_check) < 13 or hc4pw_check.empty:
            compliance_list.iloc[position_hc4pw,1] = 'FAIL'
    else:
            compliance_list.iloc[position_hc4pw,1] = 'PASS'

                              
print('        ')                     
print(' %s Pass / Fail Report for Sleep_Study' % str(now))
print('        ')


#def color_fail_red(val):
#    """
#    Takes a scalar and returns a string with
#    the css property `'color: red'` for negative
#    strings, black otherwise.
#    """
#    color = 'red' if val == 'FAIL'  else 'black'
#    return 'color: %s' % color
#
#s = compliance_list.style.applymap(color_fail_red))

print(compliance_list)
#print(hexoskin_Nulls_check)
        
cur.close()
conn.close()





