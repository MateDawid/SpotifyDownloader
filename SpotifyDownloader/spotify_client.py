from math import ceil
import os
import time
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

from spotify_song import SpotifySong


class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user = None
        self.redirect_uri = 'http://localhost:8000'
        self.favourite_playlist = []
        self.connect_with_spotify_user()

    def connect_with_spotify_user(self):
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-library-read user-library-modify"
        )
        self.user = spotipy.Spotify(auth_manager=auth_manager)
        try:
            self.get_favourite_playlist()
        except SpotifyOauthError:
            print("\nWrong SpotifyAPI credentials provided!")

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

    @staticmethod
    def get_song_age_in_days(song):
        try:
            return (datetime.today() - datetime.strptime(song.release_date, "%Y-%m-%d")).days
        except ValueError:
            return (datetime.today() - datetime.strptime(song.release_date, "%Y")).days

    def get_sorted_playlist(self, playlist, sort_method,  reverse):
        if sort_method == 'artist-release_date-track_number':
            sort_key = lambda song: (song.artists[0].lower(), song.release_date, song.track_number)
        elif sort_method == 'artist-song_age':
            sort_key = lambda song: (song.artists[0].lower(), self.get_song_age_in_days(song))
        elif sort_method == 'artist-song_name':
            sort_key = lambda song: (song.artists[0].lower(), song.name.lower())
        elif sort_method == 'song_name':
            sort_key = lambda song: song.name.lower()
        elif sort_method == 'release_date':
            sort_key = lambda song: song.release_date
        if sort_key:
            return sorted(playlist, key=sort_key, reverse=reverse)

    def create_favourite_playlist_backup_file(self):
        with open('Backups/favourite_backup.txt', 'w') as backup_file:
            for song in self.favourite_playlist:
                backup_file.write(f'{song.url}\n')

    def restore_favourite_playlist_from_backup(self, time_out=0.0):
        backup_urls = []
        with open('Backups/favourite_backup.txt', 'r') as backup_file:
            for line in backup_file:
                backup_urls.insert(0, line.replace('\n', ''))
        favourite_playlist_urls = [song.url for song in reversed(self.favourite_playlist)]
        if favourite_playlist_urls != backup_urls:
            try:
                for backup_url in backup_urls:
                    if backup_url not in favourite_playlist_urls:
                        self.user.current_user_saved_tracks_add([backup_url])
                        time.sleep(time_out)
            except spotipy.SpotifyException:
                print("SpotifyAPI error occurred - restarting process")
                self.restore_favourite_playlist_from_backup(time_out+0.2)
        os.remove("Backups/favourite_backup.txt")

    def sort_favourite_playlist(self, sort_method, reverse=False, time_out=0.0):
        unsorted_playlist_names = [str(song) for song in self.favourite_playlist]
        if os.path.isfile('Backups/favourite_backup.txt'):
            print('\nRestoring favourite playlist from backup file...')
            self.restore_favourite_playlist_from_backup()
            self.get_favourite_playlist()
        sorted_playlist = self.get_sorted_playlist(self.favourite_playlist, sort_method, not reverse)
        sorted_playlist_names = [str(song) for song in reversed(sorted_playlist)]
        list_count = len(self.favourite_playlist)
        if sorted_playlist_names != unsorted_playlist_names:
            print('\nCreating backup file...')
            self.create_favourite_playlist_backup_file()
            print('Sorting started...')
            try:
                for idx, disordered_song in enumerate(self.favourite_playlist, start=1):
                    print(f'({idx}/{2*list_count}) DELETE => {disordered_song}')
                    self.user.current_user_saved_tracks_delete([disordered_song.url])
                    time.sleep(time_out)
            except spotipy.SpotifyException:
                print("SpotifyAPI error occurred - restarting process")
                self.sort_favourite_playlist(sort_method, reverse, time_out + 0.2)
            for idx, song_in_order in enumerate(sorted_playlist, start=1):
                print(f'({idx+list_count}/{2 * list_count}) ADD => {song_in_order}')
                self.user.current_user_saved_tracks_add([song_in_order.url])
                time.sleep(1)
        else:
            print("\nFavourite playlist already sorted with selected method.")
