import mongokit
import flask

DEBUG = True
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = flask.Flask(__name__)
app.config.from_object(__name__)

def main():
    app.run()

@app.route('/')
def show_entries():
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    collection = db_stuff().find()
    entries = [dict(title=p['project'], text=p['name']) for p in collection]
    print entries
    return flask.render_template('template.html', entries=entries)

def db_stuff():
    connection = mongokit.Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
    db = connection['james']
    collection = db.projects
    return collection

if __name__ == '__main__':
    main()
