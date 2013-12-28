from showtracker import db


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    total_seasons = db.Column(db.Integer)
    eps_per_season = db.Column(db.Integer)
    episodes = db.relationship('Episode', backref='series')

    def __repr__(self):
        return "<Show(name='%s', total_seasons='%s')>" % (self.name,
            self.total_seasons)


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    season = db.Column(db.Integer)
    watched = db.Column(db.Boolean, default=False)
    date_watched = db.Column(db.DateTime)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))

    def __repr__(self):
        return "<Episode(title='%s', season='%s', date watched='%s')>" % (
            self.title, self.season, self.date_watched)
