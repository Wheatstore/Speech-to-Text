from datetime import datetime
from email.mime import audio
from fileinput import filename
from multiprocessing.connection import Client
from operator import truediv
from sqlite3 import paramstyle
from winsound import PlaySound
import pyaudio
import speech_recognition as sr
import os
from gtts import gTTS
import playsound
import requests
import pyttsx3
from bs4 import BeautifulSoup as bs4
from html.parser import HTMLParser
import lxml
import datetime
import wikipediaapi
import wolframalpha

weather_data = []
song_data = []
engine = pyttsx3.init()

def saySomething(text):
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()

def getAudio():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said  

def check_song(song):
    for i in song_data:
        if song == i:
            return True
while True:
    text = getAudio()

    if "dummy" and "weather" in text:
        count = 0
        html_content = requests.get("https://www.yr.no/en/forecast/daily-table/2-1835848/Republic%20of%20Korea/Seoul/Seoul").text
        soup = bs4(html_content, "lxml")
        climate = soup.find(class_="temperature temperature--cold")
        for i in climate:
            count += 1
            temp = i.text
            weather_data.append(temp)
            if(count == 2):
                print(weather_data[1])
                saySomething("The weather is currently" + "negative" + weather_data[1] + "in Seoul South Korea")
            else:
                pass
    
    if "dummy" and "date" in text:
        html_content = requests.get("https://www.calendardate.com/todays.htm").text
        soup = bs4(html_content, "lxml")
        date = soup.find(id="ttop")
        for i in date:
            print(i.text)
            time = i.text
        saySomething(time)

    if "get info" in text:
        app_id = "548PP6-JJJ688HL4X"
        app_name = "query"
        question = text[8:]
        client = wolframalpha.Client(app_id=app_id)
        res = client.query(question)
        saySomething(next(res.results).text)
    
    
    if "stocks" in text:
        KEY = "CQC031KZI4TJXVI0"
        stock_ticker = text[7:]
        if(stock_ticker == "Apple"):
            real_stock_ticker = "AAPL"
            res = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={real_stock_ticker}&apikey={KEY}').text      
            print(res) 
     
    
    
    
    if "stop" == text:
        saySomething("Yes sir the program is shutting down")
        break