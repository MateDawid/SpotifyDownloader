from math import ceil
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    def __init__(self, client_id=None, client_secret=None, redirect_uri='http://localhost:8000'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.user = None
        self.spotify_playlist = None
        self.connect_with_spotify_user()
        self.get_playlist()

    def connect_with_spotify_user(self):
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-library-read user-library-modify"
        )
        self.user = spotipy.Spotify(auth_manager=auth_manager)

    def get_songs_sublist(self, offset=0, limit=50):
        return self.user.current_user_saved_tracks(limit=limit, offset=offset)

    def get_favourite_songs(self, limit_step=50):
        tracks = []
        max_range = int(ceil(self.get_songs_sublist(limit=1)['total']/50)*50)
        for offset in range(0, max_range, limit_step):
            results = self.get_songs_sublist(offset=offset, limit=limit_step)
            for item in results['items']:
                tracks.append(item)
        return tracks

    @staticmethod
    def get_song_url(song_details):
        return song_details['track']['external_urls']['spotify']

    def get_playlist(self):
        tracks = self.get_favourite_songs()
        self.spotify_playlist = [(f"{item['track']['artists'][0]['name']} - "
                                  f"{item['track']['name']}", self.get_song_url(item)) for item in tracks]

    def print_playlist(self):
        if self.spotify_playlist:
            count = len(self.spotify_playlist)
            for idx, song_tuple in enumerate(self.spotify_playlist, start=1):
                print(f"({idx}/{count}) {song_tuple[0]}")
        else:
            print(f"No songs found in playlist!")
