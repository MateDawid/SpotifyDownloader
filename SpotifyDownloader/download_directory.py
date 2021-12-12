from os import listdir

from downloaded_song import DownloadedSong


class DownloadDirectory:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.downloaded_playlist = self.get_playlist()

    def get_playlist(self):
        try:
            files = listdir(self.directory_path)
        except FileNotFoundError:
            print(f"\nThere is no '{self.directory_path}' directory!")
            return []
        except NotADirectoryError:
            print(f"\n'{self.directory_path}' is not path to directory!")
            return []
        songs = filter(lambda x: (x.endswith('.mp3')), files)
        return [DownloadedSong(song[:-4], self.directory_path) for song in songs]
