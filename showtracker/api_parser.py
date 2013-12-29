from tmdbsimple import TMDB
from keys import tmdb_key


class MovieDatabase:
    def __init__(self):
        self.tmdb = TMDB(tmdb_key)

    def search(self, query):
        search = self.tmdb.Search()
        tv = search.tv({'query': query})
        result = tv['results']
        return result

    def retrieve(self, query):
        tv = self.tmdb.TV(query)
        result = tv.info()
        return result

    def seasons(self, query, season):
        tv = self.tmdb.TV_Seasons(query, season)
        result = tv.info()
        return result
