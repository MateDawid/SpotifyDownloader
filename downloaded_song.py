from os import rename


class DownloadedSong:
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory
        self.name = self.set_name()
        self.artists = self.set_artists()
        self.format_filename()

    def __repr__(self):
        return f'{", ".join(self.artists)} - {self.name}'

    def set_name(self):
        return ' '.join(('-'.join(self.filename.split('-')[1:])).strip().split())

    def set_artists(self):
        return [artist.strip() for artist in self.filename.split('-')[0].split(',')]

    def format_filename(self):
        if self.__repr__() != self.filename:
            rename(f'{self.directory}\\{self.filename}.mp3', f'{self.directory}\\{self.__repr__()}.mp3')
