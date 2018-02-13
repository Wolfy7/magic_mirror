'''
Created on 15.04.2017

@author: Wolfy7
'''
import urllib.request
import json
import logging


class FORECASTIO:
    def __init__(self):
        self.DarkSkyKey = '' # get darksky api key from https://darksky.net/  
        self.Latitude, self.Longitude = 50.608831, 8.791009 # Latitude, Longitude from 'Grossen-Buseck'
        self.URL = "https://api.darksky.net/forecast/"
        self.request = self.URL+self.DarkSkyKey+"/%.6f,%.6f?lang=de&units=auto" % (self.Latitude, self.Longitude)
        self.counter = 0
        
    def getForecast(self):         
        try:
            self.response = urllib.request.urlopen(self.request).read().decode('utf-8')
            #print(response)
            self.data = json.loads(self.response)
            #print(data)
            #self.counter += 1
            return self.data
        except urllib.error.HTTPError as e:
            #print(e)
            logging.error(e)    
        except urllib.error.URLError as e:
            #print(e)
            logging.error(e)   
            
            
    def getWatherImage(self,icon, size):
        if icon == "clear-day":
            return '/home/pi/magic-mirror/weather_icons/clear-day-'+size+'.png'
        elif icon == "clear-night": 
            return '/home/pi/magic-mirror/weather_icons/clear-night-'+size+'.png'
        elif icon == "rain": 
            return '/home/pi/magic-mirror/weather_icons/rain-'+size+'.png'
        elif icon == "snow": 
            return '/home/pi/magic-mirror/weather_icons/snow-'+size+'.png'
        elif icon == "sleet": 
            return '/home/pi/magic-mirror/weather_icons/sleet-'+size+'.png'
        elif icon == "wind": 
            return '/home/pi/magic-mirror/weather_icons/wind-and-cloud-'+size+'.png' 
        elif icon == "fog": 
            return '/home/pi/magic-mirror/weather_icons/foggy-'+size+'.png'
        elif icon == "cloudy": 
            return '/home/pi/magic-mirror/weather_icons/cloudy-'+size+'.png' 
        elif icon == "partly-cloudy-day": 
            return '/home/pi/magic-mirror/weather_icons/partly-cloudy-day-'+size+'.png'
        elif icon == "partly-cloudy-night": 
            return '/home/pi/magic-mirror/weather_icons/partly-cloudy-night-'+size+'.png'
        elif icon == "hail": 
            return '/home/pi/magic-mirror/weather_icons/hail-'+size+'.png'
        elif icon == "thunderstorm": 
            return '/home/pi/magic-mirror/weather_icons/thunderstorm-clouds-'+size+'.png'
        elif icon == "tornado": 
            return '/home/pi/magic-mirror/weather_icons/tornado-'+size+'.png'
        
        return '/home/pi/magic-mirror/weather_icons/image-not-found-'+size+'.png'
