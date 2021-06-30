from google.protobuf.symbol_database import Default
import streamlit as st
from muplot import *
from mudata import configure
import webbrowser

sp = configure('user')


st.set_page_config('music',page_icon='❤️',layout='wide')
fig=draw_plot()

def option_area():
    artist_type = st.selectbox('Artist Region', ['Western', 'Indian'])
    if artist_type=='Western':
        return load_data('music_data/data_artists.json')
    return load_data('music_data/data_artists_IN.json')






col1,col2, col3 = st.beta_columns(3)


with col1:
    st.write(fig)

with col2:
    data = option_area()
    total_artists = len(data)
    artist_dict = dict(list(zip([data[f'artist_{i+1}'][0]['artist_name'] for i in range(0, total_artists)], range(0, total_artists))))
    options = list(artist_dict.keys())
    options = sorted(options)
    options.insert(0, '')
    artist_dropdown = st.selectbox('Artist',options)
    if artist_dropdown!='':
        fig0, fig1, popular_album, loudest_track, lid =artist_albums_plot(artist_dict[artist_dropdown]+1, data)
        st.write(f'Popular album of {artist_dropdown} is {popular_album[0]}')
        st.markdown(f'The graph shows below top 20 albums by popularity.')
        st.write(fig1)
        st.write(f'Loudest track is {loudest_track}.')
        
        url = sp.track(lid)['external_urls']['spotify']

        if st.button('Play it in Spotify'):
            webbrowser.open_new_tab(url)
        st.write(fig0)

