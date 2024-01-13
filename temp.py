import os
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_search_terms(url: str) -> str:
    """
    Extracts artist and song name from spotify url.
    """
    track = sp.track(url)
    return f"{track['name']} {track['artists'][0]['name']}"


urls = [
    'https://open.spotify.com/track/7uN3Yp4N0Sf9Xq0yqg7vOI?si=23ec95d820bc4631',
    'https://open.spotify.com/track/0qxkOapx6v1hvcFBJWjry0?si=14df0886432145b0',
    'https://open.spotify.com/track/1Ucfy250EeH7Uhf25GioIC?si=1b46e7af083c4ebb',
    'https://open.spotify.com/track/59Q16UjyoQLm5T6zj8VUf7?si=cc8ff85f4abb444c',
]

for url in urls:
    print(get_search_terms(url))
