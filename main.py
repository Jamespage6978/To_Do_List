import os 
import sys
import csv
import glob
import argparse
import numpy
from pprint import pprint
from PyInquirer import prompt, print_json,Separator
from tabulate import tabulate
import datetime
import time
#testing remote on feature 1

parser = argparse.ArgumentParser(description = "Simple todo list creator and manager.")
parser.add_argument('--User', type=str, help="User account quick access")
parser.add_argument('--Add',type=str,help="quick add tasks")
args = parser.parse_args()

currentUser = "global"
currentDir = "global"

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
        newUser()
        Menu()
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
    accounts = []
    if os.path.isdir("Data"):
        os.chdir("Data")
        for file in glob.glob("*.todo"):
            filename = file.split(".")[0]
            user = filename.split("_")[1]
            accounts.append(user)
        os.chdir("..")

    return accounts

def ReadTodoFile(currentUser,Directory = "Data/",dictSwitch = 0):
    global currentDir
    for root, dirs, files in os.walk(Directory):
        for file in files:
            if file.endswith(currentUser +".todo"):
                userFile = os.path.join(root,file)
                currentDir = userFile
                print("~~~~ File Found in " + os.path.join(root,file)+ " ~~~~")
    if len(userFile) != 0:
        with open(userFile) as f:
            next(f)
            todoMasterList = list(csv.reader(f))

    todelStore = []
    for i in range(len(todoMasterList)):
        if todoMasterList[i]:
            row_value = todoMasterList[i][0]
            if row_value[0] == "#":
                todelStore.append(i)
        else:
            todelStore.append(i)
    for i in range(len(todelStore)):
        del todoMasterList[todelStore[i]]

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
        'choices': ['Add New Task','Edit Task','Delete Task','Goto Main Menu','View Tasks','Exit'] 
        }
    ]

    answers = prompt(questions)

    if answers['secondMenu'] == 'Goto Main Menu':   
        Menu()
    elif answers['secondMenu'] == 'Add New Task':
        addTask()
    elif answers['secondMenu'] == 'Edit Task':
        editTask()
    elif answers['secondMenu'] == 'Delete Task':
        deleteTask()
    elif answers['secondMenu'] == 'View Tasks':
        Load(currentUser) 
    elif answers['secondMenu'] == 'Exit':
        sys.exit()

def newUser ():
    global currentUser
    questions = [ 
        {
        'type': 'input',
        'name': 'newUser',
        'message': 'Enter username e.g persons name',
        }
    ]

    answers = prompt(questions)
    userToBeCreated = answers['newUser']
    print("~~~ creating new user " + answers['newUser'] +" ~~~~")
    if os.path.exists('Data/Todo_' + userToBeCreated+".todo"):
        print("todo list already found for user at" + 'Data/Todo_' + userToBeCreated+".todo")
    elif os.path.isdir("Data"):
        createNewUser(userToBeCreated)
    else:
        os.mkdir("Data")
        createNewUser(userToBeCreated)

    getUserList()

def createNewUser(userToBeCreated):
    f = open("Data/Todo_"+userToBeCreated+".todo","w+")
    f.write("#Title,Task,Status\n")
    f.close

    
def addTask():
    print("AddTask")

    questions = [
        {
            'type': 'input',
            'name': 'TaskTitle',
            'message': 'What is the title of the task?',
        },

        {
            'type': 'input',
            'name': 'Task',
            'message': 'What is the task to add?',
        },

        {
            'type': 'list',
            'name': 'status',
            'message': 'What is the current status?',
            'choices' : ['Complete','WIP','Not Started']
        },
    ]

    answers = prompt(questions)

    questionsConfirm = [

            {
            'type': 'confirm',
            'name': 'addCheck',
            'message': 'Your task is: Title: {} || Task: {} || Status: {}. Do you want to add this task?'.format(answers['TaskTitle'],answers['Task'],answers['status']),
            'default':False
        },

    ]
    answersConfirm = prompt(questionsConfirm)
    if answersConfirm['addCheck']:
        print("~~~~ adding task ~~~~")
        toAdd = []
        toAdd.append(answers['TaskTitle'].strip(' \n\t'))
        toAdd.append(answers['Task'].strip(' \n\t'))
        toAdd.append(answers['status'].strip(' \n\t')) 
        
        

        with open(currentDir, "a",newline='') as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(toAdd)
        print("~~~~ Task succesfully added ~~~~")
    else:
        print("~~~~ Returning to menu ~~~~~")
   
    SecondaryMenu()

def editTask():
    print("Edit Task")

    questions = [
        {
            'type': 'input',
            'name': 'editWhich',
            'message': 'Which task would you like to edit? enter line number.',
        },
    ]

    answers = prompt(questions)
    print(answers['editWhich'])
    SecondaryMenu()


def deleteTask():
    global currentDir
    questions = [ 
        {
        'type': 'input',
        'name': 'delete',
        'message': 'Select a line to delete',
        }
    ]

    answers = prompt(questions)
    rows = []
    with open(currentDir) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            rows.append(row)

    questionscheck = [ 
        {
        'type': 'confirm',
        'name': 'delete',
        'message': 'Do you want to delete Task: {} with Title: {}'.format(rows[int(answers['delete'])+1][1],rows[int(answers['delete'])+1][0]),
        }
    ]

    answerscheck = prompt(questionscheck)

    if answerscheck:
        rows[int(answers['delete'])+1][0] = '#' + rows[int(answers['delete'])+1][0]
        with open(currentDir, "w") as fp:
            wr = csv.writer(fp, dialect='excel')
            for row in rows:
                wr.writerow(row)
    SecondaryMenu()

def stringVal(a):
    if a.isaplha:
        return True 
    else:
        return False

if __name__ == '__main__':
    
    if args.User is not None and args.Add in ["1"]:
        Users = getUserList()
        if args.User in Users:
            currentUser = args.User
            ReadTodoFile(args.User,Directory="Data/",dictSwitch=0)
            addTask()
    
    
    elif args.User is not None:
        Users = getUserList()
        if args.User in Users:
            print("~~~~ Logging in as " + args.User + " ~~~~")
            currentUser = args.User
            Load(currentUser)
        else:
            print("~~~~ User not in current User list taking you to the main menu ~~~~")
            Menu()
    else:
        Menu()
    
    