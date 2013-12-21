from showtracker import app
from flask import render_template, g, session, flash, redirect, url_for, request


@app.route('/')
def show_shows():
    cur = g.db.execute('select show_name, seasons_total from shows order by show_id desc')
    shows = [dict(show_name=row[0], seasons_total=row[1]) for row in cur.fetchall()]
    return render_template('show_shows.html', shows=shows)

@app.route('/new')
def new_shows():
    return render_template('add_shows.html')

@app.route('/add', methods=['POST'])
def add_show():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into shows (show_name, seasons_total) values (?, ?)',
                    [request.form['show_name'], request.form['seasons_total']])
    g.db.commit()
    flash('New show was successfully entered')
    return redirect(url_for('show_shows'))

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
    return redirect(url_for('show_shows'))