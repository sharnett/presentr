from random import randint
import os

topic = 'Tigers'
name = 'Sean Kingston'
photos = ['comics_Layer.jpg','comics_Layer.jpg','comics_Layer.jpg', 'comics_Layer.jpg','comics_Layer.jpg']
captions = ['one caption', 'two caption', 'three caption', 'four caption', 'five caption']
text = ['lots', 'of', 'friggin', 'text', 'so', 'much', 'text', 'loads of tigers', 'nine', 'i', 'love', 'tigers','who', 'does', 'not', 'love', 'sean', 'kingston']
titles = ['TITLE 1', 'TITLE 2', 'TITLE 3', 'TITLE 4', 'TITLE 5']

def presentation(topic, name, titles, photos, captions, text):

	N = 5
	l = 0
	newsection = 3

	outfile = open('output.tex','w')

	intro = open('introduction.txt').read()
	lframe = open('frameleft.txt').read()
	rframe = open('frameright.txt').read()
	mframe = open('framemiddle.txt').read()
	concl = open('conclusion.txt').read()

	x = intro % (topic, topic, name, 'hackNY')
	outfile.write(x + '\n')

	for k in xrange(0,3*N,3):
	
		p = randint(1,3)

		if newsection == 3:
			if p == 1:
				x = lframe % ('\section{' + titles[l] + '}', '\subsection{' + captions[l] + '}', captions[l], text[k], text[k+1], text[k+2], photos[l])
				outfile.write(x + '\n')
			elif p == 2:
                		x = rframe % ('\section{' + titles[l] + '}', '\subsection{' + captions[l] + '}', captions[l], photos[l], text[k], text[k+1], text[k+2])
                		outfile.write(x + '\n')
			else :
                		x = mframe % ('\section{' + titles[l] + '}', '\subsection{' + captions[l] + '}', captions[l], photos[l])
                		outfile.write(x + '\n')
			newsection = 1
		else:
                        if p == 1:
                                x = lframe % ('', '\subsection{' + captions[l] + '}', captions[l], text[k], text[k+1], text[k+2], photos[l])
                                outfile.write(x + '\n')
                        elif p == 2:
                                x = rframe % ('', '\subsection{' + captions[l] + '}', captions[l], photos[l], text[k], text[k+1], text[k+2])
                                outfile.write(x + '\n')
                        else :
                                x = mframe % ('', '\subsection{' + captions[l] + '}', captions[l], photos[l])
                                outfile.write(x + '\n')
			newsection += 1
		
		l += 1
		print('l',l)
		print('newsection',newsection)
	x = concl % (text[N+1],text[N+2],text[N+2])
	outfile.write(x)

	outfile.close()

presentation(topic, name, titles, photos, captions, text)

os.system('pdflatex output.tex')
os.system('pdflatex output.tex')
os.system('evince output.pdf')
