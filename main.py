import sqlite3
import flask
import sys
from time import time
from tumblr import james, get_photos, get_captions, TumblrError
from wiki import getFacts
from latex import presentation
from udict import get_definitions
from flask import g

SECRET_KEY = 'KHY*&^jhgaaaaaa'
app = flask.Flask(__name__)
app.config.from_object(__name__)

def main():
    app.run(host='0.0.0.0')

@app.route('/')
def show_entries():
    g.db = connect_db()
    try:
        collection = query_db('select * from james')
    except:
        query_db('create table james (subject, name, url)')
    g.db.close()
    entries = [{'subject': p['subject'], 'name': p['name'], 'url': p['url']} for p in collection]
    return flask.render_template('template.html', entries=entries[:-6:-1])

@app.route('/add', methods=['POST'])
def add_entry():
    ''' grabs form data and passes it to latex_shite. if that works, add an
    entry to the database and let the user know. otherwise try to say
    something useful about the bajillion possible errors '''
    subject, name = flask.request.form['subject'], flask.request.form['name']
    msg = 'Presentr encountered an internal error. ' # flashed on webpage
    err = 'latex shite successful' # printed to log
    try:
        url = latex_shite(subject=subject, name=name)
    except KeyError as e:
        if e.message == 'query': # no wikipedia page for the subject
            msg += 'Try again, maybe with a different subject.'
            err = 'KeyError: query'
        else:
            err = 'KeyError: ' + e.message
    except TumblrError as e: # not enough photos or captions
        msg += e.value
        err = 'tumblr error ' + e.value
    except: # prevent from crashing. comment this out for development
        err = str(sys.exc_info())
        msg += err
    else:
        g.db = connect_db()
        args = [subject, name, url]
        collection = query_db('insert into james values (?,?,?)', args)
        g.db.commit()
        g.db.close()
        msg = 'Success! Download your pReSeNtRation below.'
    finally:
        print(err)
        flask.flash(msg)
    return flask.redirect(flask.url_for('show_entries'))

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def connect_db():
    return sqlite3.connect('db.db')

def latex_shite(subject='tiger', name='james'):
    ''' does these things:
    1. gets photos and captions from tumblr
    2. gets titles and text from wikipedia
    3. gets definition from urban dictionary
    4. assembles them into beamer latex presentation '''
    print('doing latex shite. topic: %s name: %s' % (subject, name))
    num_photos, num_captions, num_titles, num_sentences = 9, 9, 3, 30
    t0 = time()
    tumblr_response = james(limit=20, tag=subject)['response']
    photos = get_photos(tumblr_response, limit=num_photos)
    print('photos:', len(photos))
    captions = get_captions(tumblr_response, subject, limit=num_captions)
    print('captions:', len(captions))
    t1 = time()
    titles, text = getFacts(subject, num_titles=num_titles, num_sentences=num_sentences)
    t2 = time()
    definitions = get_definitions(subject)
    t3 = time()
    url = presentation(subject, name, titles, photos, captions, text, definitions)
    t4 = time()
    print('tumblr:', t1-t0)
    print('wiki:', t2-t1)
    print('urbandictionary:', t3-t2)
    print('latex:', t4-t3)
    return url

if __name__ == '__main__':
    main()
