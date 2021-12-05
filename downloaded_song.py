class DownloadedSong:
    def __init__(self, filename):
        self.filename = filename
        self.name = self.set_name()
        self.artists = self.set_artists()

    def __repr__(self):
        return f'{", ".join(self.artists)} - {self.name}'

    def set_name(self):
        return ('-'.join(self.filename.split('-')[1:])).strip()

    def set_artists(self):
        return [artist.strip() for artist in self.filename.split('-')[0].split(',')]
