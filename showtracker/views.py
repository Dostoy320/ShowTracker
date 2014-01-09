from showtracker import app, db
from models import ROLE_USER, User, Show, Episode
from forms import SignupForm, LoginForm, AddShow
from api_parser import MovieDatabase
from flask import render_template, session, flash, redirect, url_for, \
    request, abort, jsonify


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
    episodes = Episode.query.filter_by(show_id=show.id).all()
    return render_template('show_detail.html', show=show, seasons=seasons,
                           episodes=episodes)


@app.route('/episode_detail')
def episode_detail():
    show_id = request.args.get('id')
    season = request.args.get('season')
    episodes = Episode.query.filter_by(
        show_id=show_id).filter_by(season=season).all()
    if episodes != "":
        episodes_d = {}
        for i, episode in enumerate(episodes):
            episodes_d[i] = [episode.title, episode.id, episode.watched]
            print "episodes: ", episodes_d
    return jsonify(episodes_d)


@app.route('/episode_status')
def episode_status():
    episode_id = request.args.get('ep_id')
    status = request.args.get('status')
    query = Episode.query.filter_by(id=episode_id).first()
    if status == "watched":
        query.watched = True
        result = {"watched": "true"}
    else:
        query.watched = False
        result = {"watched": "false"}
    db.session.commit()
    return jsonify(result)


@app.route('/new', methods=['GET', 'POST'])
def new_show():
    form = AddShow()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('add_shows.html', form=form)
        else:
            api_session = MovieDatabase()
            result = api_session.search(form.show_name.data)
            return render_template('add_shows.html', form=form, choices=result)
    elif request.method == 'GET':
        return render_template('add_shows.html', form=form)


@app.route('/retrieve_show')
def retrieve_show():
    api_session = MovieDatabase()
    result = api_session.retrieve(request.args.get('value'))
    form = AddShow(show_id=result['id'])
    seasons = result['number_of_seasons']
    return render_template('add_shows.html', show=result, seasons=seasons,
                           form=form)


@app.route('/add', methods=['POST'])
def add_show():
    form = AddShow()
    if not session.get('username'):
        abort(401)
    # Connect to The Movie Database API and retrieve show data
    api_session = MovieDatabase()
    result = api_session.retrieve(form.show_id.data)

    # Update Show table
    new_show = Show(name=result['name'],
                    tmdb_id=form.show_id.data)
                   # total_seasons=seasons)
    db.session.add(new_show)
    db.session.commit()

    show = Show.query.filter_by(name=result['name']).first()

    # TMDB's "number_of_seasons" isn't accurate, so the number of seasons must
    # be determined by the iterations through the list of seasons.
    season_tally = 0
    for season in result.get('seasons'):
        print season['season_number']
        current = api_session.seasons(form.show_id.data,
                                      season['season_number'])
        for episode in current.get('episodes'):
            new_episode = Episode(title=episode['name'],
                                  ep_number=episode['episode_number'],
                                  season=season['season_number'],
                                  show_id=show.id)
            db.session.add(new_episode)
        season_tally += 1
    new_show.total_seasons = season_tally
    db.session.commit()
    flash('New show was successfully entered')
    return redirect(url_for('show_shows'))


@app.route('/new_eps')
def new_episodes():
    retrieve = request.args.get('value')
    show = Show.query.filter_by(name=retrieve).first()
    return render_template('add_episodes.html', show=show)


@app.route('/search', methods=['POST'])
def search_show():
    if not session.get('username'):
        abort(401)
    api_session = MovieDatabase()
    result = api_session.search(request.form['show_name'])
    return render_template('add_shows.html', choices=result)





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
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('login.html', form=form)
        else:
            session['username'] = form.username.data
            return redirect(url_for('show_shows'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect(url_for('login'))

    session.pop('username', None)
    return redirect(url_for('show_shows'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('signup.html', form=form)
        else:
            new_user = User(form.username.data, form.email.data,
                            form.password.data, ROLE_USER)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('show_shows'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)
