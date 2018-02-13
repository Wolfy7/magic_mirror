'''
Created on 19.05.2017

@author: Wolfy7
'''
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
    
    
class GOOGLECALENDAR:
    def __init__(self):     
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/calendar-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Calendar API'
        
        self.todaylist = []
        self.tomorrowlist = []
        self.tdatlist = []
        self.tdaatlist = []

    def get_credentials(self):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        #print(os.getcwd())
        home_dir = '/home/pi/magic-mirror/'
        #home_dir = os.getcwd()
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials


    def eventlist(self, event):   
        today = datetime.datetime.now()
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1))
        tdat = (datetime.datetime.now() + datetime.timedelta(days=2))
        tdaat = (datetime.datetime.now() + datetime.timedelta(days=3))
        #tdaat = datetime.datetime(2017, 8, 8)
     
        if(event['start'].get('date')):
            #print("all-day")
            start = datetime.datetime.strptime(event['start'].get('date'), "%Y-%m-%d")
            end = datetime.datetime.strptime(event['end'].get('date'), "%Y-%m-%d")
            
            #print(start.date(), tdaat.date())
            
            if(start.date() == today.date()):
                self.todaylist.append(event['summary'])    
            if(start.date() == tomorrow.date()):
                self.tomorrowlist.append(event['summary'])
            if(start.date() == tdat.date()):
                self.tdatlist.append(event['summary'])
            if(start.date() == tdaat.date()):
                self.tdaatlist.append(event['summary'])
        else:
            #print("not all-day")
            start = event['start'].get('dateTime').split("+")
            start = datetime.datetime.strptime(start[0], "%Y-%m-%dT%H:%M:%S")
            end = event['end'].get('dateTime').split("+")
            end = datetime.datetime.strptime(end[0], "%Y-%m-%dT%H:%M:%S")
            
            if((end-start) > datetime.timedelta(days=1)):
                if(end.date() == today.date()):
                    self.todaylist.append("Bis "+end.time().strftime("%H:%M")+" "+event['summary'])    
                if(end.date() == tomorrow.date()):
                    self.tomorrowlist.append("Bis "+end.time().strftime("%H:%M")+" "+event['summary'])
                if(end.date() == tdat.date()):
                    self.tdatlist.append("Bis "+end.time().strftime("%H:%M")+" "+event['summary'])
                if(end.date() == tdaat.date()):
                    self.tdaatlist.append("Bis "+end.time().strftime("%H:%M")+" "+event['summary'])
                    
                if( (start.date() < today.date()) and (end.date() > today.date())):
                    self.todaylist.append(event['summary'])    
                if((start.date() < tomorrow.date()) and (end.date() > tomorrow.date())):
                    self.tomorrowlist.append(event['summary'])
                if((start.date() < tdat.date()) and (end.date() > tdat.date())):
                    self.tdatlist.append(event['summary'])
                if((start.date() < tdaat.date()) and (end.date() > tdaat.date())):
                    self.tdaatlist.append(event['summary'])
            
            
            if(start.date() == today.date()):
                self.todaylist.append(start.time().strftime("%H:%M")+" "+event['summary'])    
            if(start.date() == tomorrow.date()):
                self.tomorrowlist.append(start.time().strftime("%H:%M")+" "+event['summary'])
            if(start.date() == tdat.date()):
                self.tdatlist.append(start.time().strftime("%H:%M")+" "+event['summary'])
            if(start.date() == tdaat.date()):
                self.tdaatlist.append(start.time().strftime("%H:%M")+" "+event['summary'])
        
    def getEvents(self):
            credentials = self.get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http, cache_discovery=False)  
            
            self.todaylist = []
            self.tomorrowlist = []
            self.tdatlist = []
            self.tdaatlist = []
            
            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
            #now = (datetime.datetime.utcnow() + datetime.timedelta(days=5)).isoformat() + 'Z'
            nowplus3d = (datetime.datetime.utcnow() + datetime.timedelta(days=20)).isoformat() + 'Z'
            
            # Decher Kalender
            eventsResult = service.events().list(
                calendarId='6iqrnak2pji4jbl15q2vkrshbo@group.calendar.google.com', timeMin=now, timeMax=nowplus3d, maxResults=10, singleEvents=True, orderBy='startTime').execute()  #, singleEvents=True, orderBy='startTime'
            events = eventsResult.get('items', [])
            
            if not events:
                print('No upcoming events found.')
            for event in events:
                #print(event)
                self.eventlist(event)
                
            # Feiertage
            eventsResult = service.events().list(
                calendarId='de.german#holiday@group.v.calendar.google.com', timeMin=now, timeMax=nowplus3d, maxResults=10, singleEvents=True, orderBy='startTime').execute()  #, singleEvents=True, orderBy='startTime'
            events = eventsResult.get('items', [])
        
            if not events:
                print('No upcoming events found.')
            for event in events:
                #print(event)   
                self.eventlist(event)     
        
