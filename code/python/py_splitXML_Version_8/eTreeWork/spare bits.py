		page = strip_XMLheader(page)
		
# ============================= CREATE FUNCTION 'strip_XMLheader' ============================ #
# Strips XML declaration from files

def strip_XMLheader(data, invalid_xmldec):
		soup = BeautifulSoup(data, "lxml-xml")
		
		for xmldeclaration in soup.findAll(True)
			if match in invalid_xmldec:
				xmldec_replace = ""
				match.replacewith(xmldec_replace)

				for c in xmldeclaration.contents:
					if not isinstance(c, NavigableString):
						c = strip_XMLheader(unicode(c), invalid_xmldec)
				s += unicode(c)

			tag.replaceWith(xmldec_replace)

			return soup

			page = soup.prettify()

			==================================
			
			
					xmldecl = soup.find_all(text = re.compile('<?xml version="1.0" encoding="utf-8"?> <p/>'))
		fixed_comments = []
		for comment in xmldecl:
			fixed_text = unicode(comment).replace('<?xml version="1.0" encoding="utf-8"?> <p/>', 'MMMMMMMMMMMMMMMMMMMMM')
			comment.replace_with(fixed_text)
			fixed_comments.append(fixed_text)