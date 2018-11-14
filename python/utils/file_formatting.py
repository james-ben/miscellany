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
	c = apt.Cache()
	if not c['enscript'].is_installed:
		print("enscript is not installed")
		return
	if not c['ghostscript'].is_installed:
		print("ghostscript is not installed")
		return

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
