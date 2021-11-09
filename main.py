import speech_recognition as sr
from bs4 import BeautifulSoup as soup
from time import strftime
import webbrowser
import re

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio,language="pl-PL").lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def assistant(command):
    "if statements for executing commands"
#open subreddit Reddit
    if 'otwórz reddit' in command:
        reg_ex = re.search('otwórz reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
    if 'poszukaj w google' in command:
        reg_ex = re.search('poszukaj w google (.*)', command)
        url = 'https://www.google.com/'
        if reg_ex:
            query = reg_ex.group(1)
            url = url + "/search?q={" + query + "}"
        webbrowser.open(url)

while True:
    assistant(myCommand())