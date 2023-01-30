import requests
from bs4 import BeautifulSoup
import spotipy
import json


# Asking user for a year to create a spotify playlist
date = input("Which year do you want to travel to?  Type the date in this format YYYY-MM-DD: ")
year = int(date.split("-")[0])

ENDPOINT = f"https://www.billboard.com/charts/hot-100/{date}"

# Scraping Billboard Web to get top 100 songs from specific date
response = requests.get(url=ENDPOINT)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.select(".o-chart-results-list__item h3")
song_list = []
for item in songs:
    song = soup.select(".o-chart-results-list__item h3")
    artist = item.find_next_sibling().getText(strip=True)
    song_list.append({"song":item.getText(strip=True), "artist":artist})

# Authorizing Spotipy
SPOTIPY_CLIENT_ID = <YOUR_CLIENT_ID>
SPOTIPY_CLIENT_SECRET = <YOUR_CLIENT_SECRET>
REDIRECT_URI = <YOUR_REDIRECT_URI>
SCOPE = "playlist-modify-public,playlist-modify-private,user-library-read"

try:
    with open('.cache') as file:
        data = file.read()
        ACCESS_TOKEN = json.loads(data)['access_token']

except FileNotFoundError:
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri=REDIRECT_URI, scope=SCOPE)
    ACCESS_TOKEN = sp_oauth.get_access_token(as_dict=False, check_cache=True)
spotify = spotipy.Spotify(ACCESS_TOKEN)

# Creating Playlist, Giving it a Title, and pulling out its ID
playlist_id = spotify.user_playlist_create(user=<YOUR_USER_ID>, name=f'{date} Billboard Top 100',
                                           public=True, collaborative=False)['id']
# Searching spotify to find unique URI for each song in Song List
uri_list = []
for entry in song_list:
    url = spotify.search(type='track', limit=1, q=f'track: {entry["song"]} year: {year}')['tracks']['items'][0]['uri']
    uri_list.append(url)

# Adding all songs found into playlist
spotify.playlist_add_items(playlist_id=playlist_id, items=uri_list)
