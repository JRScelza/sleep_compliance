#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:29:29 2016

@author: jeromescelza
"""

import requests
import json
import pprint
import pandas as pd
import http
import pandas as pd
import os
import simplejson


YOUR_ACCESS_TOKEN = '0d668ea0-907c-4b8a-b479-f364549bcf27'
YOUR_API_KEY = 'i83xX2JRQPSBckYCptHNHA'


s = requests.Session()
s.headers.update({
  "Authorization": "Bearer %s" % YOUR_ACCESS_TOKEN,
  "Content-Type": "application/json"
})

token =  '0d668ea0-907c-4b8a-b479-f364549bcf27'
study_uid =  '0d3eb4ef-a53c-45f6-a4f9-188a6d6e3dce'
part = '4ce4d14c-c063-4ec2-a6ba-932a27b0d52a'
#  
url = 'https://api.ouraring.com/api/v1/study/%s/participant/%s?access_token=%s' % (study_uid, part, token)
#url = 'https://api.ouraring.com/api/v1/study/%s?access_token=%s' % (study_uid, token)
r = s.get(url)
d  = r.text

m = json.loads(d)
pp = pprint.PrettyPrinter(indent=4)

pp.pprint(m)

#fn = '/Users/jeromescelza/Box Sync/Dudley Lab and Harris Center Electronic Regulatory Binder/Trial Specific Documents/Sleep Study/Backend/OURA_jsons/ML.json'
#file = open(fn, 'w+')
#file.write(d)
#file.close 




