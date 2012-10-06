# -*- coding: utf-8 -*-

import mongokit
import flask
import sys
from time import time
from tumblr import james, get_photos, get_captions
from wiki import getFacts
from latex import presentation
from udict import get_definitions

DEBUG = True
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
SECRET_KEY = 'secret'

app = flask.Flask(__name__)
app.config.from_object(__name__)

def main():
    app.run()

@app.route('/')
def show_entries():
    collection = db_stuff().find()
    entries = [{'project': p['project'], 'name': p['name'], 'url': p['url']} for p in collection]
    return flask.render_template('template.html', entries=entries[:-6:-1])

@app.route('/add', methods=['POST'])
def add_entry():
    collection = db_stuff()
    project, name = flask.request.form['project'], flask.request.form['name']
    try:
        url = latex_shite(subject=project, name=name)
    except KeyError as e:
        if e.message == 'query':
            flask.flash('Presentr encountered an internal error. Try again,'
                        ' maybe with a different subject.')
        else:
            raise e
   # except:
   #     print sys.exc_info()
   #     flask.flash('failed to create slides: %s' % str(sys.exc_info()))
    else:
        collection.insert({'project': project, 'name': name, 'url': url})
        flask.flash('Success! Download your pReSeNtRation below.')
    return flask.redirect(flask.url_for('show_entries'))

def db_stuff():
    connection = mongokit.Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
    db = connection['james']
    collection = db.projects
    return collection

def latex_shite(subject='tiger', name='james'):
    t0 = time()
    tumblr_response = james(limit=20, tag=subject)['response']
    photos = get_photos(tumblr_response, limit=9)
    captions = get_captions(tumblr_response, subject, limit=9)
    for i, caption in enumerate(captions):
        print i, caption
    t1 = time()
    titles, text = getFacts(subject, num_titles=3, num_sentences=30)
    t2 = time()
    definitions = get_definitions(subject)
    t3 = time()
    url = presentation(subject, name, titles, photos, captions, text, definitions)
    t4 = time()
    print 'tumblr:', t1-t0
    print 'wiki:', t2-t1
    print 'urbandictionary:', t3-t2
    print 'latex:', t4-t3
    return url

if __name__ == '__main__':
    main()
