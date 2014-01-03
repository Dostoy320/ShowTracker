#ShowTracker

####Create Database:
+ From root app directory, enter python shell
+ Type:
    + from showtracker import db
    + db.create_all()

####Work with API
+ From api_parser import MovieDatabase
+ Initialize session: sess = MovieDatabase()
+ Use methods: search/retrieve/seasons
+ Pretty Print: from pprint import pprint
    + pprint(result)

####TODO
+ Enable logging (to email?)




