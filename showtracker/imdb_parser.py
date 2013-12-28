import httplib
import json

# TODO: rewrite using urllib2 rather than httplib
#       switch to themoviedb api - http://docs.themoviedb.apiary.io/#tv
#       use this library: https://pypi.python.org/pypi/tmdbsimple


def imdbapi_interface(query):
    name = query.replace(" ", "+")
    connection = httplib.HTTPConnection("imdbapi.poromenos.org")
    connection.request("GET", "/js/?name=%s" % name)
    response = connection.getresponse()
    if response.status == 200:
        data = json.loads(response.read())
        return data
        #data = json.loads(resp.read())
        ## A response with multiple shows begins with the key 'shows'
        #if data.keys() == [u'shows']:
            #for show in data['shows']:
                #years.append(show)
            #return years
        ## If the response is a single show, return the episode list
        #else:
            #slim = data[data.keys()[0]]['episodes']
            #return slim
    else:
        return "Connection Failed."

# Use type(x) is list/dict to respond to return

#find number of seasons
#next((item for item in data if item['season'] == x), None)
