import os
import sys
import random
import apt
# import the right stuff
try:
	import tkinter
	from tkinter import filedialog
except ImportError as e:
	print("You need the tkinter library")
	print("sudo apt install python3-tk")
	sys.exit(1)

filelist = []
listbox = None
root = None
tabSize = 4


# gets source files for the formatting script
def getSources():
	# get the files you want
	filenames = filedialog.askopenfiles(parent=root, mode='r', title="Choose source files")
	for f in filenames:
		listbox.insert(tkinter.END, f.name)
		filelist.append(f.name)


# runs the formatting script
def runFormatter():
	allStrings = ' '.join(filelist)
	# this is a hacky way to do it
	f_cmd = "echo {} | sed '/CMakeFiles/d' | sort -r |  xargs enscript --color=1 --tabsize={} -C -B -M Letter -Ec -fCourier8 -o - | ps2pdf - {}".format(allStrings, tabSize, "test_formatting.pdf")
	os.system(f_cmd)
	sys.exit(0)

def main():
	global listbox, root

	# check if the right packages are installed
	# cache = apt.Cache()
	# if cache['enscript'].is_installed:
	# 	print("enscript is not installed")
	# 	return
	# if cache['ps2pdf'].is_installed:
	# 	print("ghostscript is not installed")
	# 	return
	cmd1 = 'type enscript >/dev/null 2>&1 || { echo >&2 "I require enscript but it is not installed.  Aborting."; exit 1; }'
	cmd2 = 'type ps2pdf >/dev/null 2>&1 || { echo >&2 "I require ghostscript but it is not installed.  Aborting."; exit 1; }'
	cmdval1 = os.system(cmd1)
	cmdval2 = os.system(cmd2)
	if (cmdval1 or cmdval2):
		return 1

	# create a window
	root = tkinter.Tk()
	tkinter.Button(root, text="Add files", command=getSources).pack()

	# this displays all the files you picked
	listbox = tkinter.Listbox(root)
	listbox.pack()
	listbox.config(width=50)

	# run the formatting script
	runButton = tkinter.Button(root, text="Format code", command=runFormatter)
	runButton.pack()

	# run
	root.mainloop()




if __name__ == '__main__':
	main()
