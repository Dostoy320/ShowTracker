# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from contextlib import closing

# configuration
# TODO: move configuration to own file
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'temp key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

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

# Views:

@app.route('/')
def show_shows():
    cur = g.db.execute('select show, season, ep_number from shows order by id desc')
    programs = [dict(show=row[0], season=row[1], ep_number=row[2]) for row in cur.fetchall()]
    return render_template('show_shows.html', programs=programs)

@app.route('/add', methods=['POST'])
def add_show():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into shows (show, season, ep_number, ep_title) values (?, ?, ?, ?)',
                    [request.form['show'], request.form['season'],
                    request.form['ep_number'], request.form['text']])
    g.db.commit()
    flash('New show was successfully entered')
    return redirect(url_for('show_shows.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_shows'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
