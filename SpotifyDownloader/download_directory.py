from os import listdir

from downloaded_song import DownloadedSong


class DownloadDirectory:
    def __init__(self, directory_path=None):
        self.directory_path = directory_path
        self.downloaded_playlist = self.get_playlist()

    def set_path(self, new_path):
        self.directory_path = new_path
        self.downloaded_playlist = self.get_playlist()

    def get_playlist(self):
        try:
            files = listdir(self.directory_path)
        except FileNotFoundError:
            print(f"There is no '{self.directory_path}' directory!")
            return []
        except NotADirectoryError:
            print(f"'{self.directory_path}' is not path to directory!")
            return []
        songs = filter(lambda x: (x.endswith('.mp3')), files)
        return [DownloadedSong(song[:-4], self.directory_path) for song in songs]

    def print_playlist(self):
        if self.downloaded_playlist:
            count = len(self.downloaded_playlist)
            for idx, song in enumerate(self.downloaded_playlist, start=1):
                print(f"({idx}/{count}) {song}")
        else:
            print(f"No downloaded songs found in '{self.directory_path}' directory!")
