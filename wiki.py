from urllib2 import urlopen
from json import load,dumps

#def getFacts(subject):
subject = 'pizza'

url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=1&titles='+subject+'&format=json'
article = load(urlopen(url))

articleText = article['query']['pages']['24768']['revisions'][0]['*']
print articleText
