import json
import math
import random
import hashlib

class Memorize():

    def setup(self):
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
        # create an ID for use in the log files using SHA1 hash.
        # This is done so that questions which contain hints to secure
        # information (passwords) can be stored in a less secure location

        id = hashlib.sha1(bytes(question, 'utf-8')).hexdigest()


        self.log.setdefault(id, [0, 0, 0])

        #the list format corresponds to [attempts, fails, fraction correct]

        resp = input(question+" ")
        if resp != self.questions[question]:
            print('Incorrect.')
            print('The correct answer was: "'+self.questions[question]+'"')
            self.log[id][1]+=1

        self.log[id][0]+=1
        self.log[id][2]=1-self.log[id][1]/self.log[id][0]
        #question tags? (eg. attempts, lower ok, timed, etc)
        #block accidental blank responses?
        #allow mark misspelling as a tag
        #create log
        #recommend prio?



    def __init__(self):
        # LOAD CONFIG

        c = open("config.json")
        self.config=json.load(c)
        c.close()

        # LOAD QUESTIONS
        #check for a list of locations
        q = open(self.config['question_location'])
        self.questions = json.load(q)

        # LOAD LOG

        l = open(self.config['log_location'])
        self.log = json.load(l)
        l.close()

        # CONFIG CHECKS
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
        if self.config['init']:
            resp = input(
                    """Since this is your first time using Memorize, I recommend you go through the setup. Do you want to go through the setup/tutorial? Y/N \n""")
            if resp.lower() == 'y':
                self.setup()
            else:
                self.config['init']=0

        if self.config['api_config']:
            #do whatever here
            pass
        if self.config['questions'] < 1:
            print('You have set less than one question to be asked. Check your config.json')

        if self.config['ask_all'] and not self.config['init']:
            for question in self.questions:
                self.ask(question)

        #initial question configuration?


    def exit(self):
        #review all answers (especially incorrect?)
        #dump statistics in logs
        print(self.log)
        l = open(self.config["log_location"], "w")
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
