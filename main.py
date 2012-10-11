import sqlite3
import flask
import sys
from time import time
from tumblr import james, get_photos, get_captions
from wiki import getFacts
from latex import presentation
from udict import get_definitions
from flask import g

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
    g.db = connect_db()
    collection = query_db('select * from james')
    g.db.close()
    entries = [{'subject': p['subject'], 'name': p['name'], 'url': p['url']} for p in collection]
    return flask.render_template('template.html', entries=entries[:-6:-1])

@app.route('/add', methods=['POST'])
def add_entry():
    subject, name = flask.request.form['subject'], flask.request.form['name']
    try:
        url = latex_shite(subject=subject, name=name)
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
        g.db = connect_db()
        args = [subject, name, url]
        collection = query_db('insert into james values (?,?,?)', args)
        g.db.commit()
        flask.flash('Success! Download your pReSeNtRation below.')
        g.db.close()
    return flask.redirect(flask.url_for('show_entries'))

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def connect_db():
    return sqlite3.connect('db.db')

def latex_shite(subject='tiger', name='james'):
    t0 = time()
    tumblr_response = james(limit=20, tag=subject)['response']
    photos = get_photos(tumblr_response, limit=9)
    for photo in photos:
        print photo
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
