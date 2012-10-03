from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import re

def get_definitions(tag):
	url = 'http://www.urbandictionary.com/define.php?term=%s'
	data = urlopen(url % (tag)).read()
	data = BeautifulSoup(data)
	results = data.findAll('div', attrs={'class' : 'definition'})[1].text
	return results

if __name__ == '__main__':
	tag = raw_input('topic: ')	
	definitions = get_definitions(tag)
