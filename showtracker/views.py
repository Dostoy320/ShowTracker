from showtracker import app, db
from models import Show, Episode
from api_parser import MovieDatabase
from flask import render_template, session, flash, redirect, url_for, \
    request, abort


@app.route('/')
def show_shows():
    shows = Show.query.all()
    episodes = Episode.query.all()
    return render_template('show_shows.html', shows=shows, episodes=episodes)


@app.route('/show_detail')
def show_detail():
    name = request.args.get('value')
    show = Show.query.filter_by(name=name).first()
    seasons = show.total_seasons
    season_object = []
    for season in range(seasons):
        single = Episode.query.filter_by(season=season).all()
        season_object.append(single)
    return render_template('show_detail.html', show=show, seasons=seasons,
                           season_object=season_object)


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
    # Connect to The Movie Database API
    api_session = MovieDatabase()
    result = api_session.retrieve(request.form['id'])
    new_show = Show(name=result['name'],
                    tmdb_id=request.form['id'],
                    total_seasons=result['number_of_seasons'])
    db.session.add(new_show)
    db.session.commit()
    show = Show.query.filter_by(name=result['name']).first()
    if result['number_of_seasons'] is None:
        seasons = 1
    else:
        seasons = result['number_of_seasons']
    # Add all seasons and episodes to database
    for season in range(seasons):
        result = api_session.seasons(request.form['id'], season)
        for episode in result.get('episodes'):
            new_episode = Episode(title=episode['name'],
                                  ep_number=episode['episode_number'],
                                  season=result['season_number'],
                                  show_id=show.id)
            db.session.add(new_episode)
    db.session.commit()
    flash('New show was successfully entered')
    return redirect(url_for('show_shows'))


@app.route('/search', methods=['POST'])
def search_show():
    if not session.get('logged_in'):
        abort(401)
    api_session = MovieDatabase()
    result = api_session.search(request.form['show_name'])
    return render_template('add_shows.html', choices=result)


@app.route('/retrieve_show')
def retrieve_show():
    api_session = MovieDatabase()
    result = api_session.retrieve(request.args.get('value'))
    seasons = result['number_of_seasons']
    return render_template('add_shows.html', show=result, seasons=seasons)


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
