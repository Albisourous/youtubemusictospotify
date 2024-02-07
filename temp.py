#!/usr/bin/env python3

from datetime import datetime
from difflib import SequenceMatcher
from typing import List

import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth

def dict_get(adict: dict, *keys: str):
    current = adict
    if not keys:
        return None
    for key in keys:
        if current and key in current:
            current = current.get(key, None)
        else:
            current = None
    return current


def scoped(scopes: List[str]):
    return ' '.join(scopes)

def replace_bad_words(song: str):
    bad_words = ('feat. ', 'ft. ', ' (Original Mix)', ' (Original mix)', ' (original mix)', ' - Original Mix', ' &')
    for word in bad_words:
        song = song.replace(word, '')
    return song

def divide_tracks_into_chunks(tracks):
    per_request_track_threshold = 100
    track_sub_lists = [tracks[i:i + per_request_track_threshold] for i in
                       range(0, len(tracks), per_request_track_threshold)]
    return track_sub_lists


class SpotifyImport:
    PLAYLIST_ADD_TRACK_LIMIT = 100
    LIBRARY_ADD_TRACK_LIMIT = 50

    def __init__(self, destination, songs, playlist=None):
        self.destination = destination
        self.songs = songs
        if destination == 'playlist':
            self.playlist = playlist if playlist else f'Imported Playlist on {datetime.now().isoformat()}'

        load_dotenv()
        scope = scoped(['playlist-modify-private', 'user-library-modify'])
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))

    def _get_user_id(self):
        return self.sp.me()['id']

    def _save_tracks(self, tracks: List[str], failed_count: int):
        tracks_list = divide_tracks_into_chunks(tracks)
        for tracks in tracks_list:
            self.sp.current_user_saved_tracks_add(tracks)

    def _run_txt(self):
        with open(self.songs) as songs_file, open('failed.txt', 'w') as failed_file:
            tracks = []
            failed_count = 0

            for song in (line.strip() for line in songs_file):
                song = replace_bad_words(song)

                if not song:
                    continue

                result = self.sp.search(song, limit=1)
                track_items = dict_get(result, 'tracks', 'items')
                track_id = track_items[0].get('id') if track_items else None
                if track_id:
                    tracks.append(track_id)
                else:
                    failed_count += 1
                    print(f"Couldn't find anything for {song!r}: {result!r}")
                    print(song, file=failed_file)

                if len(tracks) == self.PLAYLIST_ADD_TRACK_LIMIT:
                    self._save_tracks(tracks, failed_count)
                    tracks = []

            if tracks:
                self._save_tracks(tracks, failed_count)

        print('Done!')


    def run(self):
        self._run_txt()

def main():
    songs_path = "path/to/your/songs.txt"  # Set the path to your songs file
    destination = "library"  # Set the destination (either "library" or "playlist")
    playlist_name = None  # Set the playlist name if the destination is "playlist"

    spotify_import = SpotifyImport(destination, songs_path, playlist_name)
    spotify_import.run()


if __name__ == '__main__':
    main()