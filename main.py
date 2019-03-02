import os 
import sys
import csv
from pprint import pprint
from PyInquirer import prompt, print_json,Separator

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





def Load(currentUser):
	for root, dirs, files in os.walk("Data/"):
		for file in files:
			if file.endswith("James.todo"):
				userFile = os.path.join(root,file)
				print(os.path.join(root,file))
	if len(userFile) != 0:
		with open(userFile) as f:
			next(f)
			todoMasterList = list(csv.reader(f))
			print(todoMasterList[0])
	questions = [
    	{
        	'type': 'checkbox',
        	'qmark': '😃',
        	'message': 'Select toppings',
        	'name': 'toppings',
        	'choices': [ 
           		 Separator('= The Meats ='),
            	{
                	'name': 'Ham'
           		 },
            	{
                	'name': 'Ground Meat'
				},
				]
		}
	]
	answers = prompt(questions)


# def CreateNew():

# def addTask():

# def deleteTask():

# def updateTask():

if __name__ == '__main__':
	Menu()
	Load(currentUser)