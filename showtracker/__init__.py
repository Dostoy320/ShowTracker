# imports
import sqlite3
from flask import Flask, g, abort
from contextlib import closing

# configuration
# TODO: move configuration to own file
DATABASE = 'showtracker/tmp/tracker.db'
DEBUG = True
SECRET_KEY = 'temp key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

import showtracker.views



# Database stuff:

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()





if __name__ == '__main__':
    app.run()
