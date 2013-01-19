import pylast
import collections
from pylast import User

API_KEY = 'c6a94d5558b187f5f263f8cdf743c331'
API_SECRET = '27c72fbdd022fe8bf5978d5fc7aa7359'


def getLove(login):
    network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
        API_SECRET, username = login)
        
    user = User(login, network)
    loved = user.get_loved_tracks()

    result = ''
    for lsong in loved:
        track = lsong.track
        result += track.get_title() + ' ' + lsong.date + '<p>'
    return result
