from math import ceil
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotify_song import SpotifySong


CLIENT_ID = '6351cad0cd984110b83b21c1b4d4bce7'
CLIENT_SECRET = '5f793eda0269453d94ff8a1d822b9640'


class SpotifyClient:
    def __init__(self):
        self.user = None
        self.connect_with_spotify_user(CLIENT_ID, CLIENT_SECRET)  # TODO
        self.spotify_playlist = self.set_playlist()

    def connect_with_spotify_user(self, client_id, client_secret, redirect_uri='http://localhost:8000'):
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-library-read user-library-modify"
        )
        self.user = spotipy.Spotify(auth_manager=auth_manager)

    def get_songs_sublist(self, offset=0, limit=50):
        return self.user.current_user_saved_tracks(limit=limit, offset=offset)

    def set_playlist(self, limit_step=50):
        playlist = []
        max_range = int(ceil(self.get_songs_sublist(limit=1)['total']/50)*50)
        for offset in range(0, max_range, limit_step):
            results = self.get_songs_sublist(offset=offset, limit=limit_step)
            for item in results['items']:
                playlist.append(SpotifySong(item['track']))
        return playlist

    def print_playlist(self):
        if self.spotify_playlist:
            count = len(self.spotify_playlist)
            for idx, song in enumerate(self.spotify_playlist, start=1):
                print(f"({idx}/{count}) {song}")
        else:
            print(f"No songs found in playlist!")
