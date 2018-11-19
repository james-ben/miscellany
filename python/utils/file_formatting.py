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


def sortFileList():
	global filelist
	# sort it alphabetically
	files = sorted(filelist)
	# switch the ordering of any .c and .h files that go together
	for i in range(len(files)-1):
		cur = files[i]
		nex = files[i+1]
		if cur[:-1] == nex[:-1]:
			# swap
			files[i], files[i+1] = files[i+1], files[i]
	return files


# runs the formatting script
def runFormatter():
	global filelist
	if len(filelist) > 0:
		outfile = "test_formatting.pdf"
		files = sortFileList()
		allStrings = ' '.join(files)
		# this is a hacky way to do it
		f_cmd = "echo {} |  xargs enscript --color=1 --tabsize={} -C -B -M Letter -Ec -fCourier8 -o - | ps2pdf - {}".format(allStrings, tabSize, )
		os.system(f_cmd)
		print("Files have been formatted and written to {}".format(outfile))
		sys.exit(0)
	else:
		return


# gets source files for the formatting script
def getSources():
	# get the files you want
	filenames = filedialog.askopenfiles(parent=root, mode='r', title="Choose source files")
	for f in filenames:
		listbox.insert(tkinter.END, f.name)
		filelist.append(f.name)


def getDir():
	# get all the files in a directory
	dirname = filedialog.askdirectory(title='Choose source directories')
	if dirname:
		# print(dirname)
		files = os.listdir(dirname)
		for f in files:
			f = dirname + '/' + f
			listbox.insert(tkinter.END, f)
			filelist.append(f)


# removes files from the list
def delFiles():
	global listbox, filelist
	selection = listbox.curselection()
	if selection:
		listbox.delete(selection[0])
		del filelist[selection[0]]


def main():
	global listbox, root

	# check if the right packages are installed
	#  this is specific to Ubuntu distributions, or others using APT package manager
	c = apt.Cache()
	if not c['enscript'].is_installed:
		print("enscript is not installed")
		return
	if not c['ghostscript'].is_installed:
		print("ghostscript is not installed")
		return

	# create a window
	root = tkinter.Tk()
	# frames
	top = tkinter.Frame(root)
	top.pack(side=tkinter.TOP)
	# bottom = tkinter.Frame(root)
	# bottom.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

	tkinter.Button(root, text="Add files", command=getSources).pack(in_=top, side=tkinter.LEFT)
	tkinter.Button(root, text="Add folder", command=getDir).pack(in_=top, side=tkinter.LEFT)
	tkinter.Button(root, text="Remove files", command=delFiles).pack(in_=top, side=tkinter.LEFT)

	# this displays all the files you picked
	listbox = tkinter.Listbox(root)
	listbox.pack()
	listbox.config(width=75)

	# run the formatting script
	runButton = tkinter.Button(root, text="Format code", command=runFormatter)
	runButton.pack()

	# run
	root.mainloop()


if __name__ == '__main__':
	main()
