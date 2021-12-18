import re
import os
from random import randint, choice
from datetime import datetime

def presentation(topic, name, titles, photos, captions, text, definitions):
    themes = ['default', 'Antibes', 'Bergen', 'Berkeley', 'Berlin', 
            'Copenhagen', 'Darmstadt', 'Dresden', 'Frankfurt', 'Ilmenau', 
            'JuanLesPins', 'Luebeck', 'Madrid', 'Malmoe', 'Szeged', 'Warsaw']
    colors = ['default', 'beetle', 'crane', 'orchid', 'rose', 'whale', 'lily']
    N, l, newsection, i_title = 9, 0, 3, 0
    photos = [photo for photo in photos]
    captions = [caption for caption in captions]
    captions = [re.sub('<[^<]+?>', '', caption) for caption in captions]
    captions = [re.sub('[^a-zA-Z\d\s]','',caption) for caption in captions]
    titles = [title for title in titles]
    text = [t for t in text]
    outfile = open('tmp/output.tex','w')
    intro = open('latex_pieces/introduction.txt').read()
    lframe = open('latex_pieces/frameleft.txt').read()
    rframe = open('latex_pieces/frameright.txt').read()
    mframe = open('latex_pieces/framemiddle.txt').read()
    concl = open('latex_pieces/conclusion.txt').read()
    defn = open('latex_pieces/definition.txt').read()
    x = intro % (choice(themes), choice(colors), topic.capitalize(), 
            topic.capitalize(), name.capitalize(), 'hackNY')
    outfile.write(x + '\n')
    x = defn %  (definitions[0],definitions[1],definitions[2])
    outfile.write(x + '\n')
    for k in range(0,3*N-1,3):
        p = randint(1,3)
        if newsection == 3:
            if p == 1:
                x = lframe % ('\section{' + titles[i_title] + '}', '\subsection{' + 
                        captions[l] + '}', captions[l], text[k], text[k+1], text[k+2], photos[l])
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
                x = lframe % ('', '\subsection{' + captions[l] + '}', captions[l], text[k], 
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
    latex_cmd = 'pdflatex -output-directory tmp -interaction=batchmode tmp/output.tex'
    os.system(latex_cmd)
    os.system(latex_cmd)
    fatal = open('tmp/output.log').read().find('Fatal') # check for latex error
    if fatal == -1: # no error
        for x in os.listdir('tmp/'):
            if x not in {'.nothing', 'output.pdf'}: os.remove('tmp/' + x) 
        now = datetime.utcnow().strftime('%y%m%d%H%M%S')
        outfilename = '-'.join([name, topic, now]) + '.pdf'
        os.rename('tmp/output.pdf', 'static/' + outfilename)
        # if too many pdfs, get rid of oldest one
        pdfs = [pdf for pdf in os.listdir('static') if pdf[-3:] == 'pdf']
        oldest_pdf, oldest_age = '', 1e20
        if len(pdfs) > 5:
            for pdf in pdfs:
                age = os.stat('static/' + pdf).st_ctime 
                if age < oldest_age: 
                    oldest_pdf, oldest_age = pdf, age
            print('removing', oldest_pdf)
            os.remove('static/' + oldest_pdf)
    else: # don't delete temp files if error
        raise Exception('latex error')
    return outfilename

if __name__ == '__main__':
    topic = 'Tigers'
    name = 'Sean Kingston'
    photos = ['comics_Layer.jpg','comics_Layer.jpg','comics_Layer.jpg',
            'comics_Layer.jpg','comics_Layer.jpg']
    captions = ['one caption', 'two caption', 'three caption', 'four caption',
            'five caption']
    text = ['lots', 'of', 'friggin', 'text', 'so', 'much', 'text', 'loads of'
            'tigers', 'nine', 'i', 'love', 'tigers','who', 'does', 'not',
            'love', 'sean', 'kingston']
    titles = ['TITLE 1', 'TITLE 2', 'TITLE 3', 'TITLE 4', 'TITLE 5']
    definitions = ['james is awesome']
    presentation(topic, name, titles, photos, captions, text, definitions)
