import os 
import sys
import csv
from pprint import pprint
from PyInquirer import prompt, print_json,Separator
import datetime
import tzlocal

currentUser = "global"

def Menu():

	global currentUser

	questions = [ 
		{
        'type': 'list',
        'name': 'mainMenu',
        'message': 'Select an option',
        'choices': ['Login','Add new User',] 
		}
	]

	answers = prompt(questions)
	if answers['mainMenu'] == 'Login':
	 	SelectedUser = Login()
	 	print(SelectedUser + " Selected and loading ...")
	 	currentUser = SelectedUser
	elif answers['mainMenu'] == 'Add new User':
	 	print("not implemented yet")

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
	
	if dictSwitch == 0:
		return	dict(enumerate(todoMasterList))
	elif dictSwitch == 1:
		return todoMasterList

def dateConvert(unixTime):
	 dateT  = datetime.datetime.fromtimestamp(int(unixTime)).strftime('%d-%m-%Y')
	 return dateT


def Load(currentUser):
	print("LOAD FUNCTION")
	print(ReadTodoFile(currentUser,dictSwitch=1))
	todoMasterList = ReadTodoFile(currentUser,dictSwitch=1)

	for i in range(len(todoMasterList)):
			dateCreated = dateConvert((float(todoMasterList[i][2])))
			dateDeadline = dateConvert((float(todoMasterList[i][3])))
			print("~ Task Title ~~ Task ~~ Date Created ~~ Deadline ")
			print("| "+todoMasterList[i][0] + " | "+todoMasterList[i][1] + " | "+ dateCreated + " | "+ dateDeadline+ " |")

	# questions = [
 #    	{
 #        	'type': 'checkbox',
 #        	'qmark': '😃',
 #        	'message': 'Select toppings',
 #        	'name': 'toppings',
 #        	'choices': ReadTodoFile(currentUser)
	# 	}
	# ]
	# answers = prompt(questions)
	# print(answers)


# def CreateNew():

# def addTask():

# def deleteTask():

# def updateTask():

if __name__ == '__main__':
	Menu()
	Load(currentUser)