import json
from google.appengine.api import urlfetch

API_KEY = 'c6a94d5558b187f5f263f8cdf743c331'

def process_loved_tracks(login):
    request = ('http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks' + '&user=' + login +
                '&api_key=' + API_KEY +  '&format=json') # составляем строку запроса 
    response = urlfetch.fetch(request, deadline=60) # делаем запрос с помощью библиотеки urlfetch
    data = json.loads(response.content) # json-парсером считываем ответ в "словарь"
    total_tracks_count = int(data['lovedtracks']['@attr']['total']) # читаем данные из словаря
    total_pages = int(data['lovedtracks']['@attr']['totalPages'])

    zero_tracks = []
    for page in range(1, total_pages + 1):
        request = ('http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks' + '&user=' + login +
                   '&api_key=' + API_KEY + '&page=' + str(page) + '&format=json')
        response = urlfetch.fetch(request, deadline=60)
        data = json.loads(response.content)
        for track in data['lovedtracks']['track']:
            title = track['name']
            artist = track['artist']['name']
            title = title.replace(' ', '+')
            artist = artist.replace(' ', '+')
            pcrequest = ('http://ws.audioscrobbler.com/2.0/?method=track.getInfo' + '&track=' + title +
                         '&artist=' + artist + '&api_key=' + API_KEY + '&username=' + login + '&format=json')
            pcresponse = urlfetch.fetch(pcrequest, deadline=60)
            pcdata = json.loads(pcresponse.content)
            if not 'userplaycount' in pcdata['track'] or pcdata['track']['userplaycount']=='0':
                zero_tracks.append(track)
    total_tracks_count -= len(zero_tracks)
    return total_tracks_count, zero_tracks


def find_loved_tracks(login, total_count):
    request = ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks' + '&user=' + login +
               '&api_key=' + API_KEY + '&format=json')
    response = urlfetch.fetch(request, deadline=60)
    data = json.loads(response.content)
    total_pages = int(data['recenttracks']['@attr']['totalPages'])

    loved_tracks_names = []
    loved_tracks = []
    for page in range(1, total_pages + 1):
        request = ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks' + '&user=' + login +
                   '&api_key=' + API_KEY + '&limit=200' + '&page=' + str(page) + '&extended=1' + '&format=json')
        response = urlfetch.fetch(request, deadline=60)
        data = json.loads(response.content)
        for track in data['recenttracks']['track']:
            if track['loved']=='1':
                trackname = track['artist']['name'].lower()+track['name'].lower()
                if loved_tracks_names.count(trackname)==0:
                    loved_tracks.append(track)
                    loved_tracks_names.append(trackname)
                    if len(loved_tracks)==total_count:
                        return loved_tracks

def getInfo(login):
    result = []
    total_tracks_count, zero_tracks = process_loved_tracks(login)
    print zero_tracks
    if not len(zero_tracks) == 0:
        for track in zero_tracks:
            track['date']['#text'] = 'No Date'
        result = zero_tracks

    loved_tracks = find_loved_tracks(login, total_tracks_count)
    loved_tracks.reverse()
    result.extend(loved_tracks)
    return result
