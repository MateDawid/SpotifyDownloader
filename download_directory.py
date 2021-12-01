import os
import re


class DownloadDirectory:
    def __init__(self, directory_path=None):
        self.directory_path = directory_path
        self.downloaded_playlist = []

    def set_path(self, new_path):
        self.directory_path = new_path

    def get_playlist(self):
        try:
            files = os.listdir(self.directory_path)
        except FileNotFoundError:
            print(f'There is no {self.directory_path} directory!')
            return
        except NotADirectoryError:
            print(f'{self.directory_path} is not path to directory!')
            return
        songs = filter(lambda x: (x.endswith('.mp3')), files)
        self.downloaded_playlist = [song[:-4] for song in songs]

    def print_playlist(self):
        if self.downloaded_playlist:
            count = len(self.downloaded_playlist)
            for idx, song in enumerate(self.downloaded_playlist, start=1):
                print(f"({idx}/{count}) {song}")
        else:
            print(f"No downloaded songs found in {self.directory_path} directory!")

    def format_downloaded_songs_title(self):
        if self.downloaded_playlist:
            others = []
            for song in self.downloaded_playlist:
                if not re.match('^.*[^ ] - [^ ].*$', song):
                    title_parts = song.split('-')
                    if len(title_parts) == 2:
                        old_title = f'{self.directory_path}\\{song}.mp3'
                        new_title = f'{self.directory_path}\\{title_parts[0].strip()} - {title_parts[1].strip()}.mp3'
                        os.rename(old_title, new_title)
                    else:
                        others.append(f'{self.directory_path}\\{song}.mp3')
            if others:
                print("UNFORMATTED DOWNLOADED SONGS:")
                for idx, song in enumerate(others, start=1):
                    print(f'{idx}. {song}')
        else:
            print(f"No songs to format found in {self.directory_path} directory!")