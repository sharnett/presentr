from urllib2 import urlopen
from json import load,dumps
from splitpgraph import splitpgraph
import re

def getFacts(subject):
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

	for section in xrange(1,5):
		sentences = splitpgraph(getText(section))
		presentation[getTitle(section, getText(section))] = sentences[2:6]
		
	return presentation

print getFacts('tiger')
