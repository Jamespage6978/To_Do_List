import os 
import sys
import csv
import argparse
import numpy
from pprint import pprint
from PyInquirer import prompt, print_json,Separator
from tabulate import tabulate
import datetime
import time


parser = argparse.ArgumentParser(description = "Simple todo list creator and manager.")
parser.add_argument('--User', type=str, help="User account quick access")
args = parser.parse_args()

currentUser = "global"

def Menu():

    global currentUser

    questions = [ 
        {
        'type': 'list',
        'name': 'mainMenu',
        'message': 'Select an option',
        'choices': ['Login','Add new User','Exit'] 
        }
    ]

    answers = prompt(questions)
    if answers['mainMenu'] == 'Login':
        SelectedUser = Login()
        currentUser = SelectedUser
        Load(currentUser)
    elif answers['mainMenu'] == 'Add new User':
        print("not implemented yet")
    elif answers['mainMenu'] == 'Exit':
        sys.exit()

    return SelectedUser

def Login():

    
    questions = [ 
        {
        'type': 'list',
        'name': 'userSelect',
        'message': 'Select a user',
        'choices': getUserList()
        }
    ]

    answers = prompt(questions)
    SelectedUser = answers['userSelect']
    return SelectedUser

def getUserList():
    with open('Config/User_accounts.txt') as f:
        accounts = list(csv.reader(f))
    accounts = accounts[0]

    return accounts

def ReadTodoFile(currentUser,Directory = "Data/",dictSwitch = 0):
    for root, dirs, files in os.walk(Directory):
        for file in files:
            if file.endswith(currentUser +".todo"):
                userFile = os.path.join(root,file)
                print("~~~~ File Found in " + os.path.join(root,file)+ " ~~~~")
    if len(userFile) != 0:
        with open(userFile) as f:
            next(f)
            todoMasterList = list(csv.reader(f))
    # for i in range(len(todoMasterList)):
    #   todoMasterList[i].insert(4,dateConvert(float(todoMasterList[i][2])-float(int(time.time())),days=True))
    #   todoMasterList[i][2] = dateConvert(todoMasterList[i][2])
    #   todoMasterList[i][3] = dateConvert(todoMasterList[i][3])


    if dictSwitch == 0:
        return  dict(enumerate(todoMasterList))
    elif dictSwitch == 1:
        return todoMasterList

def dateConvert(unixTime,days=False):
     if days:
        dateT  = datetime.datetime.fromtimestamp(int(unixTime)).strftime('%d')
        print(dateT)
     else:
         dateT  = datetime.datetime.fromtimestamp(int(unixTime)).strftime('%d-%m-%Y')

     return dateT

def Load(currentUser):
    todoMasterList = ReadTodoFile(currentUser,dictSwitch=1)
    print(tabulate(todoMasterList,headers=["Task Title","Task","Status"], showindex="always", tablefmt="github"))
    SecondaryMenu()

def SecondaryMenu():
    questions = [ 
        {
        'type': 'list',
        'name': 'secondMenu',
        'message': 'Select an option',
        'choices': ['Add New Task','Edit Task','Goto Main Menu'] 
        }
    ]

    answers = prompt(questions)

    if answers['secondMenu'] == 'Goto Main Menu':   
        Menu()
    elif answers['secondMenu'] == 'Add New Task':
        addTask()
    elif answers['secondMenu'] == 'Edit Task':
        editTask()
 

def addTask():
    print("AddTask")
    SecondaryMenu()


def editTask():
    print("Edit Task")
    deleteTask()
    SecondaryMenu()


def deleteTask():
    print("Delete")


if __name__ == '__main__':
    if args.User is not None:
        Users = getUserList()
        if args.User in Users:
            print("~~~~ Logging in as " + args.User + " ~~~~")
            currentUser = args.User
        else:
            print("~~~~ User not in current User list taking you to the main menu ~~~~")
            Menu()
    else:
        Menu()
    
    