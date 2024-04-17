import json
import math
import random
import hashlib
import os
import time
#import getpass
#import pygame #potentially use

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Memorize():

    def tutorial(self):
        self.config['init']=0
        print("""Memorize is a basic framework that you can build on to memorize anything you want.
I designed Memorize with passwords in mind, so a few of its (admittedly already sparse) features have that in mind.
The format of Memorize will in general look like this: \n""")

        for q, a in [("Example Password A. Hint: it's 12345", "12345"), ("Example Password B. Hint: it's 67890", "67890")]:
            resp=""
            tries = 0
            while resp != a:
                if tries <1:
                    pass
                elif tries < 3:
                    print('Incorrect. Try typing in the hint')
                elif tries < 10:
                    print('Ok mate, what are you doing. Just type in the hint...')
                else:
                    print("You're hopeless")
                    quit()
                resp = input(q+"\n")
                tries+=1

        print("Simple enough, right? Now let's try another example: \n")
        resp = input("Example Password C. \n")
        if resp != "mlkmcdslkm8u345mnsh(Y*&Hujb3409ukjn(*&TY*Gb h34oijosdu9y9y))":
            print('Incorrect. The correct answer was "mlkmcdslkm8u345mnsh(Y*&Hujb3409ukjn(*&TY*Gb h34oijosdu9y9y))"')
            print('A typical question will tell you the correct answer after you get it wrong once. \nThis can be customized on a question-by-question basis, and you should use this when inputting more questions.')
        else:
            print("Wow. Wow. WOW. Either you're INSANELY lucky, or you cheated.")
            test = input("I'll give you one chance. Did you cheat?")
            if test.lower() in ['yes', 'yup', 'yep']:
                print('Haha, I like you. Well, anyway, the intended purpose of this question \nwas to show you that a typical question will tell you the correct answer after you get it wrong once. \nThis can be customized on a question-by-question basis, and you should use this when inputting more questions.')
            elif test.lower() not in ['no', "i'm just really really lucky, i guess"]:
                print('sus')
                quit()
        print("That's it for the tutorial. Play around with some of the settings in config.json, and input your questions using the question script (questions.py)")
        self.exit()

    def ask(self, question):
        clear()
        # create an ID for use in the log files using SHA1 hash.
        # This is done so that questions which contain hints to secure
        # information (passwords) can be stored in a less secure location

        id = hashlib.sha1(bytes(question, 'utf-8')).hexdigest()


        self.log.setdefault(id, [0, 0, 0])

        #the list format corresponds to [attempts, fails, fraction correct]

        #tag handling

        ans=self.questions[question]["answers"]

        for a in range(self.questions[question].get("attempts", 1)):
            resp = input(question+"\n")
            if resp not in ans:
                print('Incorrect.')
                time.sleep(0.5)
                clear()
                self.log[id][1]+=1
                self.review.add(question)

            else:
                print('Correct')
                self.log[id][0]+=1
                self.log[id][2]=1-self.log[id][1]/self.log[id][0]
                break

            self.log[id][0]+=1
            self.log[id][2]=1-self.log[id][1]/self.log[id][0]

        print('Answer(s): '+str(ans))
        time.sleep(1)
        if question in self.review:
            cont = input('Press Any Key to Continue:')
        #question tags? (eg. attempts, lower ok, timed, etc)
        #block accidental blank responses?
        #allow mark misspelling as a tag
        #create log
        #recommend prio?

    def __init__(self):
        clear()
        # LOAD CONFIG

        c = open("config.json")
        self.config=json.load(c)
        c.close()

        if self.config["enable_logo"]:
            print("""
                ███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗███████╗███████╗
                ████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗██║╚══███╔╝██╔════╝
                ██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝██║  ███╔╝ █████╗
                ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗██║ ███╔╝  ██╔══╝
                ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║██║███████╗███████╗
                ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝.py
                the humble memorization script
            """)

        # LOAD QUESTIONS
        #check for a list of locations
        self.questions={}
        for loc in self.config['question_location']:
            try:
                q = open(loc, 'r')
                self.questions |= json.load(q)
                print('/loaded: '+loc)
            except:
                print
                continue
        # LOAD LOG

        try:
            l = open('log.json')
            self.log = json.load(l)
            l.close()
            print('/loaded log')
        except:
            print('/log loading failed')
            self.log={}

        self.review=set()

        # CONFIG CHECKS
        time.sleep(2.5)
        if self.config['init']:
            resp = input(
                    """Since this is your first time using Memorize, I recommend you go through the tutorial. Do you want to go through the tutorial? Y/N \n""")
            if resp.lower() == 'y':
                self.tutorial()
            else:
                self.config['init']=0

        if self.config['api_config']:
            #do whatever here
            pass
        if self.config['questions'] < 1:
            print('You have set less than one question to be asked. Check your config.json')

        if self.config['ask_all'] and not self.config['init']:
            print("""
                 █ █ █   ▀█▀ ▀█▀ █▄█ █▀█ ▀█▀ █▀▀   █▀▄ █▀█ █ █ █▀█ █▀▄
                 █ █ █    █   █  █ █ █▀█  █  █▀▀   █▀▄ █ █ █ █ █ █ █ █
                 ▀▀▀ ▀▀▀  ▀  ▀▀▀ ▀ ▀ ▀ ▀  ▀  ▀▀▀   ▀ ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀
                """) #NEEDS WORK
            time.sleep(1.5)
            for question in self.questions:
                self.ask(question)

            self.exit()
        #initial question configuration?

    def refresh(self):
        clear()
        review_list = list(self.review)
        self.review=set()
        for question in review_list:
            self.ask(question)
        if self.review != set():
            self.refresh()

    def exit(self):
        clear()
        if self.review != set():
            print('Review Time!') #needs work
            time.sleep(1)
            self.refresh()
        clear()
        print("""
            ███╗   ███╗███████╗███╗   ███╗ ██████╗ ██████╗ ██╗███████╗███████╗
            ████╗ ████║██╔════╝████╗ ████║██╔═══██╗██╔══██╗██║╚══███╔╝██╔════╝
            ██╔████╔██║█████╗  ██╔████╔██║██║   ██║██████╔╝██║  ███╔╝ █████╗
            ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗██║ ███╔╝  ██╔══╝
            ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║██║███████╗███████╗
            ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝.py
            See you next time!
        """)
        #review all answers (especially incorrect?)
        #dump statistics in logs
        #print(self.log)
        l = open('log.json', "w")
        json.dump(self.log, l, indent=4)
        l.close()
        #modify config settings if necessary
        f = open('config.json', 'r')
        old = json.load(f)
        if self.config != old:
            print("CONFIG CHANGED:")
            for key in self.config:
                if self.config[key] != old[key]:
                    print(key+" : "+str(old[key])+" -> "+str(self.config[key]))
            if input('Would you like to save config changes? Y/N \n').lower() == 'y':
                c = open('config.json', 'w')
                json.dump(self.config, c, indent=4)
                c.close()
        quit()


#Questions are formatted in a dictionary, with the question as the key, and the answer as the value (or an array)
#set?

mem = Memorize()
#tests
mem.exit()
#end test

# DECIDE WHICH QUESTIONS TO ASK

# RECORD ANSWERS / WEIGHT QUESTIONS
