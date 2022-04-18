import os

def_user  = "Polikarpus"
def_path = ['D:']

temp_user = 'Polikarpus'
main_user = "Polikarpus"
main_path = ['D:']

list_user = {}
root_user = {'root':'root'}

is_root = False

def err(args):
	print("error: " + args)

def check_root():
	if not is_root:
		err("Regular user like you don't have access to this command")
		return False
	else:
		return True

def get_def_data():
	global def_user # to identify that this is global variabel
	global def_path
	global list_user
	
	with open('data') as files:
		contents = files.readlines()

	# account
	for i in range(len(contents)):
		username, password = contents[i].split(' ')
		list_user.update({username:password[0:len(password) - 1]})

	with open('def_data') as files:
		contents = files.readlines()

	def_user = contents[0][0:len(contents[0]) - 1]
	def_path = contents[1].split(' ')

def init():
	get_def_data()

	global def_user, def_path, main_user, main_path
	main_user, main_path = def_user, def_path

def end_it():
	temp_text = ""
	for key, val in list_user.items():
		temp_text = temp_text + key + " " + val + '\n'

	with open('data', 'w') as files:
		files.write(temp_text)

def build_path():

	global main_path

	res_path = main_path[0]
	for i in range(1, len(main_path)):
		res_path = res_path + "/" + main_path[i]
	return res_path

def login():

	# return False -> start the machine
	# return True  -> exit the machine

	global is_root, main_user, temp_user, list_user, def_path, def_user

	while True:
		os.system("cls")
		print()


		# if there are no user avaiable
		
		if len(list_user) == 0:
			username = input("Create new account  -> ")
			password = None
			retype   = None

			while password == None:
				password = input("Create a password   -> ")
				retype   = input("Retype the password -> ")

				if password == retype:
					list_user.update({username : password})
					main_user = username
					temp_user = main_user
					def_user  = main_user

					# set the default user
					tmp_path = def_path[0]
					for i in range(1, len(def_path)):
						tmp_path = tmp_path + " " + def_path[i]

					with open('def_data', 'w') as files:
						files.write(def_user + '\n' + tmp_path)
					return False

				else:
					err('Password not match!')

					while True:
						print("Do you want to retype your password again?[Y/n]")
						print()
						t_com = input("Command: ")
						t_com = t_com.upper()

						if t_com == 'Y':
							password = None
							break
						elif t_com == 'N':
							return True # exit the machine
						else:
							err("Invalid command!")
							print("expected: y, n")
							print()
			return False

		# else
		username = input("Username -> ")
		password = input("Password -> ")

		if list_user.get(username) == password:
			main_user = username
			temp_user = main_user
			os.system("cls")
			return False # start the machine
		else:
			print()

			if list_user.get(username) == None:
				err("User not found!")

			else:
				err("Username and password doesn't match!")

			while True:
				print("Do you want to retype your account again?[Y/n]")
				print()

				t_com = input("Command: ")

				t_com = t_com.upper()

				if t_com == "Y":
					break
				elif t_com == "N":
					return True # exit the machine
				else:
					print()
					err("Invalid command!")
					print("expected: y, n")
					print()

def root():
	
	global root_user
	print()
	password = input("Password for root user: ")

	if password == root_user.get("root"):

		global is_root, main_user, temp_user
		
		is_root = True
		temp_user = main_user
		main_user = 'root'
	else:
		err("Wrong password!")
        
def ex_sudo():

	global is_root, main_user, temp_user
	main_user = temp_user
	is_root = False
