#============= OCR LONG-S BASIC CORRECTION TOOL / EB PROJECT TEMPLE UNIVERSITY =============#
#                                                                                           #
# This script makes basic corrections to the XML/TEI Files containing OCR data which        #
# includes the "long-s" (ſ).                                                                #
#                                                                                           #
# It first creates custom dictionaries by parsing the input data. Three dictionaries are    #
# created: two for word pairs (one pair where the word containing the long-s is the first,  #
# and the other where it is the second), and one for single word substitutions. These are   #
# exported as text (.txt) files with word pairs separated by new lines.                     #
#                                                                                           #
# Once these dictionaries have been created, the script tests the content of each           #
# XML/TEI files against the dictionaries (replacing word pairs first, then single word      #
# substitutions) to correct any words containing a long-s while protecting syntax, idiom,   #
# style, and context as much as possible.                                                   #
#                                                                                           #
# It should be noted while all code is original, the design is loosely based upon           #
# the OCR-Normalizer developed by Ted Underwood who has credit for identifying word pairing #
# as the optimal form of automated text error correction. The design also loosely           #
# replicates the "training/learn" function of ABBYY FineReader allow the user to tailor the #
# dictionaries after they have been updated by the script.                                  #
#                                                                                           #
# Date Created: July, 13 2018                                                               #
# Created by: Gary Scales - gary.scales@temple.edu                                          #
# Date Modified: February, 14 2019                                                          #
# Modified By: Gary Scales - gary.scales@temple.edu                                         #
#                                                                                           #
# Script Version Number: 9.4.0                                                              #
# Python Version Used: 3.7.0                                                                #
#                                                                                           #
#===========================================================================================#

'''#######################################################################################'''
'''.......................................................................................'''
'''..........SETUP PHASE OF PROGRAM.  >  OBTAIN INPUT DATA AND SET USER VARIABLES.........'''
'''.......................................................................................'''
'''#######################################################################################'''

# ===================================== IMPORT MODULES =====================================#
# Imports necessary Python modules

import os
import codecs
import tkinter
import re
import fileinput
import glob
import string
import sys
import copy
import hashlib
from bs4 import BeautifulSoup

def main():

    # =============================== CREATE FUNCTION 'interface' ============================= #
    # Creates dictionary of variables defined by user interface
    #---------> FUNCTION WORKING - CAN BE UNCOMMENTED ONCE SCRIPT COMPLETE AND GUI IS ASSIGNED
    # def interface(Dic):                                                                    # declare function name and arguments
        # global origin_root
        # global write_directory
        # origin_root = Dic['directoryIn']
        # write_directory = Dic['directoryOut']
        # global origin_root
        # global write_directory
        #return origin_root, write_directory

    # ================================ CHECK CURRENT DIRECTORY ================================ #
    # Sets current working directory

    cwd = os.getcwd()                                                                           # check location of current working directory and declare it as a variable
    # print(cwd)                                                                                # !print command used for visual check during development only

    # ================================ CREATE FUNCTION 'prompt' =============================== #
    # This function creates raw input prompts for storing variables provided by the user

    # def prompt(promptstring, options):                                                          # declare function name and arguments
        # user = input(promptstring)                                                              # set "user" variable
        # if user not in options:                                                                 # create loop for user input
            # user = prompt(promptstring, options)                                                # define "user" variable
        # return user                                                                             # return variable

    # =================================== REQUEST USER INPUT ================================== # this will be replaced with a GUI once the program is confirmed as operational.

    print("****************** CLEaN-CL Version 10.1.2 ******************")                 # print header line for user input prompt
    origin_root = input("Path to the folder that contains source files: ")                      # request directory of input files
    write_directory = input("Path to the folder for the new (cleaned) files: ")                 # request directory of output files

    # ================================ CREATE FUNCTION 'FILEGET' ============================== #
    # This function looks into the given XML/TEI file, retrieves all content inside the "body"
    # tag, and stores it as a variable for subsequent phases of the program. DOM/tag structure
    # is maintained throughout process

    os.chdir(origin_root)                                                                               # change working directory to user specified directory for input files
    for prefile in os.listdir():                                                                        # create loop for iteration through files
        filename = os.fsdecode(prefile)                                                                 # fsdecode to escape expected bytes format of directory in Python version 3.6 and later 
        if filename.endswith(".xml"):                                                                   # create loop for iteration through xml files only (precludes processing of "entry_stats" file)
            # print(prefile)                                                                            # display file name to indicate progress during processing of files
            livefile = open(prefile,'r+',encoding="utf-8-sig").read()                                   # create variable for beautiful soup operations
            # print(livefile)                                                                           # !print command used for visual check during development only
            soup = BeautifulSoup(livefile, 'xml')                                                       # create beautiful soup object and parse as XML
            soup.prettify()                                                                             # read whole DOM of file
            # print(soup)                                                                               # !print command used for visual check during development only
            divcapture = soup.find_all("body")                                                          # find all data inside the <body> tag of file
            for text in soup:                                                                           # create loop for iteration through contents of <body> tag of file
                global text_harvest                                                                     # declare global variable
                text_harvest = text                                                                     # switch variable name
                text_harvest = re.sub("</p>", " </p>", str(text_harvest))                               # add space before any closing </p> tags to enable regex to correctly identify white space in word pairs
                # print(text_harvest)                                                                   # !print command used for visual check during development only
                text_alpha = text_harvest                                                               # switch variable name (for easy identification in subsequent code blocks)

            '''#######################################################################################'''
            '''.......................................................................................'''
            '''...............HARVEST PHASE OF PROGRAM.  >  BUILD AND APPEND DICTIONARIES.............'''
            '''.......................................................................................'''
            '''#######################################################################################'''

            # ======================== CREATE FUNCTION 'BUILD_WORD_PAIR_DICTS' ======================== #
            # function creates dynamic dictionaries from input files

            matches_leading = re.finditer(r"[a-zA-Zſ\’\'?-]*ſ[a-zA-Zſ\’\'?-]*\W+\w+|[a-zA-Zſ\’\'?-]+?ſ[a-zA-Zſ\’\'?-]+?\W+\w+", 
            str(text_harvest), re.MULTILINE)                                                            # find word pairs where leading word contains a long-s

            precede_leadwords=[]                                                                        # create empty list for leading words in identified word pairs
            precede_trailwords=[]                                                                       # create empty list for trailing words in identified word pairs

            for matchNum_one, match in enumerate(matches_leading):                                      # create loop for iteration through text
                matchNum_one = matchNum_one + 1                                                         # create counter increment by one per parse
                pair_precede_list = [match.group()]                                                     # create temporary list of identified pairs
                precede_token_word_lead = [i.split()[0] for i in pair_precede_list]                     # detach leading words from list of identified pairs
                precede_leadwords.extend(precede_token_word_lead)                                       # populate list of preceding words
                # print(precede_token_word_lead)                                                        # !print command used for visual check during development only
                try:
                    precede_token_word_trail = [i.split()[1] for i in pair_precede_list]                # detach trailing words from list of identified pairs
                except IndexError:
                    precede_token_word_trail = "[PAIRING ERROR]"
                pass
                precede_trailwords.extend(precede_token_word_trail)                                     # populate list of trailing words
                # print(precede_token_word_trail)                                                       # !print command used for visual check during development only
                # print(precede_leadwords)                                                              # !print command used for visual check during development only
                # print(precede_trailwords)                                                             # !print command used for visual check during development only

            concat_lead_dict = dict(zip(precede_leadwords, precede_trailwords))                         # create "word before" dictionary using leading words as keys and trailing words as values
            # print(concat_lead_dict)                                                                   # !print command used for visual check during development only

            matches_trailing = re.finditer(r"\w+\W+[a-zA-Zſ\’\'?-]*ſ[a-zA-Zſ\’\'?-]*|\w+\W+[a-zA-Zſ\’\'?-]+?ſ[a-zA-Zſ\’\'?-]+?", str(text_harvest), re.MULTILINE)# find word pairs where following word contains a long-s

            follow_leadwords=[]                                                                         # create empty list for leading words in identified word pairs
            follow_trailwords=[]                                                                        # create empty list for trailing words in identified word pairs

            for matchNum_one, match in enumerate(matches_trailing):                                     # create loop for iteration through text
                matchNum_one = matchNum_one + 1                                                         # create counter increment by one per parse
                pair_follow_list = [match.group()]                                                      # create temporary list of identified pairs
                follow_token_word_lead = [i.split()[0] for i in pair_follow_list]                       # detach leading words from list of identified pairs
                follow_leadwords.extend(follow_token_word_lead)                                         # populate list of preceding words
                # print(follow_token_word_lead)                                                         # !print command used for visual check during development only
                try:
                    follow_token_word_trail = [i.split()[1] for i in pair_follow_list]                      # detach trailing words from list of identified pairs
                except IndexError:
                    follow_token_word_trail = "[PAIRING ERROR]"
                pass
                follow_trailwords.extend(follow_token_word_trail)                                       # populate list of trailing words
                # print(follow_token_word_trail)                                                        # !print command used for visual check during development only
                # print(follow_leadwords)                                                               # !print command used for visual check during development only
                # print(follow_trailwords)                                                              # !print command used for visual check during development only

            concat_follow_dict = dict(zip(follow_leadwords, follow_trailwords))                         # create "word after" dictionary using leading words as keys and trailing words as values
            # print(concat_follow_dict)                                                                 # !print command used for visual check during development only

            # ======================= CREATE FUNCTION 'WRITE_LEAD_WORD_PAIR_FILE' ===================== #
            # This function uses the concatenated dictionaries from the "BUILD_WORD_PAIR_DICTS" function
            # to write into two files: one containing words pairs with the leading word containing a
            # long-s and which is also present in the "Ambiguous Word Pairs" file; and another containing
            # long-s words for which there is no ambiguity regarding whether the OCR'd character should
            # be a long-s or an f. This file is used again by the "WRITE_TRAIL_WORD_PAIR_FILE" function
            # which follows this function. This function also generates a file containing single,
            # unambiguous words for a subsequent find-and-replace operation.

            dictA = concat_lead_dict                                                                    # switch dictionary name
            dictA_New = copy.deepcopy(dictA)                                                            # create copy for storage of duplicate values
            ambig_words_in_file = open(cwd + "\\AmbiguousPairs_Single_Column.txt","a+", encoding="utf-8")

            global text_list_alpha                                                                      # declare variable global for subsequent use inside user-defined functions
            text_list_alpha = []                                                                        # create empty list for words identified in "Ambiguous Words" file
            for line in ambig_words_in_file:                                                            # create loop for iteration through file lines
                text_list_alpha.append(line.rstrip())                                                   # write list and remove "\n" (newline) characters
                #print(text_list_alpha)                                                                 # !print command used for visual check during development only

            # ==== SECTION TO FIND NON-DUPLICATE ENTRIES ==== #

            remove_dict_alpha = dictA                                                                   # switch dictionary name (for easy identification in code block)
            dict_remove_list_alpha = text_list_alpha                                                    # assign reference list for word duplicates to variable

            for key in dict_remove_list_alpha:                                                          # create loop for iteration through dictionary
                if key in remove_dict_alpha:                                                            # check dictionary for matching keys
                    remove_dict_alpha.pop(key)                                                          # remove key if found in duplicate reference list
            #print(remove_dict_alpha)                                                                   # !print command used for visual check during development only

            remove_dict_alpha_as_list=[]                                                                # create empty list for population with identified pairs
            for a,b in remove_dict_alpha.items():                                                       # create loop for iteration through dictionary items
                remove_dict_alpha_as_list.append ((a,b))                                                # append dictionary items to empty list
            #print(remove_dict_alpha_as_list)                                                           # !print command used for visual check during development only

            rdal_alpha_corrected = [tuple(map(lambda i: str.replace(i, "ſ","s"), tup)) for tup in remove_dict_alpha_as_list] # replace long-s character in all words of identified pairs
            #print(rdal_alpha_corrected)                                                                # !print command used for visual check during development only

            # ==== SECTION TO FIND DUPLICATE ENTRIES ==== #

            keep_dict_alpha = dictA_New                                                                 # switch dictionary name (for easy identification in code block)
            dict_keep_list_alpha = remove_dict_alpha                                                    # assign reference list for word duplicates to variable

            for key in dict_keep_list_alpha:                                                            # create loop for iteration through dictionary
                if key in keep_dict_alpha:                                                              # check dictionary for matching keys
                    keep_dict_alpha.pop(key)                                                            # remove key if found in duplicate reference list
            #print(keep_dict_alpha)                                                                     # !print command used for visual check during development only

            keep_dict_alpha_as_list=[]                                                                  # create empty list for population with identified pairs
            for c,d in keep_dict_alpha.items():                                                         # create loop for iteration through dictionary items
                keep_dict_alpha_as_list.append(("",c))                                                  # append dictionary items containing only long-s words to empty list
            #print(keep_dict_alpha_as_list)                                                             # !print command used for visual check during development only

            kdal_alpha_corrected = [tuple(map(lambda j: str.replace(j, "ſ","s"), tup)) for tup in keep_dict_alpha_as_list] # replace long-s character in all words of identified pairs
            #print(kdal_alpha_corrected)                                                                # !print command used for visual check during development only

            # ==== LIST JOIN WITH EQUALS SIGN OPERATION ==== #

            final_joined_remove_alpha = []                                                              # create empty list for population with selected word pairs
            final_joined_remove_alpha = list(zip(remove_dict_alpha_as_list, rdal_alpha_corrected))      # concatenate original word pairs with corresponding corrected word pairs
            #print(final_joined_remove_alpha)                                                           # !print command used for visual check during development only

            final_joined_kept_alpha = []                                                                # create empty list for population with selected word pairs
            final_joined_kept_alpha = list(zip(keep_dict_alpha_as_list, kdal_alpha_corrected))          # concatenate original word pairs with corresponding corrected word pairs
            #print(final_joined_kept_alpha)                                                             # !print command used for visual check during development only

            write_removed_pairs_alpha = '\n'.join([str(i[0]) + "=" + str(i[1]) for i in final_joined_remove_alpha]) # create new line, concatenate selected & corrected word pairs with "=" (avoids whitespace error)
            write_removed_pairs_alpha = write_removed_pairs_alpha.replace("('", "")                     # delete leading open parenthesis and single quotation mark from file entries
            write_removed_pairs_alpha = write_removed_pairs_alpha.replace("', '", " ")                  # delete dividing single quotation marks, comma, and space from all word pairs
            write_removed_pairs_alpha = write_removed_pairs_alpha.replace("')", "")                     # delete closing single quotation mark and closed parenthesis from file entries
            write_removed_pairs_alpha = write_removed_pairs_alpha.replace(";", "")                      # delete any semi-colons from file entries
            #print(write_removed_pairs_alpha)                                                           # !print command used for visual check during development only

            write_kept_pairs_alpha = '\n'.join([str(j[0]) + "=" + str(j[1]) for j in final_joined_kept_alpha]) # create new line, concatenate selected words and corrected words with "=" (avoids whitespace error)
            write_kept_pairs_alpha = write_kept_pairs_alpha.replace("('", "")                           # delete leading open parenthesis and single quotation mark from file entries
            write_kept_pairs_alpha = write_kept_pairs_alpha.replace("', '", " ")                        # delete dividing single quotation marks, comma, and space from all word pairs
            write_kept_pairs_alpha = write_kept_pairs_alpha.replace("')", "")                           # delete closing single quotation mark and closed parenthesis from file entries
            write_kept_pairs_alpha = write_kept_pairs_alpha.replace(";", "")                            # delete any semi-colons from file entries
            #print(write_kept_pairs_alpha)                                                              # !print command used for visual check during development only

            # ==== FILE WRITE OPERATION ==== #

            os.chdir(os.path.dirname(os.getcwd()))                                                      # return to program root directory to open dictionary files

# <----------- LINE DE-DUPE PROCESS BELOW ----------->

            file_remove_alpha = open(cwd + "\\test_pairs_removed_dicts_output_leading_temp.txt", 'w+', encoding="utf-8") # open file for appending new leading long-s word pairs
            file_remove_alpha.write(write_removed_pairs_alpha)                                          # write new leading long-s word pairs to file
            file_remove_alpha.write("\n")                                                               # write new line character to ensure subsequent entries start on a new line
            file_remove_alpha.close()                                                                   # close file

            output_alpha_file_path = cwd + "\\test_pairs_removed_dicts_output_leading.txt"
            input_alpha_file_path = cwd + "\\test_pairs_removed_dicts_output_leading_temp.txt"
            completed_alpha_lines_hash = set()
            output_alpha_file = open(output_alpha_file_path, "w+", encoding="utf-8")
            for line in open(input_alpha_file_path, "r+", encoding="utf-8"):
                hashValue_alpha = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
                if hashValue_alpha not in completed_alpha_lines_hash:
                    output_alpha_file.write(line)
                    completed_alpha_lines_hash.add(hashValue_alpha)
            
            output_alpha_file.close()
            os.remove(input_alpha_file_path)
            
# <----------- LINE DE-DUPE PROCESS ABOVE ----------->

            file_kept_alpha = open(cwd + "\\test_kept_single_words_output.txt", 'w+', encoding="utf-8")    # open file for appending new long-s words
            file_kept_alpha.write(write_kept_pairs_alpha)                                               # write new long-s words to file
            file_kept_alpha.write("\n")                                                                 # write new line character to ensure subsequent entries start on a new line
            file_kept_alpha.close()                                                                     # close file
            ambig_words_in_file.close()                                                                 # close file
            # print(cwd)                                                                                  # !print command used for visual check during development only
            os.chdir(cwd)                                                                               # return to user-specified directory for processing next file

            # ====================== CREATE FUNCTION 'WRITE_TRAIL_WORD_PAIR_FILE' ===================== #
            # This function uses the concatenated dictionaries from the "BUILD_WORD_PAIR_DICTS" function
            # to write into two files: one containing words pairs with the trailing word containing a
            # long-s and which is also present in the "Ambiguous Word Pairs" file; and another containing
            # long-s words for which there is no ambiguity regarding whether the OCR'd character should
            # be a long-s or an f. This function also appends the file containing single, unambiguous
            # words with any new words for a subsequent find-and-replace operation in another function.

            dictB = concat_follow_dict                                                                  # switch dictionary name
            dictB_New = copy.deepcopy(dictB)                                                            # create copy for storage of duplicate values
            ambig_words_in_file_beta = open(cwd + "\\AmbiguousPairs_Single_Column.txt","a+", encoding="utf-8")

            global text_list_beta                                                                       # declare variable global for subsequent use inside user-defined functions
            text_list_beta = []                                                                         # create empty list for words identified in "Ambiguous Words" file
            for line in ambig_words_in_file_beta:                                                       # create loop for iteration through file lines
                text_list_beta.append(line.rstrip())                                                    # write list and remove "\n" (newline) characters
                #print(text_list_beta)                                                                  # !print command used for visual check during development only

            # ==== SECTION TO FIND NON-DUPLICATE ENTRIES ==== #

            remove_dict_beta = dictB                                                                    # switch dictionary name (for easy identification in code block)
            dict_remove_list_beta = text_list_beta                                                      # assign reference list for word duplicates to variable

            for key in dict_remove_list_beta:                                                           # create loop for iteration through dictionary
                if key in remove_dict_beta:                                                             # check dictionary for matching keys
                    remove_dict_beta.pop(key)                                                           # remove key if found in duplicate reference list
            #print(remove_dict_beta)                                                                    # !print command used for visual check during development only

            remove_dict_beta_as_list=[]                                                                 # create empty list for population with identified pairs
            for a,b in remove_dict_beta.items():                                                        # create loop for iteration through dictionary items
                remove_dict_beta_as_list.append ((a,b))                                                 # append dictionary items to empty list
            #print(remove_dict_beta_as_list)                                                            # !print command used for visual check during development only

            rdal_beta_corrected = [tuple(map(lambda i: str.replace(i, "ſ","s"), tup)) for tup in remove_dict_beta_as_list] # replace long-s character in all words of identified pairs
            #print(rdal_beta_corrected)                                                                 # !print command used for visual check during development only

            # ==== SECTION TO FIND DUPLICATE ENTRIES ==== #

            keep_dict_beta = dictB_New                                                                  # switch dictionary name (for easy identification in code block)
            dict_keep_list = remove_dict_beta                                                           # assign reference list for word duplicates to variable

            for key in dict_keep_list:                                                                  # create loop for iteration through dictionary
                if key in keep_dict_beta:                                                               # check dictionary for matching keys
                    keep_dict_beta.pop(key)                                                             # remove key if found in duplicate reference list
            #print(keep_dict_beta)                                                                      # !print command used for visual check during development only

            keep_dict_beta_as_list=[]                                                                   # create empty list for population with identified pairs
            for c,d in keep_dict_beta.items():                                                          # create loop for iteration through dictionary items
                keep_dict_beta_as_list.append(("",d))                                                   # append dictionary items containing only long-s words to empty list
            # print(keep_dict_beta_as_list)                                                             # !print command used for visual check during development only

            kdal_beta_corrected = [tuple(map(lambda j: str.replace(j, "ſ","s"), tup)) for tup in keep_dict_beta_as_list] # replace long-s character in all words of identified pairs
            # print(kdal_beta_corrected)                                                                # !print command used for visual check during development only

            # ==== LIST JOIN WITH EQUALS SIGN OPERATION ==== #

            final_joined_remove_beta = []                                                               # create empty list for population with selected word pairs
            final_joined_remove_beta = list(zip(remove_dict_beta_as_list, rdal_beta_corrected))         # concatenate original word pairs with corresponding corrected word pairs
            # print(final_joined_remove_beta)                                                           # !print command used for visual check during development only

            final_joined_kept_beta = []                                                                 # create empty list for population with selected word pairs
            final_joined_kept_beta = list(zip(keep_dict_beta_as_list, kdal_beta_corrected))             # concatenate original word pairs with corresponding corrected word pairs
            # print(final_joined_kept_beta)                                                             # !print command used for visual check during development only

            write_removed_pairs_beta = '\n'.join([str(i[0]) + "=" + str(i[1]) for i in final_joined_remove_beta]) # create new line, concatenate selected & corrected word pairs with "=" (avoids whitespace error)
            write_removed_pairs_beta = write_removed_pairs_beta.replace("('", "")                       # delete leading open parenthesis and single quotation mark from file entries
            write_removed_pairs_beta = write_removed_pairs_beta.replace("', '", " ")                    # delete dividing single quotation marks, comma, and space from all word pairs
            write_removed_pairs_beta = write_removed_pairs_beta.replace("')", "")                       # delete closing single quotation mark and closed parenthesis from file entries
            write_removed_pairs_beta = write_removed_pairs_beta.replace(";", "")                        # delete any semi-colons from file entries
            # print(write_removed_pairs_beta)                                                           # !print command used for visual check during development only

            write_kept_pairs_beta = '\n'.join([str(j[0]) + "=" + str(j[1]) for j in final_joined_kept_beta]) # create new line, concatenate selected words and corrected words with "=" (avoids whitespace error)
            write_kept_pairs_beta = write_kept_pairs_beta.replace("('", "")                             # delete leading open parenthesis and single quotation mark from file entries
            write_kept_pairs_beta = write_kept_pairs_beta.replace("', '", " ")                          # delete dividing single quotation marks, comma, and space from all word pairs
            write_kept_pairs_beta = write_kept_pairs_beta.replace("')", "")                             # delete closing single quotation mark and closed parenthesis from file entries
            write_kept_pairs_beta = write_kept_pairs_beta.replace(";", "")                              # delete any semi-colons from file entries
            write_kept_pairs_beta = write_kept_pairs_beta.replace("= ", "=")                            # delete any extra spaces from file entries
            # print(write_kept_pairs_beta)                                                              # !print command used for visual check during development only

            # ==== FILE WRITE OPERATION ==== #

            os.chdir(cwd)                                                      # return to program root directory to open dictionary files

# <----------- LINE DE-DUPE PROCESS BELOW ----------->

            file_remove_beta = open(cwd + "\\test_pairs_removed_dicts_output_leading_temp.txt", 'w+', encoding="utf-8") # open file for appending new leading long-s word pairs
            file_remove_beta.write(write_removed_pairs_beta)                                          # write new leading long-s word pairs to file
            file_remove_beta.write("\n")                                                               # write new line character to ensure subsequent entries start on a new line
            file_remove_beta.close()                                                                   # close file

            output_beta_file_path = cwd + "\\test_pairs_removed_dicts_output_following.txt"
            input_beta_file_path = cwd + "\\test_pairs_removed_dicts_output_following_temp.txt"
            completed_beta_lines_hash = set()
            output_beta_file = open(output_beta_file_path, "w+", encoding="utf-8")
            for line in open(input_beta_file_path, "r+", encoding="utf-8"):
                hashValue_beta = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
                if hashValue_beta not in completed_beta_lines_hash:
                    output_beta_file.write(line)
                    completed_beta_lines_hash.add(hashValue_beta)
            
            output_beta_file.close()
            #os.remove(input_beta_file_path)
            
# <----------- LINE DE-DUPE PROCESS ABOVE ----------->

            file_kept_beta = open(cwd + "\\test_kept_single_words_output.txt", 'w+', encoding="utf-8")            # open file for appending new long-s words
            file_kept_beta.write(write_kept_pairs_beta)                                                 # write new long-s words to file
            file_kept_beta.write("\n")                                                                  # write new line character to ensure subsequent entries start on a new line
            file_kept_beta.close()                                                                      # close file
            ambig_words_in_file_beta.close()                                                            # close file

            # ========================= CREATE FUNCTION 'DE-DUPE DICTIONARIES' ======================== #
            # This function deletes any duplicate entries from the text files which were created in the
            # "WRITE_LEAD_WORD_PAIR_FILE" and "WRITE_TRAIL_WORD_PAIR_FILE" functions. The results are 
            # written into new files which are used as the reference dictionaries in the "Clean" phase
            # of the program.

            # ==== CLEAN LEADING WORD PAIRS FILE ==== #

            # print(cwd)
            file_leading_dedupe = open(cwd + "\\test_pairs_removed_dicts_output_leading.txt", "r", encoding="utf-8") # open file containing leading long-s word pairs
            lines_leading_capture = set()                                                               # retain viewed lines in file as set
            master_leading_file_output = open(cwd + "\\before_words_main_uc.txt", "a+", encoding="utf-8")        # open master file for writing function output
            for line_l in file_leading_dedupe:                                                          # create loop for iteration through file lines
                if line_l not in lines_leading_capture:                                                 # check dictionary for duplicate lines
                    master_leading_file_output.write(line_l)                                            # write new lines to output file
                    lines_leading_capture.add(line_l)                                                   # append any new lines (if none, none are appended)
            master_leading_file_output.close()                                                          # close file

            clean_lines_lwpf = []                                                                       # create empty list for cleaned file lines
            with open(cwd + "\\before_words_main_uc.txt", "r", encoding="utf-8") as lwpuc:                      # open unclean file containing leading word pairs
                lwlines = lwpuc.readlines()                                                             # read contents of unclean file containing leading word pairs
                clean_lines_lwpf = [l.strip() for l in lwlines if l.strip()]                            # remove unwanted whitespace characters

            with open(cwd + "\\before_words_main.txt", "a+", encoding="utf-8") as lwpc:                          # open file for population with clean data
                lwpc.writelines('\n'.join(clean_lines_lwpf))                                            # write file with clean data

            # ==== CLEAN TRAILING WORD PAIRS FILE ==== #

            file_trailing_dedupe = open(cwd + "\\test_pairs_removed_dicts_output_following.txt", "r", encoding="utf-8") # open file containing trailing long-s word pairs
            lines_trailing_capture = set()                                                              # retain viewed lines in file as set
            master_trailing_file_output = open(cwd + "\\after_words_main_uc.txt", "a+", encoding="utf-8")        # open master file for writing function output
            for line_t in file_trailing_dedupe:                                                         # create loop for iteration through file lines
                if line_t not in lines_trailing_capture:                                                # check dictionary for duplicate lines
                    master_trailing_file_output.write(line_t)                                           # write new lines to output file
                    lines_trailing_capture.add(line_t)                                                  # append any new lines (if none, none are appended)
            master_trailing_file_output.close()                                                         # close file

            clean_lines_twpf = []                                                                       # create empty list for cleaned file lines
            with open(cwd + "\\after_words_main_uc.txt", "r", encoding="utf-8") as twpuc:                       # open unclean file containing trailing word pairs
                twlines = twpuc.readlines()                                                             # read contents of unclean file containing trailing word pairs
                clean_lines_twpf = [l.strip() for l in twlines if l.strip()]                            # remove unwanted whitespace characters
                
            with open(cwd + "\\after_words_main.txt", "w", encoding="utf-8") as twpc:                           # open file for population with clean data
                twpc.writelines('\n'.join(clean_lines_twpf))                                            # write file with clean data

            # ==== CLEAN SINGLE WORDS FILE ==== #

            file_single_word_dedupe = open(cwd + "\\test_kept_single_words_output.txt", "r", encoding="utf-8") # open file containing single unambiguous long-s words
            lines_single_word_capture = set()                                                           # retain viewed lines in file as set
            master_single_word_file_output = open(cwd + "\\single_words_main_uc.txt", "a+", encoding="utf-8")    # open master file for writing function output
            for line_sw in file_single_word_dedupe:                                                     # create loop for iteration through file lines
                if line_sw not in lines_single_word_capture:                                            # check dictionary for duplicate lines
                    master_single_word_file_output.write(line_sw)                                       # write new lines to output file
                    lines_single_word_capture.add(line_sw)                                              # append any new lines (if none, none are appended)
            master_single_word_file_output.close()                                                      # close file
            
            clean_lines_swf = []                                                                        # create empty list for cleaned file lines
            with open(cwd + "\\single_words_main_uc.txt", "r", encoding="utf-8") as swuc:                       # open unclean file containing single words
                swlines = swuc.readlines()                                                              # read contents of unclean file containing single words
                clean_lines_swf = [l.strip() for l in swlines if l.strip()]                             # remove unwanted whitespace characters
                
            with open(cwd + "\\single_words_main.txt", "a+", encoding="utf-8") as swc:                           # open file for population with clean data
                swc.writelines('\n'.join(clean_lines_swf))                                              # write file with clean data
    
            '''#######################################################################################'''
            '''.......................................................................................'''
            ''' .........CLEAN PHASE OF THE PROGRAM.  >  EXECUTE FIND AND REPLACE OPERATIONS..........'''
            '''.......................................................................................'''
            '''#######################################################################################'''

            # ========================= CREATE FUNCTION 'DICTIONARY_TEXT_INPUT' ======================= #
            # This function creates three python dictionaries from the files created in the
            # "DE-DUPE DICTIONARIES" function: one using the word pairs in the # "before_words_main.txt"
            # file, another using the word pairs in the "after_words_main.txt" file, and a final 
            # dictionary containing single words using the "single_words_main_uc.txt" file. These 
            # dictionaries are then used in subsequent functions as the reference lists for find and 
            # replace operations.

            global file_before_words                                                                    # declare variable global for subsequent use inside user-defined functions
            file_before_words = open(cwd + "\\before_words_main.txt","r", encoding="utf-8-sig").read()          # open file containing leading long-s word pairs ("-sig" used to prevent BOM character in dict build)
            #print(file_before_words)                                                                   # !print command used for visual check during development only
            global file_after_words                                                                     # declare variable global for subsequent use inside user-defined functions
            file_after_words = open(cwd + "\\after_words_main.txt","r", encoding="utf-8-sig").read()            # open file containing trailing long-s word pairs ("-sig" used to prevent BOM character in dict build)
            #print(file_after_words)                                                                    # !print command used for visual check during development only
            global file_single_words                                                                    # declare variable global for subsequent use inside user-defined functions
            file_single_words = open(cwd + "\\single_words_main.txt","r", encoding="utf-8-sig").read()          # open file containing single unambiguous long-s words ("-sig" used to prevent BOM character in dict build)
            #print(file_single_words)                                                                   # !print command used for visual check during development only
            # global file_all_s_words                                                                     # declare variable global for subsequent use inside user-defined functions
            # file_all_s_words = open(cwd + "\\FINAL_LIST_CORRECTED_S_WORDS.txt","r", encoding="utf-8-sig").read()# open file containing single unambiguous long-s words ("-sig" used to prevent BOM character in dict build)
            #print(file_all_s_words)                                                                    # !print command used for visual check during development only

            # ======================== CREATE FUNCTION 'MAKE_BEFORE_WORDS_DICT' ======================= #
            # This function transforms the contents of the file containing leading long-s word pairs
            # into a python dictionary. The dictionary which is created is the reference point for 
            # subsequent find and replace operations.

            file_before_words.split("\n")                                                               # split lines at new line character (divides lines of file into discrete sections for dictionary build)
            file_before_words = file_before_words.replace("\n", "=")                                    # replace new line character with equals sign to enable dictionary key-and-value pairing
            bw_dict = {}                                                                                # create empty dictionary for population with selected word pairs
            bw_contents = file_before_words.split("=")                                                  # split lines at whitespace to tokenize list
            # print(bw_contents)                                                                        # !print command used for visual check during development only
            bw_dict = dict(zip(bw_contents[::2], bw_contents[1::2]))                                    # populate dictionary - words in odd positions as keys / words in even positions as values
            # print(bw_dict)                                                                            # !print command used for visual check during development only
            global dict_before_words                                                                    # declare variable global for subsequent use inside user-defined functions
            dict_before_words = bw_dict                                                                 # switch variable name (allows and safeguards use of global variable)
            # print(dict_before_words)                                                                  # !print command used for visual check during development only

            # ======================== CREATE FUNCTION 'MAKE_AFTER_WORDS_DICT' ======================== #
            # This function transforms the contents of the file containing trailing long-s word pairs
            # into a python dictionary. The dictionary which is created is the reference point for 
            # subsequent find and replace operations.

            file_after_words.split("\n")                                                                # split lines at new line character (divides lines of file into discrete sections for dictionary build)
            file_after_words = file_after_words.replace("\n", "=")                                      # replace new line character with equals sign to enable dictionary key-and-value pairing
            aw_dict = {}                                                                                # create empty dictionary for population with selected word pairs
            aw_contents = file_after_words.split("=")                                                   # split lines at whitespace to tokenize list
            # print(aw_contents)                                                                        # !print command used for visual check during development only
            aw_dict = dict(zip(aw_contents[::2], aw_contents[1::2]))                                    # populate dictionary - words in odd positions as keys / words in even positions as values
            # print(aw_dict)                                                                            # !print command used for visual check during development only
            global dict_after_words                                                                     # declare variable global for subsequent use inside user-defined functions
            dict_after_words = aw_dict                                                                  # switch variable name (allows and safeguards use of global variable)
            # print(dict_after_words)                                                                   # !print command used for visual check during development only

            # ======================== CREATE FUNCTION 'MAKE_SINGLE_WORDS_DICT' ======================= #
            # This function transforms the contents of the file containing single long-s words into a 
            # python dictionary. The dictionary which is created is the reference point for subsequent 
            # find and replace operations.

            # file_single_words = file_single_words.replace(" ", "BBB")                                   
            # file_single_words = re.sub("\n", "AAA", file_single_words)                                   
            sw_dict = {}                                                                                # create empty dictionary for population with selected word pairs
            sw_contents = file_single_words.split("=")                                                  # split lines at whitespace to tokenize list
            # print(sw_contents)                                                                        # !print command used for visual check during development only
            sw_dict = dict(zip(sw_contents[::2], sw_contents[1::2]))                                    # populate dictionary - words in odd positions as keys / words in even positions as values
            # print(sw_dict)                                                                            # !print command used for visual check during development only
            global dict_single_words                                                                    # declare variable global for subsequent use inside user-defined functions
            dict_single_words = sw_dict                                                                 # switch variable name (allows and safeguards use of global variable)
            # print(dict_single_words)                                                                  # !print command used for visual check during development only
            os.chdir(origin_root) # return to user-specified directory for processing next file

            # ============================== CREATE FUNCTION 'INPUT FILE' ============================= #
            # This function opens the test file for processing and subsequent find-and-replace 
            # operations. In the final version of the script, this will be replaced by a loop to 
            # iterate through the TEI files in the selected directory.

            # ==== FIND AND READ ENCYCLOPEDIA ENTRY ==== #

            input_text = livefile                                                                       # create variable for find and replace operations
            textwords_alpha = input_text                                                                # switch variable name (for easy identification in code block)
            # print(textwords_alpha)                                                                    # !print command used for visual check during development only

            # ========================= CREATE FUNCTION 'FIND_REPLACE_LEADING' ======================== #
            # This function uses the master output text file containing leading long-s word pairs to 
            # replace any long-s words in the input files. The cleaned files are written with the suffix 
            # "-corrected". The DOM and tag structure of the original file is maintained.

            pattern_RPL = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in dict_before_words.keys()) + r')(?!\w)') # compile regex into regex object to enable leading long-s word pairs search
            result_RPL = pattern_RPL.sub(lambda x: dict_before_words[x.group()], textwords_alpha)       # replace identified leading long-s word pairs with corrected word pairs
            # print(result_RPL)                                                                         # !print command used for visual check during development only
            text_gamma = result_RPL                                                                     # switch variable name (for easy identification in code block)

            # ======================== CREATE FUNCTION 'FIND_REPLACE_TRAILING' ======================== #
            # This function uses the master output text file containing trailing long-s word pairs to 
            # replace any long-s words in the input files. The cleaned files are written with the suffix 
            # "-corrected". The DOM and tag structure of the original file is maintained.

            pattern_RPT = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in dict_after_words.keys()) + r')(?!\w)') # compile regex into regex object to enable trailing long-s word pairs search
            result_RPT = pattern_RPT.sub(lambda y: dict_after_words[y.group()], text_gamma)             # replace identified trailing long-s word pairs with corrected word pairs
            # print(result_RPT)                                                                         # !print command used for visual check during development only
            text_epsilon = result_RPT                                                                   # switch variable name (for easy identification in code block)

            # ========================= CREATE FUNCTION 'FIND_REPLACE_SINGLE' ========================= #
            # This function uses the master output text file containing single unambiguous long-s words
            # to replace any long-s words in the input files. The cleaned files are written with the 
            # suffix "-corrected". The DOM and tag structure of the original file is maintained.

            text_zeta=[]                                                                                # create empty list for population with selected words
            for y in (o.group(0) for o in re.finditer(r'\w+|\W+', text_epsilon)):                       # create loop for iteration through text and use regex to find matching words
                if y in dict_single_words:                                                              # check dictionary for duplicates
                    y=dict_single_words[y]                                                              # build list of matching words
                text_zeta.append(y)                                                                     # append matching words to initial empty list
                # print(text_zeta)                                                                      # !print command used for visual check during development only
            epsilon_list = text_zeta                                                                    # switch variable name (for easy identification in code block)
            text_omega = ''.join(map(str, epsilon_list))                                                # replace matching words and place into new variable
            # print(text_omega)                                                                         # !print command used for visual check during development only

            # ==== FINAL TEXT CLEANING OPERATIONS ==== #

            text_omega = text_omega.replace("\n", " ")                                                  # replace residual/unwanted new line characters with spaces
            text_omega = text_omega.replace("   ", " ")                                                 # replace contiguous duplicates spaces with single spaces
            text_omega = text_omega.replace("</p> </div>", "</p></div>")                                # delete space between closing </p> and </div> tags created by word replacement operations
            text_omega = text_omega.replace(" </p>", "</p>")                                            # delete any triple spaces between any tags created by word replacement operations
            text_omega = text_omega.replace("> <", "><")                                                # delete any spaces between any tags created by word replacement operations
            text_omega = text_omega.replace(">  <", "><")                                               # delete any double spaces between any tags created by word replacement operations
            text_omega = text_omega.replace(">   <", "><")                                              # delete any triple spaces between any tags created by word replacement operations
            # print(text_omega)                                                                         # !print command used for visual check during development only

            # ============================ CREATE FUNCTION 'WRITE_NEW_FILE' =========================== #
            # This function writes the corrected file to a new directory with the suffix "-CRTD". The   #
            # directory where the corrected file is written is taken from the user input in the         #
            # "REQUEST_USER_INPUT" section.

            file_in_name = filename.split(".")[0]                                                       # capture name of input file and discard file extension
            file_out_name = file_in_name + "-CRTD" + ".xml"                                             # create new file name by adding "-CRTD" to end of name of input file and specify file extension
            print(file_out_name)                                                                        # display file name to indicate progress during processing of files
            write_location = write_directory # change directory to user-specified directory for output files
            os.chdir(write_location)                                                                    # change to user-specified directory for writing corrected files
            # print(os.getcwd())                                                                        # !print command used for visual check during development only
            with open(file_out_name,"w+", encoding="utf-8") as CRTD_file:                               # create empty new file with new file name
                CRTD_file.write(text_omega)                                                             # write corrected content to empty file
                CRTD_file.close()                                                                       # save and close new file
                os.chdir(origin_root) # return to user-specified directory for processing next file
                # print(os.getcwd())                                                                    # !print command used for visual check during development only

    # =========================================== END ========================================= #
    print("======>ALL PROCEDURES COMPLETED<======")
    print("================>END.<================")

if __name__ == "__main__":
    main()