from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import re

def get_definitions(tag):
	tag = re.sub(' ','+', tag) # put input into urban form: 'new york' --> 'new+york'
	url = 'http://www.urbandictionary.com/define.php?term=%s'
	data = urlopen(url % (tag)).read()
	data = BeautifulSoup(data)

	nodefinition, k, i = 0, 0, 0
	maxdefn = len(data.findAll('div', attrs={'class' : 'definition'}))
	defns = []

	while nodefinition < 3 and k < maxdefn:
		defn = data.findAll('div', attrs={'class' : 'definition'})[k].text	
		if defn.find('.',5)>0:
		        defn = re.sub('&quot;', '\"', defn)     # remove awkward urban dict format
                        defn = re.sub('\d', '', defn)           # remove numbers
                	defn = re.sub('\A. ', '', defn)         # remove bad formatting at beginning
			defn = defn[0:defn.find('.',5)+1]
			defns += [defn.capitalize()]
			nodefinition += 1
			i += 1
		k += 1

	# padding:
	if len(defns) == 2:
		defns += ['This is everything mankind knows about %s.' % tag]
	elif len(defns) == 1:
		defns += ['Little more is known of this %s you speak of.' % tag]
		defns += ['Hello World.']
	elif len(defns) == 0:
		defns += ['Well done.']
		defns += ['Urban Dictionary has not even heard of this %s you speak of.' % tag]
		defns += ['Hello World.']
	return defns

if __name__ == '__main__':
	tag = raw_input('topic: ')	
	definitions = get_definitions(tag)
