from showtracker import db
from showtracker.models import *
from showtracker.api_parser import MovieDatabase

# Create API interface instance:
sess = MovieDatabase()

# Retrieve total number of shows from ST database:
rows = Show.query.all()

# Cycle through shows in ST database:
for row in rows:
    # Access MovieDatabase and get show by its MovieDatabase ID
    show = sess.retrieve(row.tmdb_id)

    #Get the last season by selecting the last position in the array of seasons
    season = sess.seasons(row.tmdb_id, show['seasons'][-1]['season_number'])
    tmdb_last_season_episodes = len(season['episodes'])
    print tmdb_last_season_episodes

    database_episodes = Episode.query.filter_by(show_id=row.id) \
        .filter_by(season=season['season_number']).all()

    ST_last_season_episodes = len(database_episodes)
    print ST_last_season_episodes

    curr_eps = season['episodes']

    # If there are less episodes in the ST database than on the MovieDatabase:
    if ST_last_season_episodes < tmdb_last_season_episodes:

        ep_number = ST_last_season_episodes
        while ep_number < tmdb_last_season_episodes:
            new_episode = Episode(title=curr_eps[ep_number]['name'],
                                  ep_number=curr_eps[ep_number]
                                  ['episode_number'],
                                  ep_overview=curr_eps[ep_number]['overview'],
                                  season=season['season_number'],
                                  show_id=row.id)
            db.session.add(new_episode)
            db.session.commit()

            # Retrieve freshly committed episode:
            committed_episode = Episode.query \
                .filter_by(ep_number=curr_eps[ep_number]['episode_number']) \
                .filter_by(show_id=row.id).first()

            #print committed_episode.id
            users_tracking = UserShows.query.filter_by(show=row.id).all()
            print "This is the first user:"
            print users_tracking[0].user
            for user in users_tracking:
                user_episode = UserEpisodes(user=user.user,
                                            episode_id=committed_episode.id)
                print user_episode

                db.session.add(user_episode)
                db.session.commit()
                print user_episode.id

            # Increment to next missing episode
            ep_number = ep_number + 1
            print "========================================="
        db.session.commit()

    print "--------------------------------"
