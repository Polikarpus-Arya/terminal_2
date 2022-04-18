import os
import handle

# every command list are available here

# change directory
# use to manage the directory
# clock

def cd(com):
	if len(com) == 1:
		print(handle.build_path())
		return
			
	if com[1] == "..":
		if len(handle.main_path) > 1:
			handle.main_path.pop()

	elif com[1] == '...':
		while len(handle.main_path) > 1:
			handle.main_path.pop()

	else:

		while len(com) > 2:
			com[-2] = com[-2] + ' ' + com[-1]
			com.pop()

		if os.path.exists(com[1]) and os.path.isdir(com[1]):
			handle.main_path = list(com[1].split(" "))

		elif os.path.exists(handle.build_path() + "/" +\
			com[1]) and os.path.isdir(handle.build_path() + "/" + com[1]):
			
			if com[1][0] == '/' or com[1][0] == '\\':
				com[1][0] = com[1][1:]
			tmp = ""
			for c in com[1]:
				if c == '/' or c == '\\':
					handle.main_path.append(tmp)
					tmp = ''
				else:
					tmp = tmp + c

			if com[1][-1] != '/' and com[1][-1] != '\\':
				handle.main_path.append(tmp)

		else:
			handle.err("Your path is invalid!")

# set function ==========================================
# use to set default username and path of the terminal
def set(com):

	def set_path(com):
		handle.get_def_data()
	
		if os.path.exists(com[2]) and os.path.isdir(com[2]):
			handle.def_path.clear()
	
			tmp_path = ''
	
			for i in range(len(com[2])):
				if com[2][i] == '/' or com[2][i] == '\\':
					if i < len(com[2]) - 1:
						tmp_path += ' '
					else:
						com[2] = com[2][0:len(com[2]) - 1]
				else:
					tmp_path += com[2][i]
	
			with open('def_data', 'w') as files:
				files.write(handle.def_user + '\n' + tmp_path)
	
			print("The default path is set to: " + com[2])
		else:
			handle.err("Path not found")
	# ======================================================
	def set_user(com):
		handle.get_def_data()
	
		if handle.list_user.get(com[2]) == None:
				handle.err("User not found!")
		elif com[2] == 'root':
			handle.err("Can't set this user as default user!")
		else:
			handle.def_user = com[2]
	
			tmp_path = handle.def_path[0]
			for i in range(1, len(handle.def_path)):
				tmp_path = tmp_path + " " + handle.def_path[i]
	
			with open('def_data', 'w') as files:
				files.write(handle.def_user + '\n' + tmp_path)
	
			print("The default user is set to: " + com[2])

	# ======================================================

	if not handle.check_root():
		return

	if len(com) != 3:
		handle.err("Invalid syntax!")
		return

	if com[1] == "user":
		set_user(com)

	elif com[1] == "path":
		set_path(com)

	else:
		handle.err("Invalid syntax!")

# ls function ======================================
def ls_main(com):

	def ls_files():
		temp_path = handle.build_path()
		print(temp_path)
		file_list = os.listdir(temp_path + '/')
	
		ls_folder = []
		ls_file   = []
	
		for file in file_list:
			if os.path.isdir(temp_path + '/' + file):
				ls_folder.append(file)
			else:
				ls_file.append(file)
	
		print("Folder list:")
		for file in ls_folder:
			print('  ' + file + '/')
	
		print()
		print("File list:")
		for file in ls_file:
			print('  ' + file)

	# ======================================================

	def ls_account():
		print("List of available account:")
		for key in handle.list_user:
			print('  ' + key)

	# ======================================================

	print()
	if len(com) == 1:
		print("Format: ls [argument]")
		print()
		print("list of argument:")
		print(' ac' + ' ' * 5 + 'to print account list')
		print('  f' + ' ' * 5 + 'to print folder and file list')
	elif len(com) == 2:
		com[1] = com[1].lower()

		if com[1] == 'f':
			ls_files()
		elif com[1] == 'ac':
			ls_account()
		else:
			handle.err("Wrong arguments provided!")
			print("Type \"ls\" for help!")
	else:
		handle.err("Too many arguments for list command!")
		print("Type \"ls\" for help!")


def reset_to_default(com):

	if (len(com) > 1):
		handle.err("Invalid syntax!")
		return
	
	handle.get_def_data()
	handle.main_user = handle.def_user
	handle.main_path = handle.def_path

	print("The user and path are set to default")

# control user ================================

def con_user(com):
	if not handle.check_root():
		return

	if len(com) == 1:
		print()
		print("Format: user [args]")
		print("\nargs:")
		print(' ' * 2 + "add" + ' ' * 5 + '-> add new user')
		print(' ' * 2 + "del" + ' ' * 5 + '-> delete user')
		print(' ' * 4 + "[args]: username to be removed")
	else:
		if com[1] == 'add':
			add_user()
		elif com[1] == 'del':
			del_user(com)
		else:
			handle.err("Invalid arguments")

def add_user():
	
	print()
	username = input("Create an account   -> ")

	if handle.list_user.get(username) != None:
		handle.err("Username already exist!")
		return

	password = input("Create a password   -> ")
	retype   = input("Retype the password -> ")

	if retype != password:
		handle.err("The password are not the same!")
		return

	handle.list_user.update({username:password})

	text = ""
	for key, val in handle.list_user.items():
		text += key + " " + val + '\n'

	with open('data', 'w') as files:
		files.write(text)

def del_user(com):

	print()
	username = ''
	if len(com) == 3:
		username = com[2]
	else:
		username = input("Type an account to be deleted -> ")
		print()

	if username == 'root':
		handle.err("You can't remove this user!")
		return

	if handle.list_user.get(username) == None:
		handle.err("Username not found!")
		return
	
	del handle.list_user[username]
	print(username + ' has been removed!')

	text = ""
	for key, val in handle.list_user.items():
		text += key + " " + val + '\n'

	with open('data', 'w') as files:
		files.write(text)

def tree():
	def tree_dfs(par, space):
		file_obj = []
		try:
			file_obj  = os.listdir(par + '/')
		except PermissionError as e:
			return
		for file in file_obj:
			if os.path.isdir(par + '/' + file):
				print(' ' * space + file + '/')
				tree_dfs(par + '/' + file, space + 4)
			else:
				print(' ' * space + file)


	com_main = handle.build_path()
	print()
	print("Tree of " + com_main)
	file_obj = os.listdir(com_main + '/')
	for file in file_obj:
		if os.path.isdir(com_main + '/' + file):
			print(' ' * 4 + file + '/')
			tree_dfs(com_main + '/' + file, 8)
		else:
			print(' ' * 4 + file)

def find_files(file_to_find):

	found_in = []

	def search_dfs(par):
		file_obj = []
		try:
			file_obj  = os.listdir(par + '/')
		except PermissionError as e:
			return

		for file in file_obj:
			if file == file_to_find:
				if os.path.isdir(par + '/' + file):
					found_in.append(par + '/' + file + '/')
				else:
					found_in.append(par + '/' + file)
			if os.path.isdir(par + '/' + file):
				search_dfs(par + '/' + file)


	com_main = handle.build_path()
	try:
		file_obj  = os.listdir(com_main + '/')
	except PermissionError as e:
		handle.err("Access is denied")
		return

	for file in file_obj:
		if file == file_to_find:
			if os.path.isdir(com_main + '/' + file):
				found_in.append(com_main + '/' + file + '/')
			else:
				found_in.append(com_main + '/' + file)
		if os.path.isdir(com_main + '/' + file):
			search_dfs(com_main + '/' + file)

	print()

	if len(found_in) == 0:
		print(file_to_find + " not found :(")
		return

	print(file_to_find + " is found in:")
	for file in found_in:
		print(' ' * 4 + file)