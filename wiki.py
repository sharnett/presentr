from urllib.request import urlopen
from json import load,dumps
import re
from random import sample
from multiprocessing import Pool

def splitpgraph(pgraph):
    return re.split('\w{5,}\. ',pgraph)

def getFacts(subject, num_titles=3, num_sentences=27):
    subject = re.sub(' ','_',subject) # put input into wiki format i.e. 'albert einstein' --> 'Albert_Einstein'

    translate = [
    (r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]',r'\1'),
    ('<.*>',''),
    ('\{\{ *.* *\}\}',''),
    ('\n',' '),
    ('\'\'+',''),
    ('\|.*\|',''),
    ('\[\[.*\]\]',''),
    ('\[\[.*\]\]',''),
    (' \* ',''),
    ('File:.*\|',''),
    ('&nbsp;',' '),
    ('\w*\|\w*',''),
    ('\w*\}\}',''),
    ('[%${}]',''),
    ]

    def getTitle(section, text):
        regex1 = r"\=\=(.*?)\=\="
        header = re.search(regex1, text)
        return header.group(1)

    def getText(section):
        url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=%d&titles=%s&format=json&redirects=true'
        article = load(urlopen(url % (section, subject)))
        if not 'query' in article:
            article = load(urlopen(url % (section, subject.title())))
        if not 'query' in article:
            article = load(urlopen(url % (section, subject.lower())))
        articleID = list(article['query']['pages'].keys())
        articleText = article['query']['pages'][articleID[0]]['revisions'][0]['*']
        for substitution in translate:
            articleText = re.sub(substitution[0], substitution[1],articleText)

        return articleText

    n = num_sentences/num_titles
    titles = [getTitle(i, getText(i)) for i in range(1, num_titles+1)]
    text = []
    section = 1
    while len(text) < num_sentences:
        try:
            text += splitpgraph(getText(section))
            section += 1
        except KeyError:
            break
    while len(text) < num_sentences:
        text += ['james']
    text = sample(text, num_sentences)
    for i in range(len(text)):
        text[i] = re.sub('\=*.*?\=*','',text[i]) # now that titles have been extracted, get rid of remaining subtitles
    for i in range(len(titles)):
        titles[i] = re.sub('=','',titles[i]) # get rid of stray =
    return titles, text

if __name__ == '__main__':
    subject = input('topic: ')
    titles, text = getFacts(subject)
    for i, title in enumerate(titles):
        print(i, title)
    for i, t in enumerate(text):
        print(i, t)
