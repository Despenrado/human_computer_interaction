import speech_recognition as sr
from time import strftime
import webbrowser
import re
import json
import platform
import subprocess
import datetime




with open('dict.conf') as json_file:
    dictionary = json.load(json_file)
print(dictionary["google search"])

sys_prefix = dictionary["system"][platform.system().lower()]["sys_prefix"]
app_type = dictionary["system"][platform.system().lower()]["app_type"]

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        # Google API Client Library for Python
        command = r.recognize_google(audio,language="pl-PL").lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def assistant(command):
    if 'otwórz reddit' in command:
        reg_ex = re.search('otwórz reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:#open subreddit Reddit
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
    for com in dictionary["google search"]:
        if com in command:
            reg_ex = re.search(com+' (.*)', command)
            url = 'https://www.google.com/'
            if reg_ex:
                query = reg_ex.group(1)
                url = url + "/search?q={" + query + "}"
            webbrowser.open(url)
    for com in dictionary["launch"]:
        if com in command:
            reg_ex = re.search(com+' (.*)', command)
            if reg_ex:
                appname = reg_ex.group(1)
                try:
                    subprocess.Popen([sys_prefix + appname + app_type], stdout=subprocess.PIPE)
                except:
                    print(appname + " not found")
    for com in dictionary["open file"]:
        if com in command:
            reg_ex = re.search(com+' (.*)', command)
            if reg_ex:
                tail = reg_ex.group(1)
                for opt in dictionary["using"]:
                    if opt in tail:
                        reg_ex = re.search('(.*)'+opt+' (.*)', tail)
                        if reg_ex:
                            filename = reg_ex.group(1)
                            filename = filename.replace("slash ", "/")
                            print(filename)
                            appname = reg_ex.group(2)
                            print(appname)                
                            try:
                                print(sys_prefix + appname + app_type + " ./"+filename)
                                subprocess.Popen([sys_prefix + appname + app_type, "./" + filename], stdout=subprocess.PIPE)
                            except:
                                print(appname + " not found")
    for com in dictionary["time"]:
        if com in command:
            print("time is", datetime.datetime.now())

    
while True:
    assistant(myCommand())