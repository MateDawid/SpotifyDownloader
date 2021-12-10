import os

from download_directory import DownloadDirectory
from spotify_client import SpotifyClient
from playlist_comparator import PlaylistComparator


class DownloaderApp:
    def __init__(self):
        self.greeting_message = 'Welcome to SpotifyDownloader'
        print(self.greeting_message)
        self.active = True
        self.user_data = self.get_user_data()

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

    def run_app(self):
        print(self.user_data)