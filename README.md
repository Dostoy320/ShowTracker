#ShowTracker
This app tracks progress through the seasons of television shows. The idea
 came to me after I downloaded all 110 episodes of Northern Exposure and 
struggled to keep track of my progress because I watched episodes often weeks, and sometimes months, apart.
For a while I just maintained a txt file, but I figured there had to be a better 
way.

The app uses the [The Movie Database](http://www.themoviedb.org/) API to retrieve
the data for a given show.

###Development stuff:
####Current stack:
+ flask (python web framework)
+ Jinja2 (HTML templating)
+ SQLAlchemy
+ Sass/Compass (css framework)


####Database creation:
+ In showtracker/config.py set `SQLALCHEMY_DATABASE_URI`
+ Then from /showtracker/: `python db_create.py`

####Work with The Movie Database API in the python shell:
+ `from api_parser import MovieDatabase`
+ Initialize session: `sess = MovieDatabase()`
+ Methods:
    + `search()`: takes string query to locate show ID on TMDB
    + `retrieve()`: takes the show ID to gather specifics such as number of seasons
    + `seasons()`: takes the show ID and a season number and returns episodes
+ Example case:
    + `>>> sess = MovieDatabase()`
    + `>>> show = sess.search('northern exposure')`
    + `>>> show = sess.retrieve(4396)`
    + `>>> season1 = sess.seasons(4396, 1)`
+ Pretty Print is nice for reading the results: `from pprint import pprint`
    + `pprint(season1)`


####ToDo:
+ <del>Fix signup validation to halt duplicate usernames</del>
+ <del>Tie users to specific shows - *This is huge. Figure it out!*</del>
+ <del> Prevent duplicate shows per user </del>
+ Stop neglecting tests
+ <del> Develop an environment where users can manipulate/delete shows/seasons/episodes </del>
+ <del>Check for existing show in database before adding duplicate</del>
+ Enable logging (to email?)
+ Work on styling with priority on mobile
+ date_watched




