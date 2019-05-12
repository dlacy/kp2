###===========XML DATA CLEANING SCRIPT / ENCYCLOPEDIA PROJECT TEMPLE UNIVERSITY===========###
#																							#
# This script is based on version 5 of the script created by Luling Huang on				#
# Oct. 13, 2016 and is based on the last iteration of version 5 created on   				#
# May. 9, 2018.  It has been updated by Gary Scales. The script processes 					#
# footnotes with BeautifulSoup, refines footnote indexing, and gathers metainformation 		#
# from Excel inventory files. Two more Python libraries are needed: Pandas and xlrd.		#
#																							#
# Date Created: May 9, 2018																	#
# Created by: Luling Huang - luling.huang@temple.edu										#
# Date Modified: June 22, 2018																#
# Modified By: Gary Scales - gary.scales@temple.edu 										#
#																							#
# Script Version Number: 8.01																#
# Python Version Used: 3.6.2																#
#																							#
###=======================================================================================###
  
# ==================================IMPORT PYTHON MODULES================================== #

import os
import codecs
import re
from bs4 import BeautifulSoup 
from bs4 import SoupStrainer
import fileinput, glob, string, sys
from os.path import join
import pandas as pd
import xlrd
from pathlib import Path #ADDED JUNE 22 2018

# ============================ CREATE FUNCTION 'initializeVars' =========================== #
# CREATES DICTIONARY OF VARIABLES DEFINED BY USER VIA INTERFACE

def initializeVars (Dic):
    # LH: In the current version, user only needs to input four pieces of information (labeled with a # below), because the other information is matched from inventory files.
	global Entry_Edition #
	global Entry_Volume 
	global Entry_Letter #
	global Entry_PageStart 
	global Entry_PageEnd
	global Entry_PageStart2
	global Entry_PageEnd2
	global Entry_MultVolumes
	global FilesDirPath_Out #
	global FilesDirPath #
	global nameEntryStats
	
	Entry_Edition = "eb"+Dic['Edition']
	Entry_Letter = Dic['Letter']
	FilesDirPath_Out= Dic['DicOut']
	FilesDirPath = Dic['DicIn']
	nameEntryStats= Dic['DicOut']
	print (nameEntryStats)

# =================================== CREATE FUNCTION 'analyze' ================================= #
# COLLECTS FILES FOR PROCESSING FROM THE GIVEN DIRECTORY AND CALLS FUNCTIONS ON DATA WITHIN FILES

def analyze(paramDict):

	initializeVars(paramDict)
	
	files = [f for f in os.listdir(FilesDirPath) if os.path.isfile(os.path.join(FilesDirPath, f))] # Lists all files within specified directory
	files[:] = [x for x in files if '.DS_Store' not in x] # Addresses a potential mac file system problem
	files.sort() # Sorts files within specified directory
	
    # LH: This script assumes that the inventory file is at the path one level up from the TEI input files' path.
    # LH: See https://tu-plogan.github.io/#source/t_inventory_file.html
	onelvup = FilesDirPath.rsplit('/',1)[0]
	if onelvup == FilesDirPath:
		onelvup = FilesDirPath.rsplit('\\',1)[0]
	filesb = [f for f in os.listdir(onelvup) if os.path.isfile(os.path.join(onelvup, f))]
	ivtfile = [x for x in filesb if '.xlsx' in x][0]  # LH: Find inventory file
	ivtdf = pd.read_excel(os.path.join(onelvup, ivtfile))
	
	allPagesString =""
	for filename in files:

		print(filename)
		
		longfile= FilesDirPath+filename # Creates absolute path of given file
		
		# LH: Matches metainformation from inventory files and TEI page filenames.
		teifn = filename.split('.')[0]
		imgformat = ivtdf.columns[1].split('.')[1]
		sndcol = ivtdf.columns[1]
		Volume = ivtdf.loc[ivtdf['tei-fn.xml'] == teifn, 'p-vol'].iloc[0]
		batchNumb = filename.split('-')[1][-2:]
		pageNumber = ivtdf.loc[ivtdf['tei-fn.xml'] == teifn, 'p-pg'].iloc[0]
		imgfn = ivtdf.loc[ivtdf['tei-fn.xml'] == teifn, sndcol].iloc[0]
		
		data = codecs.open(os.path.join(FilesDirPath, filename), 'r', encoding='utf-8').read()								# Reads contents of given file
		page = newmoveNotes(data)
		soup = BeautifulSoup(page, "lxml-xml")																				# Collects and assembles all files into a single file

		invalid_tags = ['body', 'fileDesc', 'teiHeader', 'text', 'lb', 'TEI', 'titleStmt', 'title', 'author', 'publicationStmt', 'sourceDesc','p/']
		
		for tag in invalid_tags: 
			for match in soup.find_all(tag):
				match.unwrap()
		
		invalid_hi_tags = ['font0', 'font1', 'font2', 'font3', 'font4', 'font-weight: bold']
		for tag in invalid_hi_tags:
			for match in soup.find_all(rend = tag):
				match.unwrap()
		
		page = soup.prettify(formatter=None)

		page = cleanPage(page)																							# Runs the 'cleanPage' function on collected data (first cleaning pass)																								# Runs the 'moveNotes' function on collected data
		page = findEntry(page, pageNumber, batchNumb, Volume,imgfn,imgformat)																					# find the single entries and insert the correct tag for them
		allPagesString+='<pb xml:id="'+Entry_Edition+"-"+str(int(Volume))+"-"+Entry_Letter+batchNumb+"-"+'{:04d}'.format(pageNumber)+'" '+'facs="'+imgfn+'.'+imgformat+'"'+'/>\n'	# Inserts page break tag with entry information from user input
		allPagesString+=page																								# Adds page to string containing all pages
		allPagesString+="\n"																								# Adds newline to string containing all pages
		

	allPagesString =allPagesString.replace("</div>","",1)			# Deletes first occurrence of closed div tag
	allPagesString+="</div>\n"										# Adds closed div tag at the end of all pages
	allPagesString+="</body>\n"										# Adds/Closes file body tag
	numentries = parseInFiles(FilesDirPath_Out,allPagesString) 		# Runs the 'parseInFiles' function on processed data
	filelist = [f for f in os.listdir(FilesDirPath_Out) if os.path.isfile(os.path.join(FilesDirPath_Out, f))] # Creates file list of given directory for inserting into statistics file
	filelist.sort()
	EntriesStats(FilesDirPath_Out,filelist)
	removexmldec()													# Runs removexmldec function on new files to remove any extra XML declarations

# ============================= CREATE FUNCTION 'EntriesStats' ============================ #
# PRODUCES FILE CONTAINING STATISTICS OF FILES WHICH ARE BEING PROCESSED

def EntriesStats(Dir,filelist): 				# Creates statistics file
    EntryCounter=0								# Starts counter for files
    note = ""
    pagenumber ="0"
    for file in filelist:
        pageofEntry=re.search(r'\d{4,4}',file)	# Creates 4-digit page number
        if pageofEntry:
            pagenumber=pageofEntry.group(0)
            page= codecs.open(os.path.join(Dir, file), 'r', encoding='utf-8').read()
            EntryName= re.search(r'<label>.+?(</label>)',page)
            if EntryName:
                EntryCounter+=1
                if '<note ' in page:
                    note = "footnotes"
                else:
                    note = ""
                line = re.sub('<(/?)label>',"",EntryName.group(0))
                lineToAdd=('{:5}'.format(str(EntryCounter))
                            +'{:>15}'.format(file)
                            +'{:>40}'.format(line)
                            +'{:>5}'.format(pagenumber)
                            +'{:>20}'.format(note))
                with codecs.open(os.path.join(FilesDirPath_Out,"Entry_Stats.txt"),"a",encoding='utf8')as file:
                    file.write(lineToAdd+"\n")	# Writes information to file
    return filelist

# =============================== CREATE FUNCTION 'cleanPage' ============================= #
# REMOVES AND CLEANS UNWANTED TAGS, DIVISIONS, AND FORMATTING FROM FILES
# LH: Some unnecessary procedures were deleted.

def cleanPage(page): 

	page = re.sub("\s+"," ",page)									# Replaces any multiple spaces with a single space
	page = page.replace("<br clear=\"all\"/>","")					# Removes 'clear=all' break
	page = re.sub (r'<h\d>',"<p>",page)								# Creates new paragraph starting parameter
	page = re.sub (r'</h\d>',"</p>",page)							# Creates new paragraph ending parameter
	page = re.sub (r'\<{1}\/{1}\b(?:fileDesc)\b\>{1}',"", page)		# Removes opening fileDesc tag
	return page

# =============================== CREATE FUNCTION 'findentry' ============================= #
# SEARCHES FOR BEGINNING OF ENCYCLOPEDIA ENTRY USING REGULAR EXPRESSION SYNTAX
# MODIFIES THE DATA LINE INTO REQUIRED FORMAT

def findEntry(page,pageNumber,batchNumb,volNumb, imgfn,imgformat):
	Capital_Letter = Entry_Letter.upper()
#
#	IMPORTANT! -  
#	the subsequent regex parameter is the core of the script: it modifies the line where a entry is accordingly to the final xml format. 
#	It will eventually separated in different files. in a separate function 
#	The script searches for a "<p>" paragraph tag followed by a word or a 
#	sequence of words all in capital letters and a minimum of two letters each. 
#	The first word has to start with the letter gave as the letter of the batch. 
#	Odd characters or lowercase letters in the middle of the word 
#	worst case scenario in the first letter) could result in a truncated 
#	name of the entry or in a totally missing one.

	xmlheadnum1 = str(1)																	# Define '1' character for concatenation into target string
	xmlheadnum2 = str(0)																	# Define '0' character for concatenation into target string
	xmlheadnum3 = str(8)																	# Define '8' character for concatenation into target string
	xml_dec = 'xml version="'+xmlheadnum1+"."+xmlheadnum2+'"'+' encoding="utf-'+xmlheadnum3+'"?><'

	stringrule = (r'(?P<namesub>(<p>[\s]+?((\b['
					+str(Capital_Letter)
					+r'][A-Z,\u00c0-\u00DC,0-9\'\u02BC\u2019\u0100\u0102\u0104\u0106\u0108\u010A\u010C\u010E\u0112\u0114\u0116\u0118\u011A\u011C\u011E\u0120\u0122\u0124\u0128\u012A\u012C\u012E\u0130\u0134\u0136\u0139\u013B\u013D\u0141\u0143\u0145\u0147\u014C\u014E\u0150\u0152\u0154\u0156\u0158\u015A\u015C\u015E\u0160\u0162\u0164\u0168\u016A\u016C\u016E\u0170\u0172\u0174\u0176\u0178\u0179\u017B\u017D\u00C6\-]{1,}\b)|(['
					+str(Capital_Letter)
					+r'][A-Z,\u00c0-\u00DC,0-9\'\u02BC\u2019-]{1,}))[/,\s+]?((\b[A-Z,\u00c0-\u00DC\'\u02BC\u2019-]{1,}\b)?[,\s+]?)+))')  # LH: The regex now includes a hyphen or a apostrophe if in an entry name.
	regex_rule=re.compile(stringrule)														# Converts stringrule variable into object
	page = (re.sub(stringrule,"</div>"
					+"\n<?"+xml_dec+"div xmlns=\"http://www.tei-c.org/ns/1.0\" xml:id=\""
					+Entry_Edition
					+"-"
					+str(volNumb)
					+"-"
					+Entry_Letter
					+batchNumb
					+"-"
					+'{:04d}'.format(pageNumber)
					+"\" "
					+"facs=\""
					+imgfn
					+"."+imgformat+"\" "
					+"type=\"entry\">\n<label>\g<namesub></label>\n",page))
	page = re.sub(r'<label><p>',"<p><label>",page)
	
	return page

# =============================== CREATE FUNCTION 'movenotes' ============================= #
# LOCATES FOOTNOTE REFERENCES AND SPLITS BODY TEXT AT INSTANCES OF FOOTNOTE REFERENCES
# RELOCATES CORRESPONDING FOOTNOTE TEXT TO LOCATION OF BODY TEXT SPLIT
# SPLIT AND RELOCATION IS ACHIEVED USING SEQUENTIAL STRINGS OF '@' CHARACTERS

def cleanAnchor(page):  # LH: If a footnote anchor is within a <hi> tag, for example, take it out of <hi>.
    pattern = re.compile(r'(<hi\s*rend=\"\w*\">|<hi\s*style=\"\w*\">)([\w\s\|\.,\:\[\]\?\!;\"\"\'\@\#\$%\^\&\*\(\)\-\—\_\+\=\<\>\\\{\}~\`]*?[^\<\@])?(@{2,3}\s*)(\d{1,2}?\s*)?((\D.*?)*?)(<\/hi>)')
    page_reorderAnchor = pattern.sub(r'\1\2\7\3\1\5\7', page)
    emptyhi = re.compile(r'<hi\s*rend="\w*">\s*</hi>')
    page_reorderCleaned = emptyhi.sub('',page_reorderAnchor)
    return page_reorderCleaned

def moveNotesOP(page):  # LH: "OP" for footnotes at "one place"
    page = re.sub("\s+"," ",page)
    page = cleanAnchor(page)
    soup = BeautifulSoup(page, "lxml-xml")
    
    pattern1 = re.compile(r'^\s*@{3}\s*\d*(<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>)*')
    pattern2 = re.compile(r'@{2}\s*\d*(<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>)*')
    pattern3 = re.compile(r'\s*<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>\s*')
    
    
    atstrings = soup.find_all(string=pattern1)
    noteptags = [x.find_parent("p") for x in atstrings]
    
    afternotestr = ""
    for element in atstrings[-1].find_parent("p").next_siblings:
        elementstring = str(element)
        afternotestr = afternotestr + elementstring
    afternotestr = re.sub("<lb/>|</lb>","",afternotestr)
    
    beforenotestr = ""
    for element in atstrings[0].find_parent("p").previous_siblings:
        elementstring = str(element)
        beforenotestr = elementstring + beforenotestr
    
    allparntdivlist = atstrings[0].find_parent('p').find_parents('div')
    if len(allparntdivlist) > 0:
        divcount = len(allparntdivlist)
        leftdiv = '<div>' * divcount
        rightdiv = '</div>' * divcount
        leftdivhead = leftdiv + '<head>'
        for element in allparntdivlist[-1].previous_siblings:
            elementstring = str(element)
            beforenotestr = elementstring + beforenotestr
        if '<head>' in beforenotestr:
            beforenotestr = re.sub('<head>',leftdivhead,beforenotestr)
        afternotestr = afternotestr + rightdiv
        
    noteptagstrlist = []
    for index, ptag in enumerate(noteptags):
        ptagstr = ptag.prettify(formatter=None)
        ptagstr = re.sub("\s+"," ",ptagstr)
        ptagstr = re.sub("<p>|</p>","",ptagstr)
        ptagstr = re.sub(pattern1," ",ptagstr)
        ptagstr = re.sub(pattern3,"",ptagstr)
        ptagstr = '<note place = "bottom" anchored = "true" type = "authorial">' + ptagstr + '</note> '
        noteptagstrlist.append(ptagstr)
        
    bfnotestrblocks = re.split(pattern2,beforenotestr)
    bfnotestrblocks = [x for x in bfnotestrblocks if x is not None]
    bfnotestrblocks = [x for x in bfnotestrblocks if re.fullmatch(pattern3,x) is None]
    for index, x in enumerate(bfnotestrblocks):
        bfnotestrblocks[index] = re.sub(pattern3,"",bfnotestrblocks[index])
    
    bfnotewithnote = ""
    for index, block in enumerate(bfnotestrblocks[0:(len(bfnotestrblocks)-1)]):
        bfnotewithnote = bfnotewithnote + block + noteptagstrlist[index]
    bfnotewithnote = bfnotewithnote + bfnotestrblocks[-1]
    
    pagehead = re.split("<body>", page, 1)[0] + '<body>'
    pagetail = '</body>' + re.split("</body>", page, 1)[1]
    
    newpage = pagehead + bfnotewithnote + afternotestr + pagetail
    newpage = re.sub("\s+"," ",newpage)
    newpage = re.sub("&", "&amp;",newpage)
    return newpage

def newmoveNotes(page):  # LH: This one handles all patterns.
    page = re.sub("\s+"," ",page)
    page = cleanAnchor(page)
    soup = BeautifulSoup(page, "lxml-xml")
    onlyp = SoupStrainer(['p','head'])
    soupop = BeautifulSoup(page, "lxml-xml", parse_only=onlyp)
    ptextl = soupop.find_all(['p','head'])[2:(len(soupop.find_all(['p','head']))+1)]
    
    pattern1 = re.compile(r'^\s*@{3}\s*\d*(<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>)*')
    pattern2 = re.compile(r'@{2}\s*\d*(<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>)*')
    pattern3 = re.compile(r'\s*<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>\s*')
    
    checkfnl = []  # LH: Determines a footnote pattern for a tei page.
    for ptext in ptextl:
        if ptext.find(string=pattern1) is not None:
            checkfnl.append(1)
        else:
            checkfnl.append(0)
    
    if checkfnl.count(1) < 1:  # LH: No footnote moving needed
        page = re.sub("<lb/>|</lb>","",page)
        newpage = re.sub("&", "&amp;",page)
        return newpage
    elif checkfnl.count(1) == 1:
        newpage = moveNotesOP(page)  # LH: Executes moveNotesOP()
        return newpage
    elif 0 not in checkfnl[min(index for index, value in enumerate(checkfnl) if value == 1):(max(index for index, value in enumerate(checkfnl) if value == 1)+1)]:
        newpage = moveNotesOP(page)  # LH: Executes moveNotesOP()
        return newpage
    else:  # LH: Handles footnotes at two places
        firstfnindex = min(index for index, value in enumerate(checkfnl) if value == 1)
        lastfnindex = max(index for index, value in enumerate(checkfnl) if value == 1)
        
        oneindex = [index for index, value in enumerate(checkfnl) if value == 1]
        for x in oneindex:
            try:
                if checkfnl[x+1] == 0:
                    firstlastindex = x
            except IndexError:
                pass
            if checkfnl[x-1] == 0 and 0 not in checkfnl[x:]:
                secondfirstindex = x
        
        fsthalfptextl = ptextl[0:firstfnindex]
        sndhalfptextl = ptextl[(firstlastindex+1):secondfirstindex]
        
        if firstfnindex == firstlastindex:
            fsthalfpfnl = [ptextl[firstfnindex]]
        else:
            fsthalfpfnl = ptextl[firstfnindex:(firstlastindex+1)]
        if secondfirstindex == lastfnindex:
            sndhalfpfnl = [ptextl[lastfnindex]]
        else:
            sndhalfpfnl = ptextl[secondfirstindex:(lastfnindex+1)]
        
        fsthalfstrfnl = []
        for index, ptag in enumerate(fsthalfpfnl):
            ptagstr = ptag.prettify(formatter=None)
            ptagstr = re.sub("\s+"," ",ptagstr)
            ptagstr = re.sub("<p>|</p>","",ptagstr)
            ptagstr = re.sub(pattern1," ",ptagstr)
            ptagstr = re.sub(pattern3,"", ptagstr)
            ptagstr = '<note place = "bottom" anchored = "true" type = "authorial">' + ptagstr + '</note> '
            fsthalfstrfnl.append(ptagstr)
            
        sndhalfstrfnl = []
        sndhalffnstart = len(fsthalfpfnl) + 1
        for ptag in sndhalfpfnl:
            ptagstr = ptag.prettify(formatter=None)
            ptagstr = re.sub("\s+"," ",ptagstr)
            ptagstr = re.sub("<p>|</p>","",ptagstr)
            ptagstr = re.sub(pattern1," ",ptagstr)
            ptagstr = re.sub(pattern3,"", ptagstr)
            ptagstr = '<note place = "bottom" anchored = "true" type = "authorial">' + ptagstr + '</note> '
            sndhalfstrfnl.append(ptagstr)
            sndhalffnstart += 1
            
        fsthalfstrtext = " ".join(str(x) for x in fsthalfptextl)
        fsthalfstrtext = re.sub("\s+"," ",fsthalfstrtext)
        
        sndhalfstrtext = " ".join(str(x) for x in sndhalfptextl)
        sndhalfstrtext = re.sub("\s+"," ",sndhalfstrtext)
        

        fullstrtext = fsthalfstrtext + sndhalfstrtext
        fullstrtext = re.split(pattern2,fullstrtext)
        fullstrtext = [x for x in fullstrtext if x is not None]
        fullstrtext = [x for x in fullstrtext if re.fullmatch(pattern3,x) is None]
        for index, x in enumerate(fullstrtext):
            fullstrtext[index] = re.sub(pattern3,"",fullstrtext[index])
        fullstrfnl = fsthalfstrfnl + sndhalfstrfnl
        
        if soup.find('head') is not None:
            allparntdivl = soup.find('head').find_parents('div')
            if len(allparntdivl) > 0:
                divcount = len(allparntdivl)
                leftdiv = '<div>' * divcount
                rightdiv = '</div>' * divcount
                leftdivhead = leftdiv + '<head>'
                if '<head>' in fullstrfnl:
                    fullstrfnl = re.sub('<head>',leftdivhead,fullstrfnl)
                    fullstrfnl = fullstrfnl + rightdiv
        
        fulltxtwithnote = ""
        for index, block in enumerate(fullstrtext[0:(len(fullstrtext)-1)]):
            fulltxtwithnote = fulltxtwithnote + block + fullstrfnl[index]
        fulltxtwithnote = fulltxtwithnote + fullstrtext[-1]
            
        pagehead = re.split("<body>", page, 1)[0] + '<body>'
        pagetail = '</body>' + re.split("</body>", page, 1)[1]

        newpage = pagehead + fulltxtwithnote + pagetail
        newpage = re.sub("\s+"," ",newpage)
        newpage = re.sub("&", "&amp;",newpage)
        return newpage
        

# ============================== CREATE FUNCTION 'parseInFiles' =========================== #
# ISOLATES ENCYCLOPEDIA ENTRIES INTO DISCRETE XML ELEMENTS

def parseInFiles(dirPath,allPagesString):
	pageNumbStr =""
	entryCounter = 0
	PageEntryCounter = 1
	noteCounter = 1
	entryBreak = ['type="entry"','</body>']
	
	lines = allPagesString.split("\n")
	newEntryLines = []	# The list of all the lines of an entry
	oldEntryLines = []
	nameEntry = ""
	pageEntry = ""
	nameFile = ""
	
	for index,line in enumerate(lines):
		line = line.replace("</div>","\n</div>")
		line = re.sub("&", "&amp;",line)
		if ("<pb xml:id=" in line):	 # When it founds the pagecode grabs 
			CodeOfPage = line.split('"')[1]	 # the number of the page and put to zero the Counter of entries for the page
			reNumb = re.search(r'(\d){4}',CodeOfPage)
			if reNumb:
				pageNumbStr = reNumb.group(0)

			PageEntryCounter = 1
			hitNextEntry = False
						
		if any(x in line for x in entryBreak):												# If the line is the one that starts an entry
			if entryCounter == 0:															# First entry case
				nameFile = CodeOfPage+"-"+'{:02d}'.format(PageEntryCounter)              
				OldNameFile=nameFile
				
			else:																			# All the other entries cases
				OldNameFile = nameFile
				nameFile = CodeOfPage+"-"+'{:02d}'.format(PageEntryCounter)

				noteCounter = 1
				
			line = re.sub(r'xml:id=".+?"',"xml:id="+'"'+nameFile+'"',line)
			line = line+"\n"
			
			oldEntryLines = list(newEntryLines)
			newEntryLines[:] = []
			if entryCounter != 0:
				if len(oldEntryLines)>0:
					
					pageEntry = re.search(r'\d{4}',oldEntryLines[0])						#change the page parameter
					
					if pageEntry:
						page = str(pageEntry.group(0))
						
					else:
						page = "0000"
					
					allLines = "\n".join(oldEntryLines)
					allLines = re.sub(r'</p><p>','</p>\n<p>',allLines)
					
					writeEntry(dirPath,OldNameFile,allLines)
					
			PageEntryCounter += 1 
			entryCounter += 1
			newEntryLines.append(line)
			hitNextEntry = True  # LH: To be used to determine whether the footnote index at the entry level should be reset.
		else:
			if "<label>" in line:
				line = line.replace("<label>","")
				line = line.replace("</label>","")
				line = line.replace("<p>","")
				line = line.strip(" ")
				line = line.strip(",")
				line = line.replace("1","I")
				line = line.replace("0","O")
				line = line.replace("/",",")
				line = "<p><label>"+line+"</label>"
				
			if '<note ' in line:
				parts = re.split(r'(<note .+?/note>)',line)
				if hitNextEntry == True:  # LH: If the found footnote is from a new entry, reset the footnote index.
				    noteCounter = 1
				newlist=[]
				if parts!=None:
					for part in parts:
						if '<note ' in part:
							part = re.sub(r'<note anchored="true" place="bottom" type="authorial">','<note anchored="true" place="bottom" type="authorial"' + ' n="' + str(noteCounter) + '">', part)
							newlist.append(part)
							noteCounter += 1
						else:
							newlist.append(part)

				line="".join(newlist)

			if line!="\n": 
				newEntryLines.append(line)       
	return entryCounter

# =============================== CREATE FUNCTION 'writeEntry' ============================ #
# WRITES ALL SEPERATE FILES INTO A SINGLE FILE CONTAINING ALL PROCESSED AND CREATED FILES
	
def writeEntry(Dir,Name,lineslist): 														#this function writes the single entry in a file
	nameFilex = Name+".xml"
	separator = ""
	allEntry= separator.join(lineslist)

	with codecs.open(os.path.join(Dir,nameFilex),"w",encoding='utf8') as entryFile:
		entryFile.write(allEntry)
																							#print (nameFilex)

def rreplace(s,old,new,occurrence):
	li = s.rsplit(old,occurrence)
	return new.join(li)

	if __name__ == "__main__":
		main()

# =============================== CREATE FUNCTION 'removexmldec' ============================ #
# READS CREATED FILES AND REMOVES ANY EXTRA XML DECLARATIONS WITHIN TEXT BODY
# ALSO REMOVES EXTRA TEI DOM TAGS AND CLOSES ANY TAGS LEFT OPEN FROM THESE OPERATIONS

def removexmldec():

# set directory path to match directory containing processed files

	os.chdir(os.path.abspath(FilesDirPath_Out)) 											# Change working directory to directory containing newly created XML files
	setdirectory = os.getcwd()
	print(setdirectory)

	xmldecnum1 = str(1)																		# Define '1' character for concatenation into target string
	xmldecnum2 = str(0)																		# Define '0' character for concatenation into target string
	xmldecnum3 = str(8)																		# Define '8' character for concatenation into target string
	xmldecnum4 = str(3)																		# Define '3' character for concatenation into target string
	xmldecnum5 = str(9)																		# Define '9' character for concatenation into target string

	xml_extraDTD = '<?xml version="'+xmldecnum1+"."+xmldecnum2+'"'+' encoding="utf-'+xmldecnum3+'"?> <p/> <p> translated from HTML to TEI </p> '			# Concatenate text and variables into first target string
	xml_extraDTD_remove = ""																																# Create variable to replace first target string

	xml_decl = '<?xml version="'+xmldecnum1+"."+xmldecnum2+'"'+' encoding="utf-'+xmldecnum3+'"?> <p/> <p> transformed from HTML to TEI by eb-html2tei </p> '			# Concatenate text and variables into second target string
	xml_dec_remove = ""																																					# Create variable to replace second target string
	
	xml_declare2 = '<?xml version="'+xmldecnum1+"."+xmldecnum2+'"'+' encoding="utf-'+xmldecnum3+'"?><TEI xmlns="http://www.tei-c.org/ns/'+xmldecnum1+'.'+xmldecnum2+'" xmlns:html="http://www.w'+xmldecnum4+'.org/'+xmldecnum1+xmldecnum5+xmldecnum5+xmldecnum5+'/xhtml"><teiHeader><fileDesc><titleStmt><title/><author/></titleStmt><publicationStmt><p/>         </publicationStmt><sourceDesc><p>TEI-page files converted by Python to TEI-entry file</p></sourceDesc></fileDesc></teiHeader><text><body> <p/> '																									# Concatenate text and variables into third target string
	xml_dec_remove_2 = ""																																				# Create variable to replace third target string

	xml_divend = '</div>'																	# Create variable for fourth target string
	xml_end_file = '</div></body></text></TEI>'												# Create variable to replace fourth target string

	xml_init_begin_file = '<div xmlns='														# Create variable for fifth target string
	xml_TEI_begin_file = '<TEI xmlns="http://www.tei-c.org/ns/'+xmldecnum1+'.'+xmldecnum2+'" xmlns:html="http://www.w'+xmldecnum4+'.org/'+xmldecnum1+xmldecnum5+xmldecnum5+xmldecnum5+'/xhtml"><teiHeader><fileDesc><titleStmt><title/><author/></titleStmt><publicationStmt><p/></publicationStmt><sourceDesc><p>TEI-page files converted by Python to TEI-entry file</p></sourceDesc></fileDesc></teiHeader><text><body><div xmlns='						# Concatenate text and variables to replace fifth target string

	hitag_leadspace_parent = '( <hi'														# Create variable for sixth target string
	hitag_leadspace_replace = '(<hi'														# Create variable to replace sixth target string

	for file in glob.glob('*.xml'):															# Declare operation as applicable to XML files only - avoids involvement with "Entry_Stats" file
		with open(file, 'r', encoding='utf-8') as f:										# Open all newly created XML files
		  filedata = f.read()																# Read all newly created XML files

		filedata = filedata.replace(xml_extraDTD, xml_extraDTD_remove)						# Replace the first target string with replacement variable
		filedata = filedata.replace(xml_decl, xml_dec_remove)								# Replace the second target string with replacement variable
		filedata = filedata.replace(xml_declare2, xml_dec_remove_2)							# Replace the third target string with replacement variable
		filedata = filedata.replace(xml_divend, xml_end_file)								# Replace the fourth target string with replacement variable
		filedata = filedata.replace(xml_init_begin_file, xml_TEI_begin_file)				# Replace the fifth target string with replacement variable
		filedata = re.sub("\s*<p>\s*","<p>",filedata)										# Remove remaining whitespace around opening paragraph tags
		filedata = re.sub("\s*</p>\s*","</p>",filedata)										# Remove remaining whitespace around closing paragraph tags
		filedata = re.sub("\s+<note","<note",filedata)										# Remove whitespace preceding opening note tags
		filedata = re.sub("(?<=</note>)\s(?=-|!|;|:|,|\)|\]|}|-|\.)","",filedata)			# Remove whitespace following closing note tag if next character is not a letter or opening parenthesis
		filedata = re.sub("(?<=<hi rend=\"italic\">)\s+|(?<=<hi rend=\"smallcaps\">)\s+|(?<=<hi rend=\"strikethrough\">)\s+|(?<=<hi rend=\"sub\">)\s+|(?<=<hi rend=\"sup\">)\s+|(?<=<hi rend=\"underline\">)\s+|(?<=<hi rend=\"italic\"/>)\s+|(?<=<hi rend=\"smallcaps\"/>)\s+|(?<=<hi rend=\"strikethrough\"/>)\s+|(?<=<hi rend=\"sub\"/>)\s+|(?<=<hi rend=\"sup\"/>)\s+|(?<=<hi rend=\"underline\"/>)\s+","",filedata)
																							# Remove remaining whitespace following opening hi tags
		filedata = re.sub("\s(?=</hi>)","",filedata)										# Remove remaining whitespace preceding closing hi tags
		filedata = re.sub("(?<=</hi>)\s(?=-|!|;|:|,|\]|}|-|\)|\.)","",filedata)				# Remove whitespace following a closing hi tag if next character is not a letter, digit, or opening parenthesis
		filedata = re.sub("</label>\s","</label>, ",filedata)								# Removes and/or replaces comma following entry title
		filedata = filedata.replace(hitag_leadspace_parent, hitag_leadspace_replace)		# Replace the sixth target string with replacement variable

		with open(file, 'w', encoding='utf-8') as f:										# Open all newly edited XML files
		  f.write(filedata)																	# Permanently write all newly created XML files without extra XML declaration
