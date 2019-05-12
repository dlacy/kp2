###===XML/TEI CONVERSION TOOL INTERFACE SCRIPT / ENCYCLOPEDIA PROJECT TEMPLE UNIVERSITY===###
#																							#
# This script launches the TEI/XML Conversion Tool GUI. 									#
#																							#
# Date Created: Oct 13, 2016																#
# Created by: Andrea Siotto - siotto.andrea@temple.edu										#
# Modified: January 24, 2019, Gary Scales - gary.scales@temple.edu 							#
#																							#
# Script Version Number: 8.08 Ampersand signs are still not right. 							#
# After python, they are missing the & in &amp;	            								#
# Python Version Used: 3.7																	#
#																							#
###=======================================================================================###

from tkinter import *
from tkinter import filedialog
import codecs
import os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import Script_Modules_8v08

directoryName=""

class App:
	
	def __init__(self, master):

		self.labelone = Label(master, text="Enter parameters below:")
		self.labelone.grid(row=0, column=1, sticky="w", pady=4)

		self.LabelIn = Label (master, text="Directory of XML files")
		self.LabelIn.grid(row=2, pady=4, sticky="e", padx=8)
		self.eIn = Entry(master,width=150)
		self.eIn.grid(row=2,column=1)
		self.ButtonDirIn = Button(master, text="Choose input directory", command = self.chooseDir_In, width = 20)
		self.ButtonDirIn.grid(row=3, column=1, sticky="w", pady=4)

		self.LabelOut = Label(master,text="Output Directory")
		self.LabelOut.grid(row=4, pady=4, sticky="e", padx=8)
		self.eOut = Entry(master,width=150)
		self.eOut.grid(row=4,column=1)
		self.ButtonDirOut = Button(master, text="Choose output directory", command = self.chooseDir_Out, width = 20)
		self.ButtonDirOut.grid(row=5, column=1, sticky="w", pady=4)

		self.LabelEdition = Label(master,text="Edition No.")
		self.LabelEdition.grid(row=6, pady=4, padx=8, sticky="e")
		self.eEdition = Entry(master,width=4)
		self.eEdition.grid(row=6,column=1,sticky="w")

		self.LabelLettr = Label (master, text="Letter")
		self.LabelLettr.grid(row=8, pady=4, padx=8, sticky="e")
		self.eLettr = Entry (master,width=4)
		self.eLettr.grid(row=8,column=1,sticky="w")

		self.ButtonStart = Button(master, text="Start Conversion", command = self.xml_Create, bg="#66CDAA", fg="black")
		self.ButtonStart.grid(row=100, column=1, sticky="w", pady=10, padx=0)
		self.ButtonQuit = Button(master, text="Exit", command = master.quit, bg="#B22222", fg="white", width = 10)
		self.ButtonQuit.grid(row=100, column=1, sticky="e", pady=10, padx=0)

	def collectParams(self):
		Dic= {'DicIn': '', 'DicOut': '', 'Edition': '', 'Letter':''} 
		Dic['DicIn'] = self.eIn.get()
		Dic['DicOut'] = self.eOut.get()
		Dic['Edition'] = self.eEdition.get()
		Dic['Letter'] = self.eLettr.get()
		return Dic

	def xml_Create(self):
		directoryIn = self.eIn.get()
		directoryOut = self.eOut.get()
		if directoryIn == "":
			print ("Choose an Input Directory")
		elif directoryOut =="":
			print ("Choose an Output Directory")
		else:

			self.ButtonStart.configure(bg = "red")
			Curr_Dict = self.collectParams()
			print (Curr_Dict)
			Script_Modules_8v08.analyze(Curr_Dict)

	def chooseDir_In(self):
		directoryName = filedialog.askdirectory()
		self.eIn.insert(100,directoryName)
	def chooseDir_Out(self):
		directoryName = filedialog.askdirectory()
		self.eOut.insert(100,directoryName)

root =Tk()
root.geometry("1060x268")
app = App(root)
root.title("TEI/XML Page-to-Entry Conversion Tool version 8.04  (Nineteenth-Century Knowledge Project)")
root.mainloop()
root.destroy()

if __name__ == '__main__':
	pass
