# -*- coding: utf-8 -*-

import mongokit
import flask
from datetime import datetime
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
    return flask.render_template('template.html', entries=reversed(entries))

@app.route('/add', methods=['POST'])
def add_entry():
    collection = db_stuff()
    project, name = flask.request.form['project'], flask.request.form['name']
    latex_shite(subject=project, name=name)
    collection.insert({'project': project, 'name': name, 'date': datetime.utcnow()})
    flask.flash('New entry was successfully posted')
    return flask.redirect(flask.url_for('show_entries'))

def db_stuff():
    connection = mongokit.Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
    db = connection['james']
    collection = db.projects
    return collection

def latex_shite(subject='tiger', name='james'):
    tumblr_response = james(limit=20, tag=subject)['response']
    photos = get_photos(tumblr_response, limit=9)
    captions = get_captions(tumblr_response, limit=9)
    titles, text = getFacts(subject, num_titles=3, num_sentences=30)
    presentation(subject, name, titles, photos, captions, text)

if __name__ == '__main__':
    main()
