import os
import re


class FileChecker:
    def __init__(self):
        self.directory = None
        self.downloaded_playlist = None

    def set_directory(self, new_directory):
        self.directory = new_directory

    def get_downloaded_playlist(self):
        files = os.listdir(self.directory)
        songs = filter(lambda x: (x.endswith('.mp3')), files)
        self.downloaded_playlist = [song[:-4] for song in songs]

    def print_downloaded_playlist(self):
        count = len(self.downloaded_playlist)
        if count > 0:
            for idx, song in enumerate(self.downloaded_playlist, start=1):
                print(f"({idx}/{count}) {song}")
        else:
            print(f"No downloaded songs found in {self.directory} directory!")

    def format_downloaded_songs_title(self):
        others = []
        for song in self.downloaded_playlist:
            if not re.match('^.*[^ ] - [^ ].*$', song):
                title_parts = song.split('-')
                if len(title_parts) == 2:
                    old_title = f'{self.directory}\\{song}.mp3'
                    new_title = f'{self.directory}\\{title_parts[0].strip()} - {title_parts[1].strip()}.mp3'
                    os.rename(old_title, new_title)
                else:
                    others.append(f'{self.directory}\\{song}.mp3')
        if others:
            print("UNFORMATTED DOWNLOADED SONGS:")
            for idx, song in enumerate(others, start=1):
                print(f'{idx}. {song}')