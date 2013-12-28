from showtracker import app, db
from models import Show, Episode
from imdb_parser import imdbapi_interface
from flask import render_template, g, session, flash, redirect, url_for, \
    request, abort


@app.route('/')
def show_shows():
    shows = Show.query.all()
    episodes = Episode.query.all()
    return render_template('show_shows.html', shows=shows, episodes=episodes)


@app.route('/new')
def new_show():
    return render_template('add_shows.html')


@app.route('/new_eps')
def new_episodes():
    retrieve = request.args.get('value')
    show = Show.query.filter_by(name=retrieve).first()
    return render_template('add_episodes.html', show=show)


@app.route('/add', methods=['POST'])
def add_show():
    if not session.get('logged_in'):
        abort(401)
    new_show = Show(name=request.form['show_name'],
                    total_seasons=request.form['seasons_total'])
    db.session.add(new_show)
    db.session.commit()
    flash('New show was successfully entered')
    return redirect(url_for('show_shows'))

# Under Construction--------------------------------


@app.route('/search', methods=['POST'])
def search_show():
    if not session.get('logged_in'):
        abort(401)
    data = imdbapi_interface(request.form['show_name'])
    if data is None:
        flash('Sorry, no results with that name.')
        return render_template('add_shows.html')
    elif data.keys() == [u'shows']:
            multiple_choices = data[data.keys()[0]]
            return render_template('add_shows.html', choices=multiple_choices)
    else:
        episodes = data[data.keys()[0]]['episodes']
        return render_template('add_shows.html', episodes=episodes)


@app.route('/add_eps', methods=['POST'])
def add_eps():
    new_episode = Episode(title=request.form['ep_title'],
                          season=request.form['season'],
                          show_id=request.form['id'])
    db.session.add(new_episode)
    db.session.commit()
    flash('Episode entered successfully')
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
