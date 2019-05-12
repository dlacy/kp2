###===========XML DATA CLEANING SCRIPT / ENCYCLOPEDIA PROJECT TEMPLE UNIVERSITY===========###
#																							#
# This script is based on the original script created by Andrea Siotto on					#
# Oct. 13, 2016.  The script retains the data cleaning and organizaing functions			#
# but does not include HTML-to-TEI/XML formatting processes.								#
#																							#
# Date Created: June 16, 2017																#
# Created By: Gary Scales - gary.scales@temple.edu											#
# Date Modified: July 20, 2017																#
# Modified By: Gary Scales - gary.scales@temple.edu											#
#																							#
###=======================================================================================###
  
# ==================================IMPORT PYTHON MODULES================================== #

import os
import codecs
import re
from bs4 import BeautifulSoup 
from bs4 import NavigableString

from lxml import etree
# from xml.etree import ElementTree as et
import sys
try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

# xmltestfile = "file_for_testing.xml"
# testfile = open(xmltestfile, 'r')
# # print (testfile)

# from lxml import etree

# string = "<?xml version="1.0" encoding="utf-8"?> </p>"
# tree = etree.fromstring(string)

# pis = tree.xpath("//processing-instruction()")
# for pi in pis:
    # etree.strip_tags(pi.getparent(), pi.tag)

# print etree.tostring(tree)

xmlheadnum1 = str(1)
xmlheadnum2 = str(0)
xmlheadnum3 = str(8)
xml_dec = "<?xml version="+xmlheadnum1+"."+xmlheadnum2+" encoding=""utf-"+xmlheadnum3+""'?> </p>'""
e = xml_dec
print(e)