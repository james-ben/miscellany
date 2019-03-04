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

# global variables
filelist = []
listbox = None
root = None
tabSize = 4
output_filename = "formatted_code.pdf"
outfile_box = None
language = ""
font = "Courier8"
fmt = "-R"
enaLinNum = None
enaHeader = None

def sortFileList():
	global filelist
	# sort it alphabetically
	return filelist
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
# enscript arguments:
#	--color
#	--tabsize: number of spaces in a tab
#	-C: each line starts with line-number
#	-B: no header
#	-M: nedia output type
#	-E: language syntax highlighting
#	-f: font & size
#	-R: portrait (-r is landscape)
# TODO: toggle line numbers and headers
def runFormatter():
	global filelist, outfile_box, language, font, fmt, enaHeader, enaLinNum
	if len(filelist) > 0:
		files = sortFileList()
		allStrings = ' '.join(files)
		lineNumString = '-C' if (enaLinNum.get() == 1) else '-c'

		# this is a hacky way to do it
		f_cmd = "echo {fls} |  xargs enscript --color=1 --tabsize={tabs} {lNum} -B -M Letter -E{lang} -f{fnt} {align} -o - | ps2pdf - {of}".format(fls=allStrings, tabs=tabSize, align=fmt, of=outfile_box.get(), lang=language, fnt=font, lNum=lineNumString)
		os.system(f_cmd)
		print("Files have been formatted and written to {}".format(outfile_box.get()))
		# sys.exit(0)
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


def delAllFiles():
	global listbox, filelist
	listbox.delete(0, tkinter.END)
	filelist = []


def choose_lang(value):
	global language
	if value == "none":
		language = ""
	else:
		language = value


def choose_font(value):
	global font
	font = value


def choose_orientation(value):
	global fmt
	if value == "portrait":
		fmt = "-R"
	else:
		fmt = "-r"


def main():
	global listbox, root, outfile_box, enaLinNum, enaHeader

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
	top2 = tkinter.Frame(root)
	top2.pack(side=tkinter.TOP)
	top3 = tkinter.Frame(root)
	top3.pack(side=tkinter.TOP)
	top4 = tkinter.Frame(root)
	top4.pack(side=tkinter.TOP)
	# bottom = tkinter.Frame(root)
	# bottom.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

	enaLinNum = tkinter.IntVar(root)
	enaHeader = tkinter.IntVar(root)

	tkinter.Button(root, text="Add files", command=getSources).pack(in_=top, side=tkinter.LEFT)
	tkinter.Button(root, text="Add folder", command=getDir).pack(in_=top, side=tkinter.LEFT)
	tkinter.Button(root, text="Remove files", command=delFiles).pack(in_=top, side=tkinter.LEFT)
	tkinter.Button(root, text="Clear all files", command=delAllFiles).pack(in_=top, side=tkinter.LEFT)

	# drop down menus
	l1 = tkinter.Label(root, text="Language:")
	l1.pack(in_=top2, side=tkinter.LEFT)
	# list all the possible styles with `enscript --help-highlight`
	langs = ("none", "asm", "bash", "c", "cpp", "html", "java", "javascript", "lua", "makefile", "matlab", "octave", "pascal", "perl", "postscript", "python", "tcl", "tex", "verilog", "vhdl")
	dropVar1 = tkinter.StringVar()
	dropVar1.set(langs[0]) # default choice
	dropMenu1 = tkinter.OptionMenu(top2, dropVar1, *langs, command=choose_lang)
	# dropMenu1.grid(column=1,row=4)
	dropMenu1.pack(in_=top2, side=tkinter.LEFT)

	l2 = tkinter.Label(root, text="Font:")
	l2.pack(in_=top2, side=tkinter.LEFT)
	fonts = ("Courier8", "Times-Roman12")
	dropVar2 = tkinter.StringVar()
	dropVar2.set(fonts[0])
	dropMenu2 = tkinter.OptionMenu(top2, dropVar2, *fonts, command=choose_font)
	dropMenu2.pack(in_=top2, side=tkinter.LEFT)

	# orientation
	l3 = tkinter.Label(root, text="orientation:")
	l3.pack(in_=top2, side=tkinter.LEFT)
	ors = ("portrait", "landscape")
	dropVar3 = tkinter.StringVar()
	dropVar3.set(ors[0])
	dropMenu3 = tkinter.OptionMenu(top2, dropVar3, *ors, command=choose_orientation)
	dropMenu3.pack(in_=top2, side=tkinter.LEFT)

	# line numbers
	l4 = tkinter.Label(root, text='Line Numbers:')
	l4.pack(in_=top3, side=tkinter.LEFT)
	check1 = tkinter.Checkbutton(root, var=enaLinNum)
	check1.select()
	check1.pack(in_=top3, side=tkinter.LEFT)

	# headers
	l5 = tkinter.Label(root, text='Headers:')
	l5.pack(in_=top3, side=tkinter.LEFT)
	check2 = tkinter.Checkbutton(root, var=enaHeader)
	check2.deselect()
	check2.pack(in_=top3, side=tkinter.LEFT)

	# name of the output file
	l6 = tkinter.Label(root, text="Output filename:")
	l6.pack(in_=top4, side=tkinter.LEFT)
	outfile_box = tkinter.Entry(root)
	outfile_box.insert(0, "formatted_code.pdf")
	outfile_box.pack(in_=top4, side=tkinter.LEFT)

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
