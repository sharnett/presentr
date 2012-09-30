# -*- coding: utf-8 -*-

from urllib2 import urlopen
from json import load,dumps
from splitpgraph import splitpgraph
import re
from random import sample

def getFacts(subject, num_titles=3, num_sentences=27):
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
        #print articleText
        unwiki = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
        newText = unwiki.sub(r'\1', articleText)
        newText = re.sub('<.*>','',newText)
        newText = re.sub('\{\{.*\}\}','',newText)
        newText = re.sub('\n',' ',newText)
        newText = re.sub('\'*','',newText)
        return newText

    n = num_sentences/num_titles
    titles = [getTitle(i, getText(i)) for i in xrange(1, num_titles+1)]
    text = []
    for section in xrange(1, 6):
        text += splitpgraph(getText(section))[2:]
    text = sample(text, num_sentences)

    return titles, text

if __name__ == '__main__':
	subject = raw_input('topic: ')
	titles, text = getFacts(subject)
	for i, title in enumerate(titles):
		print i, title
	for i, t in enumerate(text):
		print i, t
