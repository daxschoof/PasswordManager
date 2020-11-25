import sqlite3
import sys
import signal
from hashlib import sha256

conn = sqlite3.connect('PasswordManager.db')
c = conn.cursor()

def ExitHandler(signal, frame):
	if signal is None:
		print()
	print("\n* Goodbye!")
	sys.exit(0)

def addPass(service, password):
	servHash = sha256(service.encode('utf-8')).hexdigest()

	command = 'INSERT INTO passwords VALUES (%s, %s)' %('"' + servHash + '"', '"' + password + '"')
	c.execute(command)

	conn.commit()

def getPass(service):
	servHash = sha256(service.encode('utf-8')).hexdigest()

	command = 'SELECT hashCode FROM passwords where service = %s' %('"' + servHash + '"')
	for row in c.execute(command):
		return row[0]

def changePass(service, password):
	servHash = sha256(service.encode('utf-8')).hexdigest()

	command = 'UPDATE passwords SET hashCode = %s WHERE service = %s' %('"' + password + '"', '"' + servHash + '"')
	c.execute(command)
	conn.commit()

def main():
	masterPass = None

	for row in c.execute('SELECT * FROM passwords'):
		if row[0] == 'ADMIN':
			masterPass = row[1]

	if masterPass is None:
		newMaster = ''
		while newMaster == '':
			newMaster = input('Please input your new master password\n: ')
		hashPass = sha256(newMaster.encode('utf-8')).hexdigest()
		command = 'INSERT INTO passwords VALUES ("ADMIN", %s)' %('"' + hashPass + '"')
		c.execute(command)
	else:
		inPass = input('Master Password\n: ')
		shaPass = sha256(inPass.encode('utf-8')).hexdigest()
		while shaPass != masterPass:
			print('Wrong password!')
			inPass = input('Master Password\n: ')
			shaPass = sha256(inPass.encode('utf-8')).hexdigest()
		print("\nCorrect!")

	while(True):
		print("\n* Enter \'Change\' to change the master password                     ")
		print("* Enter \'Get\' and a website or application to get that password    ")
		print("* Enter \'Add\' and a website or application to add a password       ")
		print("* Enter \'Exit\' to exit the program                                 ")
		commInp = input(": ")
		
		if len(commInp) > 6 and commInp.lower()[0:6] == 'change' and commInp.lower()[6] == ' ':
			servPass = sha256(commInp[7:].encode('utf-8')).hexdigest()
			checkCom = 'SELECT hashCode FROM passwords WHERE service = %s' %('"' + servPass + '"')
			exists = True
			row = c.execute(checkCom)
			if row.fetchone() is None:
				exists = False

			if not exists:
				print("\n* There is no password for " + commInp[7:] + ".\n* Please use add to add a password for this service")
			else:
				newPass = ""
				while newPass == "":
					newPass = input("\n* Please input your new password for " + commInp[7:] + '\n: ')
				changePass(commInp[7:], newPass)
				print("\n* Password changed for service " + commInp[7:])
		
		elif len(commInp) > 3 and commInp.lower()[0:3] == 'get' and commInp.lower()[3] == ' ':
			gottenPass = getPass(commInp[4:])
			if gottenPass is None:
				print("\n* No password was found for service " + commInp[4:] + ".\n* Please check your spelling or add a password for that service")
			else:
				print("\n* The password for service " + commInp[4:] + " is: " + gottenPass)
		
		elif len(commInp) > 3 and commInp.lower()[0:3] == 'add' and commInp.lower()[3] == ' ' and commInp[4] != ' ':
			servPass = sha256(commInp[4:].encode('utf-8')).hexdigest()
			checkCom = 'SELECT hashCode FROM passwords WHERE service = %s' %('"' + servPass + '"')
			exists = True
			row = c.execute(checkCom)
			if row.fetchone() is None:
				exists = False

			if exists:
				print("\n* There is already a password for " + commInp[4:] + ".\n* Please use a different command for this service")
			else:
				newPass = ""
				while newPass == "":
					newPass = input("\n* Please input your new password for " + commInp[4:] + '\n: ')
				addPass(commInp[4:], newPass)
				print("\n* Password for service " + commInp[4:] + " added")

		elif commInp.lower()[0:4] == 'exit':
				ExitHandler(None, None)
		
		else:
			print("Command " + commInp + " was not recognized")
		

	conn.commit()
	conn.close()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, ExitHandler)
	main()