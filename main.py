import os 
import sys
import csv


currentUser = "global"

def Menu():

	global currentUser

	print("""
		1. Login
		2. Add new user
		
		Select an option """
		)
	Selection1 = int(input("~~~~> "))
	if Selection1 == 1:
		SelectedUser = Login()
		print(SelectedUser + "Selected and loading ...")
		currentUser = SelectedUser
	elif Selection1 == 2:
		print("not implemented yet")

	return SelectedUser

def Login():
	with open('Config/User_accounts.txt') as f:
		accounts = list(csv.reader(f))
	print('Select account')
	for i in range(len(accounts[0])):
		print("{0}. {1}".format(str(i+1),accounts[0][i]))
	usrSelection = int(input("~~~~> ") - 1)

	SelectedUser = accounts[0][usrSelection]
	return SelectedUser

def Load():

def CreateNew():

def addTask():

def deleteTask():

def updateTask():

if __name__ == '__main__':
	print(currentUser)
	Menu()
	Load()
	print(currentUser) 