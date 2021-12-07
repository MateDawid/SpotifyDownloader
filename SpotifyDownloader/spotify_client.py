from math import ceil
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

from spotify_song import SpotifySong


class SpotifyClient:
    def __init__(self):
        self.credentials = self.get_credentials()
        self.user = None
        self.redirect_uri = 'http://localhost:8000'
        self.favourite_playlist = []
        if self.credentials:
            self.connect_with_spotify_user()

    def set_redirect_uri(self, redirect_uri):
        self.redirect_uri = redirect_uri

    def save_credentials(self, client_id, client_secret):
        if os.path.isfile('../.env'):
            with open('../.env', 'r+') as env_file:
                env_file.truncate(0)
        with open('../.env', 'w') as env_file:
            env_file.write(f"CLIENT_ID={client_id}\n")
            env_file.write(f"CLIENT_SECRET={client_secret}")
        self.connect_with_spotify_user()

    @staticmethod
    def get_credentials():
        credentials = {}
        if os.path.isfile('../.env'):
            with open('../.env') as env_file:
                for line in env_file:
                    key, value = line.strip().split('=', 1)
                    credentials[key.strip()] = value.strip()
        return credentials

    def connect_with_spotify_user(self):
        credentials = self.get_credentials()
        if credentials:
            auth_manager = SpotifyOAuth(
                client_id=credentials['CLIENT_ID'],
                client_secret=credentials['CLIENT_SECRET'],
                redirect_uri=self.redirect_uri,
                scope="user-library-read user-library-modify"
            )
            self.user = spotipy.Spotify(auth_manager=auth_manager)
            try:
                self.get_favourite_playlist()
            except SpotifyOauthError:
                print("Wrong SpotifyAPI credentials proviced!")

    def get_songs_sublist(self, offset=0, limit=50):
        return self.user.current_user_saved_tracks(limit=limit, offset=offset)

    def get_favourite_playlist(self, limit_step=50):
        playlist = []
        if self.user:
            max_range = int(ceil(self.get_songs_sublist(limit=1)['total']/50)*50)
            for offset in range(0, max_range, limit_step):
                results = self.get_songs_sublist(offset=offset, limit=limit_step)
                for item in results['items']:
                    playlist.append(SpotifySong(item['track']))
        self.favourite_playlist = playlist

    def print_favourite_playlist(self):
        if self.get_favourite_playlist:
            count = len(self.favourite_playlist)
            for idx, song in enumerate(self.favourite_playlist, start=1):
                print(f"({idx}/{count}) {song}")
        else:
            print(f"No songs in Spotify favourite playlist!")
