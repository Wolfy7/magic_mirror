# coding: utf8

'''
Created on 23.04.2017

@author: Wolfy7
'''

from tkinter import *
import datetime
import modules.forecastio as FC
import modules.tankerkoenig as FK
import modules.googlecalendar as GC
import modules.rss
import logging
import locale
from modules.rss import getHeadline
import os


MONTHS = ('Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember')
DAYS = ('Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag')

class APP:
    def __init__(self, master):
        self.master = master
        
        self.mainFrame = Frame(master, bg="black")
        self.mainFrame.pack(fill=BOTH, expand=True)
        
        Grid.columnconfigure(self.mainFrame, 0, weight=1)
        Grid.columnconfigure(self.mainFrame, 1, weight=0)
        Grid.rowconfigure(self.mainFrame, 0, weight=0)
        Grid.rowconfigure(self.mainFrame, 1, weight=0)
        Grid.rowconfigure(self.mainFrame, 2, weight=4)
        Grid.rowconfigure(self.mainFrame, 3, weight=1)
        
        self.create_date_time()
        self.create_weather()
        self.create_headlines()
        self.create_fuel_prices()
        self.create_calendar()

        #self.testLabel = Label(self.mainFrame, text="Test Text", bg="black", fg="white",font=("Helvectiva",32, 'bold'))
        #self.testLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    def create_headlines(self):
        self.newsFrame = Frame(self.mainFrame, bg="black")
        self.newsFrame.grid(row=3, column=0,columnspan=2,sticky=S, pady=10, padx=10)
        
        self.newsText = Text(self.newsFrame)
        self.newsText.pack(side=BOTTOM) 
        
        def update_headlines():
            headline = getHeadline()
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S") + " Update Headlines, Headline =" + headline)
            h = int(len(headline)/42)+1
            self.newsText.tag_configure('tag-center', justify='center')
            self.newsText.config(
                bg='black',
                fg='white',
                font=("Helvetica", 26, "bold"),  #system
                borderwidth=0,
                wrap = WORD,
                height=h,
                highlightcolor="black",
                highlightbackground= "black",
                state=NORMAL
                )
            self.newsText.delete(1.0, END)
            self.newsText.insert(INSERT, headline, 'tag-center')
            self.newsText.config(state=DISABLED)
            
            self.newsFrame.after(60000, update_headlines) 
        update_headlines()
        
    def create_date_time(self):
        self.timeFrame = Frame(self.mainFrame, bg="black")
        self.timeFrame.grid(row=0, column=1,sticky=E+N, padx=5, pady=5)
        
        self.dateLabel = Label(self.timeFrame)
        #self.dateLabel.pack()
        self.dateLabel.grid(row=0, column=0,sticky=E+N)
        self.timeLabel = Label(self.timeFrame)
        #self.timeLabel.pack(side=RIGHT)
        self.timeLabel.grid(row=1, column=0,sticky=E+N)
        
        def upadte_date_time():
            self.daynumber, self.monthnumber, self.kw, self.day, self.year, self.time  = datetime.datetime.now().strftime("%w,%m,%U,%d,%Y,%H:%M:%S").split(",")
            self.daynumber = int(self.daynumber)
            self.monthnumber = int(self.monthnumber)
            self.date = "KW "+self.kw+", "+DAYS[self.daynumber]+"\n"+self.day+" "+MONTHS[self.monthnumber-1]+" "+self.year

            self.dateLabel.config(
                text=self.date,
                font=("Helvetica", 26, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            ) 
            
            self.timeLabel.config(
                text=self.time,
                font=("Helvetica", 28, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )
            self.timeFrame.after(1000, upadte_date_time) 
        upadte_date_time()
    
    def create_calendar(self):
        self.calendarFrame = Frame(self.mainFrame, bg="black")
        self.calendarFrame.grid(row=1, column=1,sticky=E+N, padx=5, pady=5)
        
        self.today = Label(self.calendarFrame)
        self.today.grid(row=0, column=0,sticky=E+N)
        self.todayText = Text(self.calendarFrame)
        self.todayText.grid(row=1, column=0,sticky=E+N)
        
        self.tomorrow = Label(self.calendarFrame)
        self.tomorrow.grid(row=2, column=0,sticky=E+N)
        self.tomorrowText = Text(self.calendarFrame)
        self.tomorrowText.grid(row=3, column=0,sticky=E+N)
        
        self.tdat = Label(self.calendarFrame)
        self.tdat.grid(row=4, column=0,sticky=E+N)
        self.tdatText = Text(self.calendarFrame)
        self.tdatText.grid(row=5, column=0,sticky=E+N)
        
        self.tdaat = Label(self.calendarFrame)
        self.tdaat.grid(row=6, column=0,sticky=E+N)
        self.tdaatText = Text(self.calendarFrame)
        self.tdaatText.grid(row=7, column=0,sticky=E+N)

        def upadte_calendar():
            gcalendar.getEvents()
            #print(gcalendar.todaylist)
            #print(gcalendar.tomorrowlist)
            #print(gcalendar.tdatlist)
            #print(gcalendar.tdaatlist)
            textwidth = 30
            
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S")+" Update Google Calendar")        
            
            self.today.config(
                text= "Heute", #+ datetime.datetime.now().strftime("%a, %d.%m")
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            ) 
            
            text = ""
            if not gcalendar.todaylist:
               text = "Keine Termine"
            for event in gcalendar.todaylist:
                if len(event) >= textwidth:
                    event= event[:textwidth]+"..."                 
                text += event+"\n"            
            
            self.todayText.tag_configure('tag-right', justify='right')
            self.todayText.config(
                bg='black',
                fg='white',
                font=("Helvetica", 14, "bold"),  #system
                borderwidth=0,
                wrap = WORD,         
                highlightcolor="black",
                highlightbackground= "black",
                width = textwidth,
                height=len(gcalendar.todaylist)
                )
            self.todayText.delete(1.0, END)
            self.todayText.insert(INSERT, text, 'tag-right')
            
            
            self.tomorrow.config(
                text= "Morgen, " + (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%a, %d.%m"),
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )
            
            text = ""
            if not gcalendar.tomorrowlist:
               text = "Keine Termine"
            for event in gcalendar.tomorrowlist:
                if len(event) >= textwidth:
                    event= event[:textwidth]+"..."                 
                text += event+"\n"            
            
            self.tomorrowText.tag_configure('tag-right', justify='right')
            self.tomorrowText.config(
                bg='black',
                fg='white',
                font=("Helvetica", 14, "bold"),  #system
                borderwidth=0,
                wrap = WORD,
                highlightcolor="black",
                highlightbackground= "black",                
                width = textwidth,
                height=len(gcalendar.tomorrowlist)
                )
            self.tomorrowText.delete(1.0, END)
            self.tomorrowText.insert(INSERT, text, 'tag-right')
            
            self.tdat.config(
                text= (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%a, %d.%m"),
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            ) 
            
            text = ""
            if not gcalendar.tdatlist:
               text = "Keine Termine"            
            for event in gcalendar.tdatlist:
                if len(event) >= textwidth:
                    event= event[:textwidth]+"..." 
                text += event+"\n"            
            
            self.tdatText.tag_configure('tag-right', justify='right')
            self.tdatText.config(
                bg='black',
                fg='white',
                font=("Helvetica", 14, "bold"),  #system
                borderwidth=0,
                wrap = WORD,
                highlightcolor="black",
                highlightbackground= "black",                
                width = textwidth,
                height=len(gcalendar.tdatlist)
                )
            self.tdatText.delete(1.0, END)
            self.tdatText.insert(INSERT, text, 'tag-right')   
            
            self.tdaat.config(
                text= (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%a, %d.%m"),
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )      
            
            text = ""
            if not gcalendar.tdaatlist:
               text = "Keine Termine"  
            for event in gcalendar.tdaatlist:
                if len(event) >= textwidth:
                    event= event[:textwidth]+"..."                
                text += event+"\n"            
            
            self.tdaatText.tag_configure('tag-right', justify='right')
            self.tdaatText.config(
                bg='black',
                fg='white',
                font=("Helvetica", 14, "bold"),  #system
                borderwidth=0,
                wrap = WORD,
                highlightcolor="black",
                highlightbackground= "black",                
                width = textwidth,
                height=len(gcalendar.tdaatlist)
                )
            self.tdaatText.delete(1.0, END)
            self.tdaatText.insert(INSERT, text, 'tag-right')

            self.calendarFrame.after(300000, upadte_calendar) 
        upadte_calendar() 
        
    def create_fuel_prices(self):
        self.fuelFrame = Frame(self.mainFrame, bg="black")
        self.fuelFrame.grid(row=2, column=1,sticky=E+N, padx=5, pady=5)
        
        self.dieselLabel = Label(self.fuelFrame)
        self.dieselLabel.grid(row=0, column=0,sticky=E+N)
        self.fuelLabel = Label(self.fuelFrame)
        self.fuelLabel.grid(row=2, column=0,sticky=E+N)
        self.fuele10Label = Label(self.fuelFrame)
        self.fuele10Label.grid(row=1, column=0,sticky=E+N)
        
        def upadte_fuel_prices():
            self.petrolPrices = fuelking.getPetrolPrices()
            #print(datetime.datetime.now().strftime("%H:%M:%S")+" "+str(forecast.counter))
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S")+" Update Fuel Prices, Prices = "+str(self.petrolPrices)) 
            
            self.dieselLabel.config(
                text= "Diesel " + str(self.petrolPrices['diesel']),
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            ) 
            
            self.fuelLabel.config(
                text= "Super " + str(self.petrolPrices['e5']),
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )
            
            self.fuele10Label.config(
                text= "Super E10 " + str(self.petrolPrices['e10']),
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )        

            self.fuelFrame.after(300000, upadte_fuel_prices) 
        upadte_fuel_prices()   
    
    def create_weather(self):
        self.weatherFrame = Frame(self.mainFrame, bg="black")
        self.weatherFrame.grid(row=0, column=0, sticky=W+N, padx=5, pady=5)
        self.weekforecastFrame = Frame(self.mainFrame, bg="black")
        self.weekforecastFrame.grid(row=1, column=0, sticky=W+N, padx=5, pady=5)
        
        self.summaryLabel = Label(self.weatherFrame)
        self.summaryLabel.grid(row=1, column=1, columnspan=6)
        self.temperatureLabel = Label(self.weatherFrame)
        self.temperatureLabel.grid(row=0, column=1, columnspan=6)
        self.imageLabel = Label(self.weatherFrame)
        self.imageLabel.grid(row=0, column=0, rowspan=3)
        
        self.temperatureMax = Label(self.weatherFrame)
        self.temperatureMax.grid(row=2, column=1)
        self.temperatureMin = Label(self.weatherFrame)
        self.temperatureMin.grid(row=2, column=2)
        
        self.umbrellaLabel = Label(self.weatherFrame)
        self.umbrellaLabel.grid(row=2, column=3)
        self.umbrella = PhotoImage(file='/home/pi/magic-mirror/weather_icons/umbrella-32.png')
        self.umbrellaLabel.config(
            image=self.umbrella,
             bg='black',
        ) 
        self.precipProbabilityLabel = Label(self.weatherFrame)
        self.precipProbabilityLabel.grid(row=2, column=4)
        
        self.cloudyLabel = Label(self.weatherFrame)
        self.cloudyLabel.grid(row=2, column=5)
        self.cloudy = PhotoImage(file='/home/pi/magic-mirror/weather_icons/clouds-32.png')
        self.cloudyLabel.config(
            image=self.cloudy,
             bg='black',
        ) 
        self.cloudCoverLabel = Label(self.weatherFrame)
        self.cloudCoverLabel.grid(row=2, column=6)
        
        #self.weekforecastLabel = Label(self.weatherFrame)
        #self.weekforecastLabel.grid(row=3, column=0, columnspan=16)  
        self.weekforecastText = Text(self.weekforecastFrame)
        self.weekforecastText.grid(row=3, column=0, columnspan=7)  
        
        self.weekLabels = []
        for i in range(7):
            dic = {"time":1, "summary":2, "icon":0, "temperatureMin":4, "temperatureMax":3, "precipProbability":6, "cloudCover":8, "precipIcon":5, "cloudIcon":7}
            for key in dic:
                if key == "summary":
                    tmp = Text(self.weekforecastFrame)
                else:
                    tmp = Label(self.weekforecastFrame)
                #tmpLabel.grid(row=5+i, column=0+dic[key])
                dic[key] = tmp 
            self.weekLabels.append(dic)  

        def update_weather():
            self.forecast = forecast.getForecast()
            #print(datetime.datetime.now().strftime("%H:%M:%S")+" "+str(forecast.counter))
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S")+" Update Weather, Forecast = "+ str(self.forecast))   
             
            r=4           
            for i, days in enumerate(self.forecast['daily']['data']):
                if i == 0:                   
                    self.temperatureMax.config(text=str(days['temperatureMax']) +"°",
                                                            font=("Helvetica", 16, "bold"),  #system
                                                            bg='black',
                                                            fg='white',
                                                            justify='right')
                    
                    self.temperatureMin.config(text=str(days['temperatureMin']) +"°",
                                                            font=("Helvetica", 16, "bold"),  #system
                                                            bg='black',
                                                            fg='white',
                                                            justify='right')
                    continue
                if i == 4:
                    break

                tmpImage = PhotoImage(file=forecast.getWatherImage(days['icon'], '32'))
                
                self.weekLabels[i-1].get('time').config(text=datetime.date.fromtimestamp(days['time']).strftime("%a, %d.%m"),
                                                        font=("Helvetica", 16, "bold"),  #system
                                                        bg='black',
                                                        fg='white',
                                                        justify='left')
                self.weekLabels[i-1].get('time').grid(row=r+i, column=0)
                
                r += 1                
                
                self.weekLabels[i-1].get('icon').config(
                    image=tmpImage,
                    bg='black',
                )
                self.weekLabels[i-1].get('icon').image = tmpImage
                self.weekLabels[i-1].get('icon').grid(row=r+i, column=0)   
            
                self.weekLabels[i-1].get('temperatureMax').config(text=str(days['temperatureMax']) +"°",
                                                        font=("Helvetica", 14, "bold"),  #system
                                                        bg='black',
                                                        fg='white',
                                                        justify='right')
                self.weekLabels[i-1].get('temperatureMax').grid(row=r+i, column=1)
                self.weekLabels[i-1].get('temperatureMin').config(text=str(days['temperatureMin']) + "°",
                                                        font=("Helvetica", 14, "bold"),  #system
                                                        bg='black',
                                                        fg='white',
                                                        justify='right')
                self.weekLabels[i-1].get('temperatureMin').grid(row=r+i, column=2)
                
                
                self.weekLabels[i-1].get('precipProbability').config(text=str(int(days['precipProbability'] * 100)) + "%",
                                                        font=("Helvetica", 14, "bold"),  #system
                                                        bg='black',
                                                        fg='white',
                                                        justify='right')
                self.weekLabels[i-1].get('precipProbability').grid(row=r+i, column=4)
                
                self.weekLabels[i-1].get('cloudCover').config(text=str(int(days['cloudCover'] * 100)) + "%",
                                                        font=("Helvetica", 14, "bold"),  #system
                                                        bg='black',
                                                        fg='white',
                                                        justify='right')
                self.weekLabels[i-1].get('cloudCover').grid(row=r+i, column=6)
                self.weekLabels[i-1].get('cloudIcon').config(
                    image=self.cloudy,
                    bg='black',
                ) 
                self.weekLabels[i-1].get('cloudIcon').grid(row=r+i, column=5)
                self.weekLabels[i-1].get('precipIcon').config(
                    image=self.umbrella,
                    bg='black',
                )
                self.weekLabels[i-1].get('precipIcon').grid(row=r+i, column=3)

                r += 1  

                #print(len(days['summary']))
                self.weekLabels[i-1].get('summary').tag_configure('tag-center', justify='center')
                self.weekLabels[i-1].get('summary').config(
                    bg='black',
                    fg='white',
                    font=("Helvetica", 14, "bold"),  #system
                    borderwidth=0,
                    wrap = WORD,
                    width = 42,
                    height=int(len(days['summary'])/42)+1,
                    highlightcolor="black",
                    highlightbackground= "black"
                    )
                self.weekLabels[i-1].get('summary').delete(1.0, END)
                self.weekLabels[i-1].get('summary').insert(INSERT, days['summary'], 'tag-center')
                self.weekLabels[i-1].get('summary').grid(row=r+i, column=0, columnspan=7)                
 
            
            self.image = PhotoImage(file=forecast.getWatherImage(self.forecast['currently']['icon'], '128'))
            
            """
            self.weekforecastLabel.config(
                text=self.forecast['daily']['summary'],
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )   
            """
            #print(len(self.forecast['daily']['summary']))
            #print(int(len(self.forecast['daily']['summary'])/30)+1)
            self.weekforecastText.tag_configure('tag-center', justify='center')
            self.weekforecastText.config(
                bg='black',
                fg='white',
                font=("Helvetica", 16, "bold"),  #system
                borderwidth=0,
                wrap = WORD,
                width = 30,
                height=int(len(self.forecast['daily']['summary'])/30)+1,
                highlightcolor="black",
                highlightbackground= "black"
                )
            self.weekforecastText.delete(1.0, END)
            self.weekforecastText.insert(INSERT, self.forecast['daily']['summary'], 'tag-center')
            
            
            self.summaryLabel.config(
                text=self.forecast['currently']['summary'],
                font=("Helvetica", 24, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )  
            self.temperatureLabel.config(
                text=str(self.forecast['currently']['temperature'])+" °",
                font=("Helvetica", 28, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )      
            self.imageLabel.config(
                image=self.image,
                 bg='black',
            ) 
            self.precipProbabilityLabel.config(
                text= str(int(self.forecast['currently']['precipProbability'] * 100)) + "%",
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            ) 
            self.cloudCoverLabel.config(
                text= str(int(self.forecast['currently']['cloudCover'] * 100)) + "%",
                font=("Helvetica", 16, "bold"),  #system
                bg='black',
                fg='white',
                justify='right'
            )                
            self.timeFrame.after(300000, update_weather) 
        update_weather()            

def initLogging():
    logging.basicConfig(filename="/home/pi/magic-mirror/log/mm2.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def OneSec():
    #logging.debug("OneSec:" + datetime.datetime.now().strftime("%H:%M:%S"))
    app.mainFrame.after(1000, OneSec)
    

if __name__ == "__main__":

    #os.system('sh monitor_off.sh')
    os.system('sh monitor_on.sh')
    
    initLogging()
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    
    logging.info("Start Magic Mirror")
    forecast = FC.FORECASTIO()
    fuelking = FK.TANKERKOENIG()
    gcalendar = GC.GOOGLECALENDAR()
    
    root = Tk()
        
    root.attributes('-fullscreen', True)
    root.config(cursor='none')
    #root.geometry('1024x1600')
    app = APP(root)          
    
    #app.mainFrame.after(1000, OneSec)
    string = "Hallo"
    #os.system('espeak -vde "{}"'.format(string))  
    root.mainloop()
    
    logging.info("Stop Magic Mirror")
