# kp2
## Introduction
This repository contains working files for the _Nineteenth-Century Knowledge Project_. The project is creating standards-compliant digital editions of four historical editions of the _Encyclopedia Britannica_. For further information, see [the GitHub pages site](http://TU-plogan.github.io).

## Organization

folder | subfolder | subfolder | type | description
--- | --- | --- | --- | ---
page | edition/section | 2-page-docx | docx| ocr output files @1 page per file
&nbsp; | | 3-page-tei | xml | tei files @1 page per file
entry | edition/section | 4-entry-tei | xml | tei files @1 entry per file
&nbsp; | | 5-entry-md | csv | subject metadata files from HIVE
&nbsp; | &nbsp; | 6-master-tei | xml | master files: 4-entry-tei with metadata added; used to create digital-editions 
digital-editions | css | | css | stylesheets for html edition
&nbsp; | images | |	jpg, png | images for html edition
&nbsp; | html | | html | html derivatives from master files
&nbsp; | txt | | txt | plain text derivatives from master files
analytics | | |	csv; xlsx | output from analytic procedures
code | python | AddMetaData | | alpha: grabs data from 5-entry-md files and writes into the TEI header of 6-master-tei files
&nbsp; | &nbsp; | LongS_Correction_Tool | | beta: cleans the long S from eb03 files.
&nbsp; | &nbsp; | py_splitXML_version_8 | | beta: concatenates page files (3-page-tei), corrects footnotes, segments into entry files (4-entry-tei).
&nbsp; | regex | | txt | regex scripts and notes
&nbsp; | scenarios | | scenario | groups of xslt routines used in Oxygen
&nbsp; | xslt | | | xsl transformation scripts

