# Inspired by https://github.com/smtchahal/spotify-import/blob/master/spotify_import.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from credentials import set_spotify_credentials

# Set Spotify credentials from credentials.py
set_spotify_credentials()

# Access credentials from environment variables
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

def main():


if __name__ == '__main__':
    main()
