# -*- coding: utf-8 -*-

import mongokit
import flask
import sys
from datetime import datetime
from time import time
from tumblr import james, get_photos, get_captions
from wiki import getFacts
from latex import presentation

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
    entries = [dict(project=p['project'], name=p['name']) for p in collection]
    return flask.render_template('template.html', entries=entries[:-6:-1])

@app.route('/add', methods=['POST'])
def add_entry():
    collection = db_stuff()
    project, name = flask.request.form['project'], flask.request.form['name']
    latex_shite(subject=project, name=name)
    collection.insert({'project': project, 'name': name, 'date': datetime.utcnow()})
    flask.flash('New entry was successfully posted')
   # try:
   #     latex_shite(subject=project, name=name)
   # except:
   #     print sys.exc_info()
   #     flask.flash('failed to create slides: %s' % str(sys.exc_info()))
   # else:
   #     collection.insert({'project': project, 'name': name, 'date': datetime.utcnow()})
   #     flask.flash('New entry was successfully posted')
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
    captions = get_captions(tumblr_response, limit=9)
    for i, caption in enumerate(captions):
        print i, caption
    t1 = time()
    titles, text = getFacts(subject, num_titles=3, num_sentences=30)
    t2 = time()
    presentation(subject, name, titles, photos, captions, text)
    t3 = time()
    print 'tumblr:', t1-t0
    print 'wiki:', t2-t1
    print 'latex:', t3-t2

if __name__ == '__main__':
    main()
