from showtracker import app, db
from models import ROLE_USER, User, Show, Episode, UserShows, UserEpisodes
from forms import SignupForm, LoginForm, AddShow
from api_parser import MovieDatabase
from urllib import urlencode
from datetime import datetime
from flask import render_template, session, flash, redirect, url_for, \
    request, abort, jsonify


@app.route('/test')
def test_page():
    return render_template('test_page.html')


@app.route('/')
def show_shows():
    if session.get('username'):
        user = User.query.filter_by(username=session.get('username')).first()
        usershows = UserShows.query.filter_by(user=user.id).all()
        shows = []
        for show in usershows:
            shows.append(show.series)
        return render_template('show_shows.html', shows=shows)
    else:
        return render_template('welcome.html')


@app.route('/show_detail')
def show_detail():
    show_id = request.args.get('value')
    show = Show.query.filter_by(id=show_id).first()
    seasons = show.total_seasons
    episodes = Episode.query.filter_by(show_id=show.id).all()
    return render_template('show_detail.html', show=show, seasons=seasons,
                           episodes=episodes)


@app.route('/episode_detail')
def episode_detail():
    user_id = session.get('id')
    show_id = request.args.get('id')
    season = request.args.get('season')
    episodes = UserEpisodes.query \
        .filter_by(user=user_id).join(UserEpisodes.episode) \
        .filter_by(show_id=show_id).filter_by(season=season).all()
    if episodes != "":
        episodes_d = {}
        for i, episode in enumerate(episodes):
            episodes_d[i] = [episode.episode.title,
                             episode.episode.id,
                             episode.watched]
            print "episodes: ", episodes_d
    return jsonify(episodes_d)


@app.route('/episode_overview')
def episode_overview():
    user_id = session.get('id')
    ep_number = request.args.get('ep_number')
    episode = Episode.query.filter_by(id=ep_number).first()

    # Query UserEpisodes to get episode rating
    user_episode = UserEpisodes.query \
        .filter_by(user=user_id) \
        .filter_by(episode_id=ep_number).first()
    episode_info = {}
    if episode.ep_overview == "":
        episode_info[0] = "Sorry, no overview available."
        episode_info[1] = user_episode.rating
    else:
        episode_info[0] = episode.ep_overview
        episode_info[1] = user_episode.rating
        #episode_info[1] = 3
    return jsonify(episode_info)

# These ajax routes should have methods specified!!!!
# So do that.


@app.route('/episode_rating')
def episode_rating():
    user_id = session.get('id')
    ep_number = request.args.get('ep_number')
    rating = request.args.get('ep_rating')
    user_episode = UserEpisodes.query \
        .filter_by(user=user_id) \
        .filter_by(episode_id=ep_number).first()
    # Update query with new rating value
    user_episode.rating = rating
    # If this is  the first time rating, set this:
    if user_episode.watched is False:
        user_episode.watched = True
        user_episode.date_watched = datetime.now()

    db.session.commit()
    # return the new value
    success = {}
    success[0] = user_episode.rating

    return jsonify(success)

# Unused route??????
#
# @app.route('/episode_status')
# def episode_status():
#     user = User.query.filter_by(username=session.get('username')).first()
#     episode_id = request.args.get('ep_id')
#     status = request.args.get('status')
#     query = UserEpisodes.query \
#         .filter_by(episode_id=episode_id) \
#         .filter_by(user=user.id).first()
#     if status == "watched":
#         query.watched = True
#         query.date_watched = datetime.now()
#         result = {"watched": "true"}
#     else:
#         query.watched = False
#         result = {"watched": "false"}
#     db.session.commit()
#     return jsonify(result)


@app.route('/new', methods=['GET', 'POST'])
def new_show():
    form = AddShow()
    if not session.get('username'):
        abort(401)
    if request.method == 'POST':
        if form.validate() is False:
            return render_template('add_shows.html', form=form)
        else:
            api_session = MovieDatabase()
            result = api_session.search(form.show_name.data)
            # Send "empty" variable to trigger no results message in template
            if result == []:
                return render_template('add_shows.html',
                                       form=form, empty="empty")
            else:
                return render_template('add_shows.html',
                                       form=form, choices=result)
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
    # Check for duplicate show within a specific user
    if form.validate_unique() is False:
            message = "You already follow this show."
            return render_template('add_shows.html', message=message, form=form)
    # Check if requested show already exists in database:
    existing_show = Show.query.filter_by(tmdb_id=form.show_id.data).first()
    if existing_show:
        user = User.query.filter_by(username=session.get('username')).first()
        add_show = UserShows(user=user.id,
                             show=existing_show.id)
        for episode in existing_show.episodes:
            add_episode = UserEpisodes(user=user.id,
                                       episode_id=episode.id)
            db.session.add(add_episode)
        db.session.add(add_show)
        db.session.commit()
        flash('New show was successfully entered')
        return redirect(url_for('show_shows'))
    else:
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

        # TMDB's "number_of_seasons" isn't accurate, so the number of seasons
        # must be determined by the iterations through the list of seasons.
        season_tally = 0
        for season in result.get('seasons'):
            # Some API results include a None season
            # "This Old House", for example...
            if season['season_number'] is None:
                pass
            else:
                print season['season_number']
                current = api_session.seasons(form.show_id.data,
                                              season['season_number'])
                for episode in current.get('episodes'):
                    new_episode = Episode(title=episode['name'],
                                          ep_number=episode['episode_number'],
                                          ep_overview=episode['overview'],
                                          season=season['season_number'],
                                          show_id=show.id)
                    db.session.add(new_episode)
                season_tally += 1
        new_show.total_seasons = season_tally
        db.session.commit()

        #TODO: This stuff below is repeated above.  Clean up?
        user = User.query.filter_by(username=session.get('username')).first()
        add_show = UserShows(user=user.id,
                             show=show.id)
        for episode in show.episodes:
            add_episode = UserEpisodes(user=user.id,
                                       episode_id=episode.id)
            db.session.add(add_episode)
        db.session.add(add_show)
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


# Routes to handle user signup/login/admin:

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
            session['new_user'] = form.username.data
            return redirect(url_for('login', new_user=new_user))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('login.html', form=form)
        else:
            # Get the case-correct username for session use
            username = User.query.filter(User.username.ilike
                                        (form.username.data)).first()
            session['username'] = username.username
            session['id'] = username.id

            flash('You are logged in.')
            return redirect(url_for('show_shows'))
    if session.get('new_user'):
        new_user = session['new_user']
        session.pop('new_user', None)
        return render_template('login.html', form=form, new_user=new_user)
    if request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect(url_for('login'))

    session.pop('username', None)
    return redirect(url_for('show_shows'))


@app.route('/admin', methods=['GET'])
def admin():
    print request.method
    if 'username' not in session:
        return redirect(url_for('login'))
    elif request.values['action'] == 'landing':
        print "Landing"
        return render_template('admin.html')
    # List user's shows for possible deletion
    elif request.values['action'] == 'get_shows':
        user = User.query.filter_by(username=session.get('username')).first()
        usershows = UserShows.query.filter_by(user=user.id).all()
        shows = []
        # Collect series name and UserShow id (as opposed to series id)
        for show in usershows:
            shows.append({
                'name': show.series.name,
                'usershow_id': show.id
            })
        return render_template('admin.html', shows=shows)
    # Delete show records from UserShows and UserEpisodes tables
    elif request.values['action'] == 'delete_show':
        user = User.query.filter_by(username=session.get('username')).first()
        usershow = UserShows.query.filter_by(id=request.values['id']).first()

        # Get all UserEpisodes for a particular user, then narrow by show id
        to_delete = UserEpisodes.query.filter_by(user=user.id) \
            .join(UserEpisodes.episode).filter_by(show_id=usershow.show).all()

        for row in to_delete:
            db.session.delete(row)
        db.session.delete(usershow)
        db.session.commit()

        # Repopulate show list
        usershows = UserShows.query.filter_by(user=user.id).all()
        shows = []
        # Collect series name and UserShow id (as opposed to series id)
        for show in usershows:
            shows.append({
                'name': show.series.name,
                'usershow_id': show.id
            })
        return render_template('admin.html', shows=shows)
    # Delete user, end session and land on Welcome screen
    elif request.values['action'] == 'delete_user':
        user = User.query.filter_by(username=session.get('username')).first()
        shows = UserShows.query.filter_by(user=user.id).all()
        episodes = UserEpisodes.query.filter_by(user=user.id).all()
        for row in episodes:
            db.session.delete(row)
        for row in shows:
            db.session.delete(row)
        db.session.delete(user)
        db.session.commit()
        session.pop('username', None)
        return render_template('welcome.html')
