import json
import math
import random
import hashlib

class Memorize():

    def setup(self):
        pass

    def ask(self, question):
        # create an ID for use in the log files using SHA1 hash.
        # This is done so that questions which contain hints to secure
        # information (passwords) can be stored in a less secure location

        id = hashlib.sha1(bytes(question, 'utf-8')).hexdigest()

        
        self.log.setdefault(id, [0, 0, 0])
        print(id)
        resp = input(question+" ")
        if resp != self.questions[question]:
            print('Incorrect.')
            print('The correct answer was: "'+self.questions[question]+'"')
            self.log[id][1]+=1

        self.log[id][0]+=1
        self.log[id][2]=1-self.log[id][1]/self.log[id][0]
        #question tags? (eg. attempts, lower ok, timed, etc)
        #block accidental blank responses?
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

        if self.config['init']:
            resp = input(
                    """Welcome To Memorize, the humble memorization script. Since this is your first time using Memorize, I recommend you go through the setup. Do you want to go through the setup? Y/N """)
            if resp.lower == 'y':
                self.setup()

        if self.config['api_config']:
            #do whatever here
            pass
        if self.config['questions'] < 1:
            print('You have set less than one question to be asked. Check your config.json')

        if self.config['ask_all']:
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



#Questions are formatted in a dictionary, with the question as the key, and the answer as the value (or an array)
#set?

mem = Memorize()
#tests
print(mem.questions)
mem.exit()
#end test

# DECIDE WHICH QUESTIONS TO ASK

# RECORD ANSWERS / WEIGHT QUESTIONS
