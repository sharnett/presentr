# -*- coding: utf-8 -*-

from urllib2 import urlopen
from json import load,dumps
import re
from random import sample
from re import split

def splitpgraph(pgraph):
    return split('\. ',pgraph)

def getFacts(subject, num_titles=3, num_sentences=27):
    
    subject = subject.title()
    subject = re.sub(' ','_',subject) # put input into wiki format i.e. 'albert einstein' --> 'Albert_Einstein'

    presentation = {}

    def getTitle(section, text):
        regex1 = r"\=\=(.*?)\=\="
        header = re.search(regex1, text)
        return header.group(1)

    def getText(section):
        url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=%d&titles='+subject+'&format=json'
        article = load(urlopen(url % section))
        articleID = article['query']['pages'].keys()
        articleText = article['query']['pages'][articleID[0]]['revisions'][0]['*']

        unwiki = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
        newText = unwiki.sub(r'\1', articleText)                  # handles wiki links w/ pipes and without
        newText = re.sub('<.*>','',newText)                       # gets rid of anything inside and including < >
        newText = re.sub('\{\{ *.* *\}\}','',newText)             # gets rid of anything inside and including {{ }}
        newText = re.sub('\n',' ',newText)                        # turns newline characters into spaces
        newText = re.sub('\'\'+','',newText)                      # gets rid of more than one consecutive single quote
        newText = re.sub('\|.*\|','',newText)                     # gets rid of anything inside and including | |
        newText = re.sub('\[\[.*\]\]','',newText)                 # gets rid of anything inside and including [[ ]]
        newText = re.sub(' \* ','',newText)                       # gets rid of wiki's bullet points
        newText = re.sub('File:.*\|','',newText)                  # gets rid of anything inside and including File: |
        newText = re.sub('&nbsp;',' ',newText)                    # turns &nbsp; into spaces
        newText = re.sub('\w*\|\w*','',newText)                   # gets rid of pipe between any number of alphanumeric chars

        return newText

    n = num_sentences/num_titles
    titles = [getTitle(i, getText(i)) for i in xrange(1, num_titles+1)]
    text = []
    for section in xrange(1, 6):
        text += splitpgraph(getText(section))
    text = sample(text, num_sentences)

    for i in xrange(len(text)):
 		text[i] = re.sub('\=*.*?\=*','',text[i])                  # now that titles have been extracted, get rid of remaining subtitles

    return titles, text

if __name__ == '__main__':
	subject = raw_input('topic: ')
	titles, text = getFacts(subject)
	for i, title in enumerate(titles):
		print i, title
	for i, t in enumerate(text):
 		print i, t
