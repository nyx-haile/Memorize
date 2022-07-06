import json
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#LOAD config
c=open('config.json')
config = json.load(c)
c.close()

t= open('tags.txt', 'r')
all_tags=t.read()
print("TAGS:")
print(all_tags)

def q_update(dict):
    while True:
        q = input('type the question\n')
        print(dict.get(q, ''))
        a = input("enter all of the answers, separated by '||', (e.g., 1||2||3||4)\n")
        ans = a.split('||')
        dict[q]={}
        dict[q]['answers']=ans
        tags_input = input("Type the tags. Separate tags by '||' and individual tags from values by ':' (e.g., attempts:3||case-sensitive:1) \n")
        if tags_input:
            tags=[i.split(':') for i in tags_input.split('||')]
            for tag in tags:
                dict[q][tag[0]]=tag[1]

        end = input('Done adding questions? Y/N\n')
        if end.lower()=='y':
            break

    return(dict)


while True:
    resp=input('Create a new questions file? Y/N \n')
    if resp.lower() == 'y':
        resp = input('Please give the path to the new questions file \n')
        if resp[-5:] != ".json":
            resp+=".json"
        n = open(resp, 'w')
        new={}
        q_update(new)
        json.dump(new, n, indent=4)
        n.close()
        if resp not in config['question_location']:
            config['question_location'].append(resp)
            c = open('config.json', 'w')
            json.dump(config, c, indent=4)
            c.close()

    else:
        print('Modifying existing file')
        print('Please note that currently, only adding more questions is supported.\nIf you would like to delete questions, please open the text file directly.')
        resp = input('Please give the path to the questions file \n')
        if resp[-5:] != ".json":
            resp+=".json"
        m = open(resp, 'r')
        mod = json.load(m)
        m.close()
        print(mod.keys())
        print([(key, mod[key]['answers']) for key in mod.keys()])
        q_update(mod)
        n=open(resp, 'w')
        json.dump(mod, n, indent=4)
        n.close()
        if resp not in config['question_location']:
            config['question_location'].append(resp)
            c = open('config.json', 'w')
            json.dump(config, c, indent=4)
            c.close()
    print('To quit, press Ctrl+C')
