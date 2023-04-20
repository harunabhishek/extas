#!/usr/bin/env python3
# This a program to automate the formatting process of the disks and drives from cmd in windows.


import subprocess, re, time, ctypes, sys

command_output = ""
def user_choices():
	# Ask user to make choices
	global command_output
	print('\nEnter the disk to be selected....Enter "r" to RESCAN....', end="")
	while True:
		selected_disk = input("")
		re_expression = "(?:Disk\s)(\d*)(?:\s)"
		available_disks = re.findall(re_expression, command_output)
		if selected_disk in available_disks:
			if selected_disk == "0" or selected_disk == "1":
				print("[-] Disk 0 and 1 are not allowed to be selected....TRY Again....", end="")
				continue
			else:
				break
		else:
			print("[-] Please Select from availabe disks....RESCANNING")
			
			lis_dis()
			time.sleep(2)
			subprocess.call("cls", shell=True)
			print(command_output)
			print("\nEnter the disk to be selected....", end="")
			continue

	return selected_disk

def create_script_file(commands):
	# Write commands in a file so dispart can use it as a script
	with open ("diskpart_script.txt", "w") as out_file:
		out_file.write(commands)

def create_operation_script(selected_disk, file_system):
	# Forms the commands to be written
	commands = "sel dis " + selected_disk + "\n"
	commands = commands + "clean\n"
	commands = commands + "create par pri\n"
	commands = commands + "sel par 1\n"
	commands = commands + "format fs=" + file_system +" quick"

	create_script_file(commands)

def lis_dis():
	# Lis all diks available on the system
	global command_output
	create_script_file("lis dis")
	command_output = subprocess.check_output("diskpart /s diskpart_script.txt", shell=True)
	command_output = command_output.decode()
	

def execute_command():
	# Executes the commands on the terminal
	global command_output
	subprocess.call("cls", shell=True)
	lis_dis()
	print(command_output)
	selected_disk = user_choices()
	re_expression = "(?:Disk " + selected_disk + ".*?\s)(\d+)"
	file_system = re.search(re_expression, command_output).group(1) 		#use "re.match" that match the string from starting, use 're.search' to match within string
																			#also use ".group(group_no)" for various groups, eg:- result.group(1 )

	if int(file_system[0]) <= 32:
		file_system = "FAT32"
		# print(file_system)

	create_operation_script(selected_disk, file_system)
	subprocess.call("diskpart /s diskpart_script.txt", shell=True)
	# command_output = subprocess.check_output("diskpart /s diskpart_script.txt", shell=True)
	# command_output = command_output.decode()

	# command_output = command_output.replace("\r", "")										#removed "\r" from the string, creating issues
	# # matched_data = re.search("Micro.*OVO", command_output, re.S).group(0)
	# # command_output = command_output.replace(matched_data, "")
	# command_output = re.sub(".*OVO", "", command_output,flags=re.S)							# used "re.S" dot character also includes new line character
	# print(command_output)

	
def run():
	# Handles the errors
	try:
		execute_command()
		print("Enter q to quit....", end="")
		while True:
			choice = input("")
			if choice == "q":
				exit()	
			else:
				print("Not allowed")
				continue

	except KeyboardInterrupt:
		print("\n[+] Exitting..")
		time.sleep(3)
	except Exception as error:
		print("[-] Some Error Occured...Exitting...>> " + str(error))
		time.sleep(5)



def is_admin():
	# checks the execution with admin privledges
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# main code
# To run with admin privileges
if is_admin():
    run()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
