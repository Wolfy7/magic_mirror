'''
Created on 02.05.2017

@author: Wolfy7
'''

#  pip install feedparser

import feedparser
import logging
import random

WELT = "http://www.welt.de/?service=Rss"
GOOGLE = "https://news.google.com/news?cf=all&hl=de&pz=1&ned=de&output=rss"
TAGESSCHAU = "http://www.tagesschau.de/xml/rss2"
HESSENSCHAU = "http://hessenschau.de/index.rss"
FOCUS = "http://rss.focus.de/fol/XML/rss_folnews.xml"

URLS = (WELT,GOOGLE,TAGESSCHAU,HESSENSCHAU,FOCUS)

def getHeadline():
    URL = random.choice(URLS)
    #print(URL)
    d = feedparser.parse(URL)
    if d.bozo:
        #print(d.bozo_exception)
        logging.error("RSS: bozo exception =" + str(d.bozo_exception)) 
    #print(len(d.entries))
    #print (d['entries'][0]['title'])
    
    headline = d['entries'][0]['title']
    #if(len(str) > 60):
    #    str = str[:str.find(" ", 60)]+" ..."
    return headline


