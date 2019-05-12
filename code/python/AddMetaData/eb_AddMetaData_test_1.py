from lxml import etree as et
import pandas as pd

'''
This script is a test of adding meta data to a TEI entry file based on this entry's meta-data csv file.
Created by Luling Huang on April 30, 2019.
luling.huang@temple.edu
'''

def analyze_csv(csv):
    '''
    Evaluate the values in a meta-data csv file.
    Retrieve three pieces of information: scheme name, uri, and label.
    Put these three pieces of information in a nested dictionary of the following structure:
    {
    "Scheme_1":{uri_1:label_1,
                uri_2:label_2,
                uri_3:label_3},
    "Scheme_2":{uri_4:label_2,
                uri_5:label_3,
                uri_6:label_6}           
                }
    Note that uri is treated as a unique identifier here, while label may not be unique.
    In theory, uri under one scheme name can be not unique.
    '''
    df = pd.read_csv(csv)
    schemes = df.v_name.unique().tolist()
    adict = {}
    for x in schemes:
        count_labels = 0
        for index,row in df[df['v_name']==x].iterrows():
            if row['score'] >= 6: # Change accordingly
                label = row['preflabel'].lower()
                if pd.isnull(row['uri']) == True: # If uri is empty
                    scheme_uri = '#' + x.lower() + ':_' + str(index) # Create a unique identifier (with the row index as a proxy unique id)
                else:
                    scheme_uri = row['uri']
                if count_labels == 0: 
                    adict[x] = {}
                adict[x].update({scheme_uri:label})
                count_labels += 1
            else:
                continue
    return adict

def create_tags(nest_dict):
    '''
    Create the tags for meta-data based on the nested dictionary.
    '''
    profileDesc = et.Element('profileDesc')
    textClass = et.SubElement(profileDesc,'textClass')
    for x in nest_dict.keys():
        scheme_name = x.lower()
        if scheme_name == 'lcsh':
            scheme_uri = list(nest_dict[x].keys())[0].rsplit('/',1)[0] + '.html'
            keywords = et.SubElement(textClass,'keywords',scheme=scheme_uri)
            for key in nest_dict[x].keys():
                term_text = nest_dict[x][key]
                ref_value = 'lcsh:' + key.rsplit('/',1)[1]
                term = et.SubElement(keywords, "term", ref=ref_value)
                term.text = term_text
        else:
            scheme_uri = '#' + scheme_name
            keywords = et.SubElement(textClass,'keywords',scheme=scheme_uri)
            for key in nest_dict[x].keys():
                if key[0] == '#':
                    term_text = nest_dict[x][key]
                    ref_value = key
                    term = et.SubElement(keywords, "term", ref=ref_value)
                    term.text = term_text
                else:
                    term_text = nest_dict[x][key]
                    ref_value = scheme_name + ':' + term_text
                    term = et.SubElement(keywords, "term", ref=ref_value)
                    term.text = term_text
    return profileDesc

if __name__=='__main__':
    csv = 'Rope.txt.csv'
    csv_dict = analyze_csv(csv)
    
    profileDesc = create_tags(csv_dict)

    with open ('eb11-23-r04-0713-01-old.xml','r') as f:
        tree = et.parse(f)
    root = tree.getroot()
    '''
    Deal with multiple namespaces in xml.
    See: https://stackoverflow.com/questions/36777424/python-lxml-findall-with-multiple-namespaces
    The following uses the xpath solution given in the answer in the above link
    '''
    nsmap = {'a':'http://www.tei-c.org/ns/1.0','b':'http://www.w3.org/1999/xhtml'}
    fileDesc = root.xpath('/a:TEI/a:teiHeader/a:fileDesc',namespaces=nsmap)[0]
    fileDesc.addnext(profileDesc)

    tree.write('eb11-23-r04-0713-01-output5.xml', xml_declaration=True, encoding='UTF-8')