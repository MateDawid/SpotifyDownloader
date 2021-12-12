import os

from download_directory import DownloadDirectory
from spotify_client import SpotifyClient
from playlist_comparator import PlaylistComparator


class DownloaderApp:
    def __init__(self):
        self.greeting_message = '\nWelcome to SpotifyDownloader'
        print(self.greeting_message)
        self.active = True
        self.user_data = self.get_user_data()
        self.spotify_client = None
        self.download_directory = None
        self.playlist_comparator = None
        self.general_actions = {
            '1': "List of downloaded songs not in Spotify favourite playlist",
            '2': "List of liked songs not in downloaded directory",
            '3': "Download songs from Spotify favourite playlist",
            '4': "Sort Spotify favourite playlist",
            '5': "Change Spotify Client credentials",
            '6': "Change download directory",
            '7': "Close SpotifyDownloader"
        }
        self.sort_methods = {
            '1': 'Artist alphabetically - Song age descending - Track number',
            '2': 'Artist alphabetically - Song age ascending',
            '3': 'Artist - Song name',
            '4': 'Song name',
            '5': 'Song age descending',
            '6': 'Return to general actions.'
        }

    @staticmethod
    def get_user_data():
        credentials = {}
        if os.path.isfile(f'{os.getcwd()}/.env'):
            with open(f'{os.getcwd()}/.env') as env_file:
                for line in env_file:
                    key, value = line.strip().split('=', 1)
                    credentials[key.strip()] = value.strip()
        return credentials

    def save_user_data(self):
        if os.path.isfile(f'{os.getcwd()}/.env'):
            with open(f'{os.getcwd()}/.env', 'r+') as env_file:
                env_file.truncate(0)
        with open(f'{os.getcwd()}/.env', 'w') as env_file:
            for key in self.user_data:
                env_file.write(f"{key}={self.user_data[key]}\n")

    def set_client_id(self, client_id):
        self.user_data['CLIENT_ID'] = client_id
        self.save_user_data()

    def set_client_secret(self, client_secret):
        self.user_data['CLIENT_SECRET'] = client_secret
        self.save_user_data()

    def set_download_path(self, download_path):
        self.user_data['DOWNLOAD_PATH'] = download_path
        self.save_user_data()

    def select_general_action(self):
        print("\nGENERAL ACTIONS:")
        for action_number in self.general_actions:
            print(f"{action_number}. {self.general_actions[action_number]}")
        chosen_action = str(input("\nEnter number of selected action: "))
        while chosen_action not in self.general_actions.keys():
            chosen_action = str(input("Error. Try again: "))
        return chosen_action

    def select_sorting_method(self):
        print("\nSORTING METHODS:")
        for sort_method_number in self.sort_methods:
            print(f"{sort_method_number}. {self.sort_methods[sort_method_number]}")
        chosen_method = str(input("\nEnter number of sorting method: "))
        while chosen_method not in self.sort_methods.keys():
            chosen_method = str(input("Error. Try again: "))
        return chosen_method

    def execute_sorting_method(self, sort_method):
        if sort_method == '1':
            self.spotify_client.sort_playlist(self.spotify_client.favourite_playlist,
                                              'artist-release_date-track_number')
        elif sort_method == '2':
            self.spotify_client.sort_playlist(self.spotify_client.favourite_playlist, 'artist-song_age')
        elif sort_method == '3':
            self.spotify_client.sort_playlist(self.spotify_client.favourite_playlist, 'artist-song_name')
        elif sort_method == '4':
            self.spotify_client.sort_playlist(self.spotify_client.favourite_playlist, 'song_name')
        elif sort_method == '5':
            self.spotify_client.sort_playlist(self.spotify_client.favourite_playlist, 'release_date')
        elif sort_method == '6':
            pass

    def execute_general_action(self, action):
        if action == '1':
            self.playlist_comparator.print_not_liked_songs()
        elif action == '2':
            self.playlist_comparator.print_not_downloaded_songs()
        elif action == '3':
            self.playlist_comparator.download_songs_from_list()
        elif action == '4':
            sort_method = self.select_sorting_method()
            self.execute_sorting_method(sort_method)
        elif action == '5':
            self.set_client_id(input('\nEnter SpotifyAPI Client ID:\n'))
            self.set_client_secret(input('\nEnter SpotifyAPI Client Secret:\n'))
            print("\nConnecting with Spotify account...")
            self.spotify_client = SpotifyClient(self.user_data['CLIENT_ID'], self.user_data['CLIENT_SECRET'])
        elif action == '6':
            self.set_download_path(input('\nEnter full path to your download directory:\n'))
        elif action == '7':
            self.active = False

    def run_app(self):
        if 'CLIENT_ID' not in self.user_data:
            self.set_client_id(input('Enter SpotifyAPI Client ID:\n'))
        if 'CLIENT_SECRET' not in self.user_data:
            self.set_client_secret(input('Enter SpotifyAPI Client Secret:\n'))
        if 'DOWNLOAD_PATH' not in self.user_data:
            self.set_download_path(input('Enter full path to your download directory:\n'))
        self.spotify_client = SpotifyClient(self.user_data['CLIENT_ID'], self.user_data['CLIENT_SECRET'])
        while self.active:
            self.download_directory = DownloadDirectory(self.user_data['DOWNLOAD_PATH'])
            self.playlist_comparator = PlaylistComparator(self.download_directory, self.spotify_client)
            action = self.select_general_action()
            self.execute_general_action(action)
