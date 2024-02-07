# Lesson: ChatGPT is powerful for scripting

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

def read_song_list(file_path):
    with open(file_path, 'r') as file:
        songs = file.read().splitlines()
    return songs

def add_songs_to_library(spotify, songs):
    for song in songs:
        results = spotify.search(q=song, type='track', limit=1)
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            spotify.current_user_saved_tracks_add([track_id])
            print(f"Added '{song}' to your library.")
        else:
            print(f"Couldn't find '{song}' on Spotify.")

def main():
    file_path = 'playlist_output.txt'
    songs = read_song_list(file_path)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope='user-library-modify'
    ))

    add_songs_to_library(sp, songs)

if __name__ == "__main__":
    main()
