import os
import sys
import time

import terminal # list of command
import handle

done = False
def prompt(com):

	global done

	# change directory
	if com[0] == 'cd':
		terminal.cd(com)

	# list of available account
	elif com[0] == 'ls':
		terminal.ls_main(com)

	# exit terminal
	elif com[0] == 'exit':
		done = True
		handle.end_it()

	#set default user or path
	elif com[0] == 'set':
		terminal.set(com)

	# reset everything to default settings
	elif com[0] == 'def':
		terminal.reset_to_default(com)

	# control user
	elif com[0] == 'user':
		terminal.con_user(com)

	# command not found :(
	else:
		handle.err("Command not found :(")

def work():
	print(time.strftime("[%H:%M:%S] ", time.localtime()), end = '')
	print(handle.main_user + " ~/" + handle.build_path())
	com = list(input("\u03BB ").split(" ")) # lambda

	# enter root mode
	if com[0] == 'sudo':

		if len(com) == 1:
			if handle.is_root == False:
				handle.root()
			else:
				print("You are the administrator already!")

		else:
			com = com[1:]
			if handle.is_root == False:

				print()
				password = input("Password for root user: ")

				if password != handle.root_user.get("root"):
					handle.err("Wrong password!")
					print()
					return

				handle.is_root = True

				prompt(com)
				handle.ex_sudo()
			else:
				prompt(com)

	# exit root mode
	elif com[0] == 'ex':

		if len(com) == 1:
			if handle.is_root:
				handle.ex_sudo()
			else:
				handle.err("You have to enter root mode to run this command!")
		else:
			handle.err("Too many arguments to run this command!")
			handle.err("Required arguments: 0")

	else:
		prompt(com)

	if not done:
		print()

# driver code -------------------------------------------------

def main():

	global done
	handle.init()
	
	if len(sys.argv) == 1:
		done = handle.login()
		if done == False:
			print()
	
	elif len(sys.argv) == 2 and sys.argv[1] == "alog":
		os.system("cls")
		print()

	else:
		handle.err("Invalid argument!")
		done = True

	while not done:
		work()

main()