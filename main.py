import mongokit
import flask
from datetime import datetime

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
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    collection = db_stuff().find()
    entries = [dict(project=p['project'], name=p['name']) for p in collection]
    return flask.render_template('template.html', entries=reversed(entries))

@app.route('/add', methods=['POST'])
def add_entry():
    collection = db_stuff()
    collection.insert(dict(project=flask.request.form['project'], 
        name=flask.request.form['name'], date=datetime.utcnow()))
    flask.flash('New entry was successfully posted')
    return flask.redirect(flask.url_for('show_entries'))

def db_stuff():
    connection = mongokit.Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
    db = connection['james']
    collection = db.projects
    return collection

if __name__ == '__main__':
    main()
