import os
import re


class DownloadedPlaylist:
    def __init__(self, directory=None):
        self.directory = directory
        self.downloaded_playlist = []

    def set_directory(self, new_directory):
        self.directory = new_directory

    def get_playlist(self):
        try:
            files = os.listdir(self.directory)
        except FileNotFoundError:
            print(f'There is no {self.directory} directory!')
            return
        except NotADirectoryError:
            print(f'{self.directory} is not path to directory!')
            return
        songs = filter(lambda x: (x.endswith('.mp3')), files)
        self.downloaded_playlist = [song[:-4] for song in songs]

    def print_playlist(self):
        if self.downloaded_playlist:
            count = len(self.downloaded_playlist)
            for idx, song in enumerate(self.downloaded_playlist, start=1):
                print(f"({idx}/{count}) {song}")
        else:
            print(f"No downloaded songs found in {self.directory} directory!")

    def format_downloaded_songs_title(self):
        if self.downloaded_playlist:
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
        else:
            print(f"No songs to format found in {self.directory} directory!")