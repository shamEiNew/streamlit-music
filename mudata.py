import spotipy, json, time
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from os import environ


def configure(user):
    """
    Client id and secret are defined as environmental variables.

    """
    scope = "playlist-modify-public"
    cs_id = environ['CLIENT_ID']
    cs_secret = environ['CLIENT_SECRET']

    client_credentials_manager = SpotifyClientCredentials(client_id=cs_id, client_secret=cs_secret)

    if user == 'user':return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = cs_id, client_secret = cs_secret,redirect_uri='http://localhost:8888/callback', scope=scope))
    return spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def collect_data(sp, name, data, decade, mid, y):
    l = []
    for i in range(0, len(data)):
        s = []
        songs_temp = {}
        t = {}
        m =[]
        if not data[i]['track']['album']['release_date'][:-6] or int(data[i]['track']['album']['release_date'][:-6]) > y: t['year'] = mid
        else:t['year'] = int(data[i]['track']['album']['release_date'][:-6])
        t['id'] = data[i]['track']['id']
        songs_temp['track_name'] = data[i]['track']['name']
        t['duration'] = data[i]['track']['duration_ms']
        f = sp.audio_features(data[i]['track']['id'])
        f = {k:f[0][k] for k in f[0].keys() if k not in ["type","id", "uri", "track_href","analysis_url","duration_ms","time_signature"]}
        t['properties'] = f
        s.append(t)
        songs_temp['features'] = s
        m.append(songs_temp)
        l.append({f'track_{i}': m})

    name[decade]=l

def initiate_collection(sp):
    #for i in range(0, len(data)):
    #    print(playlist['tracks']['items'][i]['track']['album']['release_date'][:-6])
    playlist_ids = ['37i9dQZF1DWTJ7xPn4vNaz', '37i9dQZF1DX4UtSsGT1Sbe', '0rZJqZmX61rQ4xMkmEWQar', '5tW8T4fK7DoTtLr8ordLpa','1tPWTwuxOLsE2Do1JQSUxA']
    name = {}
    year = 1970
    mid_year = 1975
    last_year = 1979
    for id in playlist_ids:
        playlist = sp.playlist(playlist_id = id)
        data = playlist['tracks']['items']
        collect_data(sp, name, data, f'{year}s', mid_year, last_year)
        mid_year += 10
        last_year += 10
        year += 10

    data_filtered = json.dumps(name, indent = 4)
    with open("music.json", "w") as outfile: 
        outfile.write(data_filtered)

def albums(sp, artist_name, artist_ids):
    start_time = time.time()
    for ids in artist_ids:
        
        """
        Included only studio albums due for simplification, anyway if needed we can change
        album type to None.
        In this we use the paging object 'next' described in the API. But it's
        slower as compared to the technique used in collect_data for decades because there we
        accessed values directly by keys. Moreover, this also calls track
        object, therefore expected to be slower. To fetch approx. 54 artist details it took 45 minutes
        in total. I haven't included the track popularity parameter as the most new tracks and
        singles will have always a higher number (this is also described in the api page).

        """
        artist_albums = sp.artist_albums(artist_id = ids, album_type=None,
                                        country=None, limit=50, offset=0)
        tracks_ids = []
        data_artists = {}
        albums_list = []

        while artist_albums:
            for _, album in enumerate(artist_albums['items']):
                    tracks  = sp.album_tracks(album['id'])
                    while tracks:
                        album_tracks = []
                        for __, track in enumerate(tracks['items']):
                            if track['id'] not in tracks_ids:
                                try:

                                    f = sp.audio_features(track['id'])
                                    f = {k:f[0][k] for k in f[0].keys() if k not in ["type","id", "uri", "track_href","analysis_url","duration_ms","time_signature"]}

                                    album_tracks.append({'track_name':track['name'],
                                                        'track_artists':track['artists'][0]['name'],
                                                        'track_id':track['id'], 'features':[f]})
                                except:

                                    print(f"Exception Occured for {track['name']}")

                                    with open('logfile.txt', 'a', encoding='utf-8') as log:
                                        log.write(f"Exception Occured for {track['name']}={track['id']}")
                                        log.write("\n")

                                    album_tracks.append({'track_name':track['name'],
                                                        'track_artists':track['artists'][0]['name'],
                                                        'track_id':track['id'], 'features':[None]})
                        
                        if tracks['next']:
                            tracks = sp.next(tracks)
                        else:
                            """
                            Need to call sp.album() as api endoint returns a simplied object
                            for the artist_albums which has no populartity key.
                            """
                            albums_list.append({'album_name': album['name'],'album_artists':album['artists'][0]['name'],'album_type':album['album_type'],'album_popularity':sp.album(album_id = album['id'])['popularity'], 'release_date': album['release_date'], 'tracks':album_tracks})
                            tracks = None
        
            if artist_albums['next']:
                artist_albums =  sp.next(artist_albums)
            else:
                artist_albums =  None
        """
        Albums get duplicated needed to remove a better block is needed here.
        """

        albums_list = list(set([json.dumps(i) for i in albums_list]))
        albums_list = [json.loads(i) for i in albums_list]

        data_artists['artist_name'] = artist_name
        data_artists['artist_id'] = ids
        data_artists['albums_full'] = albums_list

        print(time.time()-start_time)

        """
        Returning as list for each artist containing name, album details, and track details.
        
        """
        return [data_artists]
    
def get_artist_id(sp, artists_name):
    """
    To search artists and get their 'id' parameter for list of names.
    Also if needed we can add a new artist to the file artist_ids.json
    and then get further details and attach to our data file data_artists.json.
    """
    artist_ids = {}
    for name_string in artists_name:
        """
        Using exception as there is possibility of null result.
        """
        try:
            result = sp.search(q = 'artist:'+ name_string, type = 'artist')
            artist_ids[result['artists']['items'][0]['name']] = result['artists']['items'][0]['id']
        except:
            print(f'Not able to find:{name_string}')

    with open('music_data/artists_IN_ids.json','w', encoding='utf-8') as out:
        out.write(json.dumps(artist_ids, indent = 4))

def initiate_artists_data(sp):

    with open('music_data/artists_IN_ids.json', 'r', encoding='utf-8') as art:
        artist_ids_dict = json.load(art)

    #with open('music_data/testing.json', 'r', encoding='utf-8') as json_file:
    #    dict_art = json.load(json_file)

    peee = 0
    dict_art = {}
    for name in list(artist_ids_dict.keys())[::-1]:
        peee += 1
        print(f"{peee}: {name}")

        with open('logfile.txt', 'a', encoding='utf-8') as log:
            log.write(f"{peee}: {name}")
            log.write("\n")
        """
        Even single ids are passed in list because the code was changed at latter stage
        as passing the list to the above function was generating a 443 response
        so so passed as single parameters to prevent any further changes.
        """
        file_in = albums(sp, name, [artist_ids_dict[name]])
        dict_art[f'artist_{peee}'] = file_in

        with open('music_data/testing.json', 'w', encoding = 'utf-8') as file_out:
            file_out.write(json.dumps(dict_art, indent= 4))

    """
    Just for verification prints out album names in the entire file.
    """
    with open('music_data/testing.json', 'r', encoding= 'utf-8') as f:
       val = json.load(f)

    for key in val:
        for pee in range(0,len(val[key][0]['albums_full'])):
            print(val[key][0]['albums_full'][pee]['album_name'])