from showtracker import db
from werkzeug import generate_password_hash, check_password_hash

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pwdhash = db.Column(db.String(120), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __init__(self, username, email, password, role):
        self.username = username.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return "<User %s>" % (self.username)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    tmdb_id = db.Column(db.Integer)
    total_seasons = db.Column(db.Integer)
    episodes = db.relationship('Episode', backref='series')
    usershows = db.relationship('UserShows', backref='series')

    def __repr__(self):
        return "<Show(name='%s', total_seasons='%s')>" % (self.name,
                                                          self.total_seasons)


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    ep_number = db.Column(db.Integer)
    season = db.Column(db.Integer)
    watched = db.Column(db.Boolean, default=False)
    date_watched = db.Column(db.DateTime)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    userepisodes = db.relationship('UserEpisodes', backref='episode')

    def __repr__(self):
        return "<Episode(title='%s', season='%s', date watched='%s')>" % (
            self.title, self.season, self.date_watched)


class UserShows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    show = db.Column(db.Integer, db.ForeignKey('show.id'))

    def __repr__(self):
        return "<UserShows(user='%s', show='%s')>" % (self.user, self.show)


class UserEpisodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))
    watched = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<UserEpisodes(user'%s', episode='%s', watched='%s')>" % (
            self.user, self.episode_id, self.watched)
