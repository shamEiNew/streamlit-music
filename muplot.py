import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors
import streamlit as st

"""
This is used for plotting music albums tracks and loudness for 1970s to 2010s.
"""

p = list(mcolors.CSS4_COLORS.keys())
for i in range(len(p)):
    if i in ['black','grey','dimgrey','dimgray','darkslategrey','darkslategray', 'midnightblue',
    'navy', 'darkblue','slategray','darkslateblue']:p.remove(i)

def load_data(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

@st.cache
def music():

    data = load_data('music_data/music.json')
    years = list(data.keys())

    x = np.array(
        [
            data[k][i][f'track_{i}'][0]['features'][0]['year'] 
            for k in data.keys() 
            for i in range(0,len(data[k]))
        ])
    
    y = np.array(
        [
            data[k][i][f'track_{i}'][0]['features'][0]['properties']['loudness']
            for k in data.keys() 
            for i in range(0,len(data[k]))
        ])

    area = np.array(
        [
            data[k][i][f'track_{i}'][0]['features'][0]['properties']['speechiness']
            for k in data.keys()
            for i in range(0,len(data[k]))
            ])*70

    color = [
        p[k]
        for k in range(0, len(years))
        for _ in range(0,len(data[years[k]]))
        ]
    return x, y, area, color

@st.cache
def artist_plot(i_, artist_data):

    # artist_data = load_data('music_data/data_artists.json')
    
    complete_albums = artist_data[f'artist_{i_}'][0]['albums_full']
    total_albums = len(complete_albums)

    album_names = [complete_albums[j_]['album_name'] for j_ in range(0, total_albums)]
    album_popularity = [complete_albums[j_]['album_popularity'] for j_ in range(0, total_albums)]

    artist_tracks_loudness, artist_tracks_danceability, artist_tracks_speechiness = list(), list(), list()
    color_ = dict()
    album_color = list()
    loudest_track_name = ''

    if total_albums > 0:

        for j_ in range(0, total_albums):

            loudest_track = -60

            for k_ in range(0, len(complete_albums[j_]['tracks'])):

                item = complete_albums[j_]['tracks'][k_]['features'][0]

                if complete_albums[j_]['album_name'] != 'Ultraviolence - Audio Commentary':
                    try:
                        loudest_track = item['loudness']
                        loudest_track_name = complete_albums[j_]['tracks'][k_]['track_name']
                        loudest_track_id = complete_albums[j_]['tracks'][k_]['track_id']
                    except Exception:
                        loudest_track_name = complete_albums[j_]['tracks'][k_]['track_name']
                        loudest_track_id = complete_albums[j_]['tracks'][k_]['track_id']
                
                    try:
                        artist_tracks_loudness.append(item['loudness'])
                        artist_tracks_danceability.append(item['danceability'])
                        artist_tracks_speechiness.append(item['speechiness'])
                        album_color.append(p[j_])
                        color_[complete_albums[j_]['album_name']] = p[j_]
                    except Exception:
                        artist_tracks_loudness.append(-30)
                        artist_tracks_danceability.append(0)
                        artist_tracks_speechiness.append(0)
                        album_color.append('red')
                        color_[complete_albums[j_]['album_name']] = 'red'
        
        popular_album = (album_names[album_popularity.index(max(album_popularity))].encode('utf-8').decode('utf-8'),
        color_[album_names[album_popularity.index(max(album_popularity))]])

    else:

        popular_album = ["None", "black"]

    y_pos = np.arange(len(album_names))*6
    artist_tracks_loudness = (np.abs(np.array(artist_tracks_loudness)) + 1)

    return loudest_track_id, y_pos, album_color, color_, loudest_track_name, popular_album, album_popularity, album_names,artist_tracks_loudness,artist_tracks_danceability,artist_tracks_speechiness

def artist_albums_plot(i_, artist_data):

    # artist_data = load_data('music_data/data_artists.json')

    fig0, ax0 = plt.subplots(figsize=(12, 8),facecolor='black')

    lid, y_pos, album_color, color_, loudest_track_name, popular_album, album_popularity, album_names,artist_tracks_loudness,artist_tracks_danceability,artist_tracks_speechiness = artist_plot(i_, artist_data)
    # x_value.extend(artist_tracks_speechiness)
    # y_value.extend(artist_tracks_danceability)
    #sp = ply.configure()
    #sp.user_playlist_create('0hczuz4ovfgx09ch7q216824z', 'Louddddd', public =True,description= 'loud tracks I guess')
    """
    Scatter plot of Danceability vs Speechiness.
    """
    ax0.spines['bottom'].set_color('w')
    ax0.set_facecolor('black')
    ax0.spines['top'].set_color('w')
    ax0.spines['right'].set_color('w')
    ax0.spines['left'].set_color('w')
    ax0.tick_params(axis = 'y', colors = 'w')
    ax0.tick_params(axis='x', colors='floralwhite')
    ax0.set_xlabel('Danceability', color = 'w')
    ax0.set_ylabel('Speechiness', color ='w')
    ax0.set_title(f"{artist_data[f'artist_{i_}'][0]['artist_name']}", c = 'w')

    colors = cm.hsv(np.array(artist_tracks_loudness) / float(max(np.array(artist_tracks_loudness))))
    
    ax0.scatter(artist_tracks_danceability, artist_tracks_speechiness, s= artist_tracks_loudness, c = colors, marker = "+", alpha = 1)
    """
    Horizontal bar plot for album popularity
    """

    name_popular = dict(list(zip(album_names,album_popularity)))
    name_popular = {k:v for k, v in sorted(name_popular.items(), key=lambda np:np[1], reverse=True)}

    fig1, ax1 = plt.subplots(figsize=(12, 8),facecolor='black')
    limit = 20
    y_pos = y_pos[:limit]
    ax1.set_yticks(y_pos)
    ax1.set_facecolor('black')
    ax1.set_yticklabels(list(name_popular.keys())[:limit][::-1], fontsize = 8, c='r')
    ax1.set_xlabel('Album Popularity', fontsize = 8, c = 'w')
    ax1.spines['bottom'].set_color('w')
    ax1.spines['top'].set_color('w')
    ax1.spines['right'].set_color('w')
    ax1.spines['left'].set_color('r')
    ax1.tick_params(axis = 'y', colors = 'w')
    ax1.tick_params(axis='x', colors='w')


    colors = cm.hsv(np.array(album_popularity) / float(max(np.array(album_popularity))))

    ax1.barh(
        y_pos,
        list(name_popular.values())[:limit][::-1],
        height = 1,
        color = colors,
        align = 'center'
        )

    # """
    # Adding name of popular album and loudest track on left upper corner.
    # """
    # plt.subplots_adjust(left = 0.3)
    # textstr = "\n".join([f"Popular Album\n{popular_album[0]}",f"Loudest Track\n{loudest_track_name}"])
    # plt.text(0.02, 0.9, textstr, fontsize=10, color = 'lime',
    # fontname = 'sans-serif',transform=plt.gcf().transFigure)
    # #plt.savefig(rf"ims\{artist_data[f'artist_{i_}'][0]['artist_name']}".replace(" ", "_"))
    # plt.show()
    # plt.clf()
    # plt.close()
    return fig0, fig1, popular_album, loudest_track_name, lid

def draw_plot():
    fig, ax = plt.subplots(figsize=(12, 8),facecolor='black')
    x_a, y_a, area, color = music()
    colors = cm.hsv(np.array(area) / float(max(np.array(area))))

    ax.scatter(x_a, y_a, s=area, c=colors)
    ax.set_facecolor('black')
    ax.set_xlim(1965, 2020)
    ax.set_xticks(range(1970, 2020, 4))
    ax.set_xlabel('Year', c = 'white')
    ax.set_ylabel('Loudness in dB (-60 to 0)', c = 'white')
    ax.set_title('Spotify: Music Loudness and Speechines from 1970 to 2019', c = 'lime')
    ax.spines['bottom'].set_color('w')
    ax.spines['top'].set_color('w')
    ax.spines['right'].set_color('w')
    ax.spines['left'].set_color('w')
    ax.tick_params(axis = 'y',colors = 'floralwhite')
    ax.tick_params(axis='x',which='major',colors='floralwhite')
    

    minor_xticks = np.arange(1965, 2020, 1)
    ax.set_xticks(minor_xticks, minor=True)
    ax.tick_params(axis = 'x', which = 'minor',colors='floralwhite')

    minor_yticks = np.arange(-25, 0, 1)
    ax.set_yticks(minor_yticks, minor=True)
    ax.tick_params(axis = 'y', which = 'minor',colors='floralwhite')

    return fig