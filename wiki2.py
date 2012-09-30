from urllib2 import urlopen
from json import load,dumps
import re

#def getFacts(subject):
subject = 'tiger'
section = 1

url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=%d&titles='+subject+'&format=json'
article = load(urlopen(url % section))

articleText = article['query']['pages']['30075']['revisions'][0]['*']

print articleText
unwiki = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
newText = unwiki.sub(r'\1', articleText)
print newText



