# Data Visualization of Certain Artists ![langs](https://img.shields.io/badge/Python-1784d4?style=flat&logo=python&logoColor=orange) ![langs](https://img.shields.io/badge/numpy-98f041?style=plastic&logo=numpy&logoColor=orange)

This project involves gathering data from spotify endpoint using spotify api with the help of python wrapper/package spotipy and displaying different albums and various attributes. This was done while I was learning to handle json data and as well as using api. These results are visualized using matplotlib library.
## Data Extraction
The data was scrapped from the spotify api endpoint and doesn't required much cleaning especially for western artists. For indian artists the albums are basically bollywood films which have different singers which leads to multiple duplicates in the data which are filtered.
The data format is json and it is available here as well as on [kaggle uploaded](https://www.kaggle.com/shameinew/spotify-artist-data-for-some-artists) by me.

## Data Visualisation
The following image displays the tracks and album data from a western artist Eminem.
The first graph displays danceability (a metric which measures how much you can tap your toe on the track) and acousticness of that track. And the second graph consists of popularity of albums of that particular artist and the top-left corner consists of popular albums and popular track of that artist.
!['Deducing Popular album of Eminem'](https://github.com/shamEiNew/musicplot/blob/master/ims/Eminem.png)
