from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import re

def get_definitions(tag):
	tag = re.sub(' ','+', tag) # put input into urban form: 'new york' --> 'new+york'
	url = 'http://www.urbandictionary.com/define.php?term=%s'
	data = urlopen(url % (tag)).read()
	data = BeautifulSoup(data)
	results1 = data.findAll('div', attrs={'class' : 'definition'})[0].text
	results2 = data.findAll('div', attrs={'class' : 'definition'})[1].text
	results3 = data.findAll('div', attrs={'class' : 'definition'})[2].text
#	results = re.sub('str', '', results)
	
	if results1.find('&quot',0,200)<0:
		results = results1
#		print('one')
	elif results2.find('&quot',0,200)<0:
		results =results2
#		print('two')
	else:
		results = results3
#		print('three')
#	print(results)

	if results.find('.',100)>0:
		results = results[0:results.find('.',100)+1]
	else:
		results = results[0:100]
#	print results
	return results

if __name__ == '__main__':
	tag = raw_input('topic: ')	
	definitions = get_definitions(tag)
