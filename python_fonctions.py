import urllib.parse
import urllib.request
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime,timedelta

# https://stackoverflow.com/questions/72186562/getting-weather-data-for-all-locations-in-us-in-python
def getWeatherForecast(LOCATION, startdate, enddate):
#    now = datetime.now()
   # startdate = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
   # enddate = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
   # LOCATION =  ["Lille"]
   try:
       for i in LOCATION:
           requestUrl = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"+i+"/"+startdate+"/"+enddate+"?unitGroup=metric&include=days&key=ZUVQJ5N739599C7DZR823CQD8&contentType=json"
           print('Weather requestUrl={requestUrl}'.format(requestUrl=requestUrl))
           req = urllib.request.urlopen(requestUrl)
           rawForecastData = req.read()
           req.close()
           d = json.loads(rawForecastData)
           time.sleep(5)
   except:
      pass
   return d