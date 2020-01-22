import json
from datetime import datetime
import os.path
from os import path

data = {}

def unpickle():
    with open("grades.json","r") as file:
        data=json.load(file)

def picklesave():
    print("saved!")
    with open("grades.json",'w') as file:
        json.dump(data,file)
    
    
def spacing(words,space):
    return (words+" "*(space-len(words)))

def parse_input(commands):
    cmds = commands.split(",")
    no = len(cmds)
    cmds[0] = cmds[0][:2]

    if (cmds[0] == "ad"):
        if (no == 2):
            if (data[cmds[1]]):
                print("[Error] Duplicate class")
            else:
                data[cmds[1]]= {"cats":{},"grade":0}
        if (no == 3):
            try:
                assert("=" in cmds[2])
                assert(float(cmds[2].split("=")[1]) <= 100 and float(cmds[2].split("=")[1])> 0)
                assert((sum([cat["weight"]*100 for cat in data[cmds[1]]["cats"].values()]) + float(cmds[2].split("=")[1])) <= 100)
            except AssertionError:
                if ("=" not in cmds[2]):
                    print("[Error] Incorrect Syntax: Category must have a valid weight")
                else:
                    print("[Error] Invalid value: Please enter a valid weight")
            else:
                category = cmds[2].split("=")
                category[1] = float(category[1])/100
                data[cmds[1]]["cats"][category[0]] = {"weight":category[1],"items":[],"totalpts":0,"pts":0,"grade":0}
        if (no == 4 or no > 5):
            print("[Error] Not a valid number of commands!")
        if (no == 5):
            date = "-".join(str(datetime.now()).split()[0].split("-")[1:])
            assignment = (cmds[3],cmds[4],date)
            points = [float(num) for num in cmds[4].split("/")]
            data[cmds[1]]["cats"][cmds[2]]["items"].append(assignment)
            weight = data[cmds[1]]["cats"][cmds[2]]["weight"]
            
            data[cmds[1]]["cats"][cmds[2]]["totalpts"] += points[1]
            data[cmds[1]]["cats"][cmds[2]]["pts"] += points[0]
            data[cmds[1]]["cats"][cmds[2]]["grade"] = round(100*(data[cmds[1]]["cats"][cmds[2]]["pts"]/data[cmds[1]]["cats"][cmds[2]]["totalpts"]),1)
            
            add_sum = 0
            total_weights = 0
            old_grade = data[cmds[1]]["grade"] 
            for cats in data[cmds[1]]["cats"]:
                if len(data[cmds[1]]["cats"][cats]["items"]) > 0:
                    total_weights += data[cmds[1]]["cats"][cats]["weight"]
            for cats in data[cmds[1]]["cats"]:
                add_sum += data[cmds[1]]["cats"][cats]["grade"]*(data[cmds[1]]["cats"][cats]["weight"]/total_weights)
            data[cmds[1]]["grade"] = add_sum
            if (old_grade>add_sum):
                symbol = "-"
            else:
                symbol = "+"
            print("Grade Change  ",str(round(old_grade,2)),"->",round(data[cmds[1]]["grade"],2),": ",symbol,str(round(add_sum-old_grade,2)))    
            
    elif (cmds[0] == "di"):
        if (no == 1):
            display_classes()
        if (no == 2):
            try:
                test = data[cmds[1]]["cats"]
            except KeyError:
                print("[Error] Invalid: Class does not exist")
            else:
                print(spacing("Categories",15),spacing("Points",10),spacing("Percentage",11),spacing("Weight",7))
                print("********************************************************************")
                for cats in data[cmds[1]]["cats"]:
                    pts = "("+str(data[cmds[1]]["cats"][cats]["pts"])+"/"+str(data[cmds[1]]["cats"][cats]["totalpts"])+")"
                    print(spacing(cats,15),spacing(pts,10),spacing(str(data[cmds[1]]["cats"][cats]["grade"]),11), spacing(str(data[cmds[1]]["cats"][cats]["weight"]),7))
                print("Overall Percentage: ",data[cmds[1]]["grade"])
        if (no == 3):
            try:
                test = data[cmds[1]]["cats"]
            except KeyError:
                print("[Error] Invalid: Class does not exist")
            else:
                try:
                    test = data[cmds[1]]["cats"][cmds[2]]["items"]
                except KeyError:
                    print("[Error] Invalid: Category does not exist")
                else:
                    print(spacing("Name",15),spacing("Points",10),spacing("Percentage",13),spacing("Date",10))
                    print("********************************************************************")
                    for item in data[cmds[1]]["cats"][cmds[2]]["items"]:
                        points = [float(num) for num in item[1].split("/")]
                        percent = round(100*(points[0]/points[1]))
                        print(spacing(item[0],15),spacing(str(item[1]),10),spacing(str(percent)+"%",13),spacing(item[2],10))
                
    elif (cmds[0]=="cd"):
        global addlist
        if (cmds[-1]==".."):
            addlist.pop()
        elif(cmds[-1] == ",,"):
            addlist = []
        else:
            addlist.extend(cmds[1:])

    elif (cmds[0] == "re" or cmds[0] == "rm"):
        if (no == 2):
            popped = data.pop(cmds[1],None)
            if (popped):
                print("[Info]", cmds[1],"has been removed")
            else:
                print("[Warn] This class does not exist")
        if (no == 3):
            if (data[cmds[1]]["cats"].pop(cmds[2],None)):
                print("[Info]",cmds[2],"has been removed from",cmds[1])
            else:
                print("[Warn] This subject does not exist")

        if (no == 4):
            assignment = None
            try:
                for item in data[cmds[1]]["cats"][cmds[2]]["items"]:
                    if (item[0] == cmds[3]):
                        assignment = item
            except KeyError:
                print("[Error] Either this class or category does not exist")
            else:
                if (assignment != None):
                    print("[Info]",cmds[3],"has been removed from",cmds[2])
                    points = [float(num) for num in assignment[1].split("/")]
                    
                    data[cmds[1]]["cats"][cmds[2]]["totalpts"] -= points[1]
                    data[cmds[1]]["cats"][cmds[2]]["pts"] -= points[0]
                    data[cmds[1]]["cats"][cmds[2]]["grade"] = round(100*(data[cmds[1]]["cats"][cmds[2]]["pts"]/data[cmds[1]]["cats"][cmds[2]]["totalpts"]),1)
                    
                    data[cmds[1]]["cats"][cmds[2]]["items"].remove(assignment)

                    add_sum = 0
                    total_weights = 0
                    for cats in data[cmds[1]]["cats"]:
                        if len(data[cmds[1]]["cats"][cats]["items"])>0:
                            total_weights += data[cmds[1]]["cats"][cats]["weight"]
                    for cats in data[cmds[1]]["cats"]:
                        add_sum += data[cmds[1]]["cats"][cats]["grade"]*(data[cmds[1]]["cats"][cats]["weight"]/total_weights)
                    data[cmds[1]]["grade"] = add_sum
                else:
                    print("[Warn] This item does not exist")
            
                    
            
            
            
            

                    
def display_classes():
    print(spacing("classes",15),spacing("grade",5),)
    print("************************************")
    for clas in data:
        print(spacing(clas,15),spacing(str(round(data[clas]["grade"],1)),5))

def get_input():
    newlist = []
    user = input("commands "+",".join(addlist)+": ")
    print(" ")
    userlist = user.split(",")
    newlist.append(userlist[0])
    newlist.extend(addlist)
    newlist.extend(userlist[1:])
    user = ",".join(newlist)
    if(len(user.split(","))<2):
        if (user == "exit"):
            picklesave()
            return False
        elif (user == "die"):
            print("Exitted without saving","\n")
            return False
        else:
            return True
    else:
        parse_input(user)
        return True;
        

if path.exists("grades.json"):        
    with open("grades.json","r") as file:
        data=json.load(file)

global addlist
addlist = []
display_classes()
while(get_input()):
    print(" ")
    display_classes()


