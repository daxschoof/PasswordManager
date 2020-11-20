import sqlite3
from hashlib import sha256

conn = sqlite3.connect('PasswordManager.db')

c = conn.cursor()

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
	print("Correct!")

conn.commit()
conn.close()