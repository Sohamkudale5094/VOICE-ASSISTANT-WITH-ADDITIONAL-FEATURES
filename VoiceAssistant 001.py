from multiprocessing.pool import CLOSE
import speech_recognition as sr
import webbrowser as wb
import ecapture as ec
import wolframalpha
import VirtualMouse
import pywhatkit
import wikipedia
import requests
import datetime
import random
import pyttsx3
import os

# building object for Speech Recognizer
device= sr.Recognizer()
# building object for Transcriber
engine= pyttsx3.init()
# retrieving voices from system
device_voices= engine.getProperty('voices')
# select voice id 1 
engine.setProperty('voice',device_voices[1].id)

cond=True

#-----------function to take result in VOICE of device----------------
def talk(text):
    engine.say(text)
    engine.runAndWait()
 
#-----------function to start program by wishing acc to time----------------
def start():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12 :
        talk('Good Morning Sir')
        print('Good Morning Sir','\n')
    elif hour>12 and hour<18 :
        talk('Good Afternoon Sir')
        print('Good Afternoon Sir','\n')
    else:
        talk('Good Evening Sir')
        print('Good Evening Sir','\n')
    talk('I am Luci'+'How can I help you')

#-----------function to convert VOICE into TEXT----------------
def com_for_Luci():
    while True:
        with sr.Microphone() as source:
            print('Listening....')
            device= sr.Recognizer()
            device.pause_threshold=1
            voice= device.listen(source)
            try:
                    global command
                    with sr.Microphone() as source:
                        device= sr.Recognizer()
                        device.pause_threshold=1
                        voice= device.listen(source,timeout=None,phrase_time_limit=None)
                        command=device.recognize_google(voice)
                        command=command.lower()
                        command = command.replace("wake up","")
                        return command
            except:
                pass
            
#-----------working start on commands by user----------------
def running_Luci():
    global command
    command= com_for_Luci()
    print('USER_COMMAND : ' , command)

    #------To open cmd------
    if 'open command prompt' in command or 'open cmd' in command :
        os.system('start cmd')
        
    #------To play music from local storage------
    elif 'play music' in command :
        music_dir="D:\\project"
        songs=os.listdir(music_dir)
        rsong=random.choice(songs)
        os.startfile(os.path.join(music_dir,rsong))

    #------for recent day--------
    elif 'day' in command :
        day= datetime.datetime.today().strftime('%A')
        talk('Today is '+ day)
        print('Today is '+ day)

    #------for current time------
    elif 'time' in command :
        time= datetime.datetime.now().strftime('%H:%M %p')
        talk('Current Time is '+ time)
        print('Current Time is '+ time)
        
    #------for ip address of device------
    elif 'ip address' in command :
        ip=get('https://api.ipify.org').text
        talk('your IP address is' + ip)
        print('your IP address is' + ip)
    
    #------To play a video or song using youtube-----
    elif 'play' in command :
        play=command.replace('play','')
        talk('Playing'+ play)
        pywhatkit.playonyt(play)
    
    #------for searching wikipedia------
    elif 'search wikipedia of ' in command  or 'who is' in command or 'what is ' in command :
        search_wiki=command.replace('search wikipedia of','')
        talk('searching for '+search_wiki)
        info_wiki= wikipedia.summary(search_wiki,sentences=2)
        talk('according to wikipedia' + info_wiki)
    
    #------To open google browser------
    elif 'open google' in command or 'open browser' in command :
        talk('Ok Sir, what should I search')
        with sr.Microphone() as source:
                device= sr.Recognizer()
                device.pause_threshold=1
                voice= device.listen(source,timeout=10,phrase_time_limit=6)
                com_gle =device.recognize_google(voice)
                com_gle=com_gle.lower()
                com_gle = com_gle.replace("friday","")
        if 'just open browser' in com_gle :
            print('Opening Google Browser....')
            wb.open('https://www.google.co.in/')
        else:
            print('Opening Google Browser....')
            wb.open(f"{com_gle}")
    
    #------To open youtube------
    elif 'open youtube' in command or 'open yt' in command :
        talk('opening youtube....')
        wb.open('https://m.youtube.com')
    
    #------for search on youtube------
    elif 'search on youtube' in command or 'search on yt' in command :
        search_yt=command.replace('search on youtube','')
        talk('Searching youtube....')
        pywhatkit.playonyt(search_yt)
    
    #------talk with Luci-----------
    elif 'how are you' in command :
        talk('i am good sir.')
        talk('tell me , how i can help you ')
        
    elif 'who are you' in command or 'who creates you' in command or 'introduce yourself' in command :
        talk('hello sir, i am Luci. Created by group 20 . How i can help you sir')
        print('hello sir, i am Luci. Created by group 20 . How i can help you sir')

    #------To search any random query--------
    elif 'what is ' in command or 'who is' in command:
        client = wolframalpha.Client("PH4756-RH9LH625WH")
        res = client.command(command)
         
        try:
            print (next(res.results).text)
            talk (next(res.results).text)
        except StopIteration:
            print ("No results")
            
    #-------To calculate any maths-----------
    elif "calculate" in command:
             
            app_id = "PH4756-RH9LH625WH"
            client = wolframalpha.Client(app_id)
            indx = command.lower().split().index('calculate')
            command = command.split()[indx + 1:]
            res = client.command(' '.join(command))
            answer = next(res.results).text
            print("The answer is " + answer)
            talk("The answer is " + answer)

    #------for opening of camera----------
    elif "camera" in command or "take a photo" in command:
            ec.capture(0, "Voice Assistant Camera ", "img.jpg")
        
    #------for virtual mouse------------
    elif 'enable virtual mouse' in command :
        talk('the Virtual Mouse is enabled sir. ')
        VirtualMouse.VirtualMouse.initializeCam()
    elif 'disable virtual mouse' in command:
        talk('the Virtual Mouse is enabled sir. ')
        VirtualMouse.VirtualMouse.destroyWin()

    #------for flappy bird game--------
    elif "start game" in command :
        import FlappyBird
        talk("Starting Flappy Bird Game for you")
        FlappyBird.main()
        FlappyBird.StartScreen()
        FlappyBird.mainGame()
        
    #------for close the program------
    elif 'turn off' in command or 'switch off' in command :
        talk('Thank You so much for your precious time ')
        talk('See you soon')
        global cond 
        cond=False
    else:
        talk('Please repeat the given command again.')

start()                                    
while True :
    running_Luci()
    if not cond :
        break

#---@prtkkor007---
#---Thank You So Much---# 



