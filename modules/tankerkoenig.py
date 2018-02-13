'''
Created on 12.05.2017

@author: Wolfy7
'''
import urllib.request
import json
import logging


class TKrequestException(Exception):
    pass


class TANKERKOENIG:
    def __init__(self):
        self.ApiKey = '' # get api key from https://creativecommons.tankerkoenig.de  
        self.Latitude, self.Longitude = 50.608831, 8.791009 # Latitude, Longitude from 'Grossen-Buseck'
        self.PetrolStationID = '717e4226-67ca-4941-967f-063f12f891bd' # Mengin Tank-Stop Buseck
        self.URL = "https://creativecommons.tankerkoenig.de/json"
        #self.request = self.URL+self.DarkSkyKey+"/%.6f,%.6f?lang=de&units=auto" % (self.Latitude, self.Longitude)
        
        self.counter = 0
        
    def getPetrolPrices(self):         
        try:
            self.PriceRequest = self.URL+"/prices.php?ids="+self.PetrolStationID+"&apikey="+self.ApiKey
            self.response = urllib.request.urlopen(self.PriceRequest).read().decode('utf-8')
            #print(response)
            self.data = json.loads(self.response)
            
            if(self.data['ok'] == False):
                raise TKrequestException(self.data['message']) 
            #print(data)
            #self.counter += 1
            return self.data['prices'][self.PetrolStationID]
        except urllib.error.HTTPError as e:
            #print(e)
            logging.error(e)    
        except urllib.error.URLError as e:
            #print(e)
            logging.error(e)   
        except TKrequestException as e:
            #print(e)
            logging.error(e)            