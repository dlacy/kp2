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
# Script Version Number: 8.07																#
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
import string #ADDED SEPTEMBER 19 2018

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

#		invalid_tags = ['body', 'fileDesc', 'teiHeader', 'text', 'lb', 'TEI', 'titleStmt', 'title', 'author', 'publicationStmt', 'sourceDesc','p/']  
		invalid_tags = ['body', 'fileDesc', 'teiHeader', 'text', 'lb', 'TEI', 'titleStmt', 'title', 'author', 'publicationStmt', 'sourceDesc', 'revisionDesc', 'p/']  # add revisionDesc 4/20/19 /pl

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
	removexmldec()													# Runs removexmldec function on new files to remove any extra XML declarations
	EntriesStats(FilesDirPath_Out,filelist)							# Jan. 31, 2019: Run removexmldec() first, then run EntriesStats().
	print('One batch of TEI pages done.')

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
            label_tag = BeautifulSoup(page,'lxml-xml',parse_only=SoupStrainer('label')).label  # Use BS to retrieve entry name (Jan 31 2019)
            EntryName = label_tag.get_text().strip() # Use BS to retrieve entry name (Jan 31 2019)
			#EntryName= re.search(r'<label>.+?(</label>)',page) (Jan 31 2019)
            if EntryName:
                EntryCounter+=1
                if '<note ' in page:
                    note = "footnote(s)"
                else:
                    note = ""
                line = EntryName
				#line = re.sub('<(/?)label>',"",EntryName.group(0)) (Jan 31 2019)
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
#	the subsequent regex parameter is the core of the script: it modifies the line where an entry is according to the final xml format. 
#	It will eventually separated in different files. in a separate function 
#	The script searches for a "<p>" paragraph tag followed by a word or a 
#	sequence of words all in capital letters and a minimum of two letters each. 
#	The first word has to start with the letter given as the letter of the batch. 
#	Odd characters or lowercase letters in the middle of the word 
#	(or worst case scenario in the first letter) could result in a truncated 
#	name of the entry or in a totally missing one.

	xmlheadnum1 = str(1)																	# Define '1' character for concatenation into target string
	xmlheadnum2 = str(0)																	# Define '0' character for concatenation into target string
	xmlheadnum3 = str(8)																	# Define '8' character for concatenation into target string
	xml_dec = 'xml version="'+xmlheadnum1+"."+xmlheadnum2+'"'+' encoding="utf-'+xmlheadnum3+'"?><'

	stringrule = (r'(?P<namesub>(<p>[\s]+?((\b['
					+str(Capital_Letter)
					+r'][A-Z,\u00c0-\u00DC,0-9\'\u02BC\u2019\u0100\u0102\u0104\u0106\u0108\u010A\u010C\u010E\u0112\u0114\u0116\u0118\u011A\u011C\u011E\u0120\u0122\u0124\u0128\u012A\u012C\u012E\u0130\u0134\u0136\u0139\u013B\u013D\u0141\u0143\u0145\u0147\u014C\u014E\u0150\u0152\u0154\u0156\u0158\u015A\u015C\u015E\u0160\u0162\u0164\u0168\u016A\u016C\u016E\u0170\u0172\u0174\u0176\u0178\u0179\u017B\u017D\u00C6\-]{1,}\b)|(['
					+str(Capital_Letter)
					+r'][A-Z,\u00c0-\u00DC,0-9\'\u02BC\u2019-]{1,}))[/,\s+]?((\b[A-Z,\u00c0-\u00DC\'\u02BC\u2019-]{1,}\b)?[,\s+]?)+))')  # LH: The regex now includes a hyphen or an apostrophe if in an entry name.
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

def newmoveNotes(page):  # LH: This one handles all patterns.
    page = re.sub("\s+"," ",page)
    page = cleanAnchor(page)
    soup =  (page, "lxml-xml")
    onlyp = SoupStrainer(['p','head','table'])
    soupop = BeautifulSoup(page, "lxml-xml", parse_only=onlyp)
    ptextl = soupop.find_all(['p','head','table'])[2:(len(soupop.find_all(['p','head','table']))+1)]
    
    pattern1 = re.compile(r'^\s*@{3}\s*\d*(<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>)*')
    pattern2 = re.compile(r'@{2}\s*\d*(<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>)*')
    pattern3 = re.compile(r'\s*<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>\s*')
    pattern4 = re.compile(r'<p>\s*@{3}\s*\d*(<hi\s*rend=\"\w*\">\s*\d{1,2}\s*<\/hi>)*')
    
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
    else:
        fn_start_ind = []
        for i, x in enumerate(checkfnl):
            if x == 1:
                fn_start_ind.append(i)
        fst_fn_idx = fn_start_ind[0]

        main_txt_str = " ".join(str(x) for x in ptextl[0:fst_fn_idx])
        
        fn_p_l = []
        if len(fn_start_ind) == 1:
            fn_p_l.append(ptextl[fst_fn_idx:])
        else:
            for i, x in enumerate(fn_start_ind):
                try:
                    next_x = fn_start_ind[i+1]
                except IndexError:
                    fn_p_l.append(ptextl[x:])
                    continue
                if next_x - x == 1:
                    fn_p_l.append(ptextl[x])
                else:
                    fn_p_l.append(ptextl[x:next_x])
        
        fn_str_l = []
        for fn_p in fn_p_l:
            if type(fn_p) == list:
                fn_str = " ".join(str(x) for x in fn_p)
            else:
                fn_str = fn_p.prettify(formatter=None)    
            fn_str = re.sub("\s+"," ",fn_str)
            #fn_str = re.sub("<p>|</p>","",fn_str)
            fn_str = re.sub(pattern4,"<p>",fn_str)
            fn_str = re.sub(pattern3,"", fn_str)
            fn_str = '<note place = "bottom" anchored = "true" type = "authorial">' + fn_str + '</note> '
            fn_str_l.append(fn_str)
        
        main_txt_str = re.split(pattern2,main_txt_str)
        main_txt_str = [x for x in main_txt_str if x is not None]
        main_txt_str = [x for x in main_txt_str if re.fullmatch(pattern3,x) is None]
        for x in main_txt_str:
            x = re.sub(pattern3,"",x)
        full_txt_with_note = ""
        for index, block in enumerate(main_txt_str[0:(len(main_txt_str)-1)]):
            full_txt_with_note = full_txt_with_note + block + fn_str_l[index]
        full_txt_with_note = full_txt_with_note + main_txt_str[-1]
            
        pagehead = re.split("<body>", page, 1)[0] + '<body>'
        pagetail = '</body>' + re.split("</body>", page, 1)[1]

        newpage = pagehead + full_txt_with_note + pagetail
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
		if ("<pb xml:id=" in line):	 # When it finds the pagecode grabs 
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
			# if "<label>" in line:
				# line = line.replace("<label>","")
				# line = line.replace("</label>","")
				# line = line.replace("<p>","")
				# line = line.strip(" ")
				# line = line.replace("1","I")
				# line = line.replace("0","O")
				# line = line.replace("/",",")
				# if line[-1] in string.punctuation:
				    # line = "<p><label>"+line[0:len(line)-1]+"</label>"+line[-1]
				# else:    
				    # line = "<p><label>"+line+"</label>"
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
	xml_TEI_begin_file = '<TEI xmlns="http://www.tei-c.org/ns/'+xmldecnum1+'.'+xmldecnum2+'" xmlns:html="http://www.w'+xmldecnum4+'.org/'+xmldecnum1+xmldecnum5+xmldecnum5+xmldecnum5+'/xhtml"><teiHeader><fileDesc><titleStmt><title/><author/></titleStmt><publicationStmt><p/></publicationStmt><sourceDesc><p>TEI-page files converted by Python to TEI-entry file v8.07</p></sourceDesc></fileDesc></teiHeader><text><body><div xmlns='						# Concatenate text and variables to replace fifth target string

	hitag_leadspace_parent = '( <hi'														# Create variable for sixth target string
	hitag_leadspace_replace = '(<hi'														# Create variable to replace sixth target string

	#====== Section below added January 24 2019 to remove unwanted docx conversion DTD =====#

	docxDTDdigitone = str(2)																# Define '8' character for concatenation into target string
	docxDTDdigittwo = str(15)																# Define '2' character for concatenation into target string
	# docxDTDdigitthree = str(5)																# Define '5' character for concatenation into target string

	# docx_target_DTD_one = '<label><?xml version="I.O" encoding="utf-'+docxDTDdigitone+'"?> unknown title unknown author <editionStmt> <edition> <date> unknown date <,date> <,edition> <,editionStmt>  unknown <,p>  Converted from a Word document with eb-docx'+docxDTDdigittwo+'tei. <,p> <encodingDesc> <appInfo> <application ident="TEI_fromDOCX" version="'+docxDTDdigittwo+'.I'+docxDTDdigitthree+'.O" xml:id="docxtotei">  Knowledge Project: DOCX to TEI  <,application> <,appInfo> <,encodingDesc> <revisionDesc> <listChange> <change> '		# Concatenate text and variables into target string 
	docx_target_DTD_one = '<?xml version="'+xmldecnum1+'.'+xmldecnum2+'" encoding="utf-'+xmldecnum3+'"?> unknown title unknown author <editionStmt> <edition> <date> unknown date </date> </edition> </editionStmt><p>unknown</p><p>Converted from a Word document with eb-docx'+docxDTDdigitone+'tei.</p><encodingDesc> <appInfo> <application ident="TEI_fromDOCX" version="'+docxDTDdigitone+'.'+docxDTDdigittwo+'.'+xmldecnum2+'" xml:id="docxtotei"> <label> Knowledge Project: DOCX to TEI </label> </application> </appInfo> </encodingDesc> <revisionDesc> <listChange> <change> '

	docx_target_DTD_two = r' <name> unknown author </name> </change> </listChange> </revisionDesc>(<p>)?'	# Concatenate text and variables into target string

	unwanted_label_tag_pattern = '<,p></label>'												# Define unwanted label pattern
	corrected_unwanted_label_tag_pattern = '<,p>'											# Define corrected label pattern

	damaged_p_tag = '<,p>'																	# Define damaged p tag
	damaged_hi_tag = '<,hi>'																# Define damaged hi tag
	repaired_p_tag = '</p><p>'																# Define repaired p tag
	repaired_hi_tag = '</hi>'																# Define repaired hi tag

	damaged_p_tag_v2 = '<,p</label>>'														# Define concatenated p and label tags
	damaged_end_div_tag = '<,div</label>>'													# Define concatenated div and label tags
	repaired_p_tag_v2 = '</p>'																# Define substitute for concatenated p and label tags
	repaired_end_div_tag = '<,div></label>'													# Define substitute for concatenated div and label tags

	unwanted_end_tags_pattern = '<,div></label>'											# Define pattern of unwanted tags at the end of the file
	empty = ''																				# Define empty variable
	xml_eof = '</div></body></text></TEI>'													# Define tag pattern for end of file

	#====== Section above added January 24 2019 to remove unwanted docx conversion DTD =====#

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
		#filedata = re.sub("</label>\s","</label>, ",filedata)								# Removes and/or replaces comma following entry title
		filedata = filedata.replace(docx_target_DTD_one, empty)								# Remove first section of unwanted DTD (Jan 24 2019)
		#filedata = filedata.replace(docx_target_DTD_two, empty)								# Remove second section of unwanted DTD (Jan 24 2019)
		filedata = re.sub(docx_target_DTD_two,empty,filedata)
		filedata = filedata.replace(damaged_p_tag_v2, repaired_p_tag_v2)					# Repair concatenated p and label tags (Jan 24 2019)
		filedata = filedata.replace(damaged_end_div_tag, repaired_end_div_tag)				# Repair concatenated div and label tags  (Jan 24 2019)
		filedata = filedata.replace(unwanted_label_tag_pattern, corrected_unwanted_label_tag_pattern)					# Repair unwanted "label" tags (Jan 24 2019)
		filedata = re.sub(r'<date>\s[0-9]{4}-[0-9]{2}-[0-9]{2}[A-Za-z]{1}[0-9]{2}:[0-9]{2}:[0-9]{2}[A-Za-z]{1}\s<\/date>','',filedata)				# Remove unwanted DTD date stamp (Jan 24 2019)
		filedata = re.sub(r'</p>\s{0,}<pb\s{1}xml:id','<pb xml:id',filedata)				# Remove unwanted </p> tags before image record declaration (Jan 24 2019)
		filedata = re.sub(r'jp2\"/>\s{0,}<p>','jp2"/>',filedata)							# Remove unwanted <p> tags following image record declaration (Jan 24 2019)
		filedata = filedata.replace(damaged_p_tag, repaired_p_tag)							# Repair damaged "p" tags (Jan 24 2019)
		filedata = filedata.replace(damaged_hi_tag, repaired_hi_tag)						# Repair damaged "hi" tags (Jan 24 2019)
		filedata = filedata.replace(unwanted_end_tags_pattern, xml_eof)						# Repair ending tags sequence (Jan 24 2019)
		filedata = re.sub(r'<p>\s\n<\/div>','</div>',filedata)								# Remove extra p tag from ending tags sequence (Jan 24 2019)
		filedata = filedata.replace(hitag_leadspace_parent, hitag_leadspace_replace)		# Replace the sixth target string with replacement variable

		#################### Jan. 31, 2019: If a smallcap <hi> immediately follows the <label>, insert <hi> into <label>.
		
		space_before_closing_label = re.search(r'\s+</label>',filedata)
		if not space_before_closing_label:
			filedata = re.sub('</label>',' </label>',filedata)

		soup = BeautifulSoup(filedata,'lxml-xml')
		label = soup.find('label')
		try:
			if label.nextSibling == '\n' and label.nextSibling.nextSibling.name == 'hi':
				if label.nextSibling.nextSibling.get('rend') == 'smallcaps':
					target_hi = label.nextSibling.nextSibling
					label.append(target_hi)
			else:
				pass
		except AttributeError:
			pass
		
		filedata = str(soup)

		space_after_opening_label = re.search(r'<label>\s+',filedata)
		space_before_closing_label = re.search(r'\s+</label>',filedata)
		if space_after_opening_label:
			filedata = re.sub(space_after_opening_label.group(0), '<label>',filedata)
		if space_before_closing_label:
			filedata = re.sub(space_before_closing_label.group(0), '</label>',filedata)
		##################### Jan. 31, 2019 ##################################################
		
		##################### Apr. 8, 2019 ##################################################
		'''
		This block deals with two problems:
		(1) In a <label> tag, if there is any trailing punctuation, remove the punctuation out of <label>
		(2) Remove the redundant "amp;" following a "&amp;"  
		'''
		pattern_label = re.compile(r'(<label>)(\w+\-?\w+)([\|\.,\:\[\]\?\!;\"\"\'\@\#\$%\^\&\*\(\)\-\—\_\+\=\<\>\\\{\}~\`]*)(</label>)')
		filedata = pattern_label.sub(r'\1\2\4\3', filedata)
		filedata = re.sub("&amp;amp;","&amp;",filedata)
		bad_end = re.search("</p></text></TEI>",filedata)
		if bad_end:
			filedata = re.sub("</div>","",filedata)
			filedata = re.sub("</body>","",filedata)
			filedata = re.sub("</p></text></TEI>","</p></div></body></text></TEI>",filedata)
		##################### Apr. 8, 2019 ##################################################

		with open(file, 'w', encoding='utf-8') as f:										# Open all newly edited XML files
			f.write(filedata)																	# Permanently write all newly created XML files without extra XML declaration