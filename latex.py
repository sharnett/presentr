# -*- coding: utf-8 -*-
from random import randint
import re
import os

def presentation(topic, name, titles, photos, captions, text, definitions):
    themes = ['default', 'Antibes', 'Bergen', 'Berkeley', 'Berlin', 'Boadilla',
            'CambridgeUS', 'Copenhagen', 'Darmstadt', 'Dresden', 'Frankfurt',
            'Ilmenau', 'JuanLesPins', 'Luebeck', 'Madrid', 'Malmoe',
            'Montpellier', 'Pittsburgh', 'Rochester', 'Szeged', 'Warsaw']
    colors = ['default', 'beaver', 'beetle', 'crane', 'dove', 'rose',
            'seahorse', 'whale', 'lily']
    N, l, newsection, i_title = 9, 0, 3, 0
    photos = [photo.encode('ascii','ignore') for photo in photos]
    captions = [caption.encode('ascii','ignore') for caption in captions]
    captions = [re.sub('<[^<]+?>', '', caption) for caption in captions]
    captions = [re.sub('[^a-zA-Z\d\s]','',caption) for caption in captions]
    titles = [title.encode('ascii','ignore') for title in titles]
    text = [t.encode('ascii','ignore') for t in text]
    print 'photos:', len(photos)
    print 'captions:', len(captions)
    print 'titles:', len(titles)
    print 'text:', len(text)
    outfile = open('tmp/output.tex','w')
    intro = open('latex_pieces/introduction.txt').read()
    lframe = open('latex_pieces/frameleft.txt').read()
    rframe = open('latex_pieces/frameright.txt').read()
    mframe = open('latex_pieces/framemiddle.txt').read()
    concl = open('latex_pieces/conclusion.txt').read()
    defn = open('latex_pieces/definition.txt').read()
    x = intro % (themes[randint(0,len(themes)-1)],
            colors[randint(0,len(colors)-1)], topic, topic, name, 'hackNY')
    outfile.write(x + '\n')
    x = defn %  (topic, definitions)
    outfile.write(x + '\n')
    for k in xrange(0,3*N-1,3):
        p = randint(1,3)
        if newsection == 3:
            if p == 1:
                x = lframe % ('\section{' + titles[i_title] + '}', '\subsection{' + 
                        captions[l] + '}', text[k], text[k+1], text[k+2], photos[l])
                outfile.write(x + '\n')
            elif p == 2:
                x = rframe % ('\section{' + titles[i_title] + '}', '\subsection{' + 
                        captions[l] + '}', captions[l], photos[l], text[k], text[k+1], text[k+2])
                outfile.write(x + '\n')
            else :
                x = mframe % ('\section{' + titles[i_title] + '}', '\subsection{' + 
                        captions[l] + '}', captions[l], photos[l])
                outfile.write(x + '\n')
            newsection = 1
            i_title += 1
        else:
            if p == 1:
                x = lframe % ('', '\subsection{' + captions[l] + '}', text[k], 
                        text[k+1], text[k+2], photos[l])
                outfile.write(x + '\n')
            elif p == 2:
                x = rframe % ('', '\subsection{' + captions[l] + '}', 
                        captions[l], photos[l], text[k], text[k+1], text[k+2])
                outfile.write(x + '\n')
            else :
                x = mframe % ('', '\subsection{' + captions[l] + '}', 
                        captions[l], photos[l])
                outfile.write(x + '\n')
            newsection += 1
        l += 1
    x = concl % (text[3*N],text[3*N+1],text[3*N+2])
    outfile.write(x)
    outfile.close()
    os.system('pdflatex -output-directory tmp -interaction=batchmode tmp/output.tex')
    os.system('pdflatex -output-directory tmp -interaction=batchmode tmp/output.tex')
    os.system("cd tmp/ && ls -1 . | grep '[^(output.pdf)]' | xargs rm -v && rm output.out")

if __name__ == '__main__':
    #topic = 'Tigers'
    #name = 'Sean Kingston'
    #photos = ['comics_Layer.jpg','comics_Layer.jpg','comics_Layer.jpg', 'comics_Layer.jpg','comics_Layer.jpg']
    #captions = ['one caption', 'two caption', 'three caption', 'four caption', 'five caption']
    #text = ['lots', 'of', 'friggin', 'text', 'so', 'much', 'text', 'loads of tigers', 'nine', 'i', 'love', 'tigers','who', 'does', 'not', 'love', 'sean', 'kingston']
    #titles = ['TITLE 1', 'TITLE 2', 'TITLE 3', 'TITLE 4', 'TITLE 5']
    presentation(topic, name, titles, photos, captions, text, definitions)
