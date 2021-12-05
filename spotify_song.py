class SpotifySong:
    def __init__(self, track_data):
        self.track_data = track_data
        self.name = self.set_name()
        self.artists = self.set_artists()
        self.release_date = self.set_release_date()
        self.track_number = self.set_track_number()
        self.url = self.set_url()

    def __repr__(self):
        return f'{", ".join(self.artists)} - {self.name}'

    def set_name(self):
        return self.track_data['name'].strip()

    def set_artists(self):
        return [artist['name'].strip() for artist in self.track_data['artists']]

    def set_release_date(self):
        return self.track_data['album']['release_date'].strip()

    def set_track_number(self):
        return self.track_data['track_number'].strip()

    def set_url(self):
        return self.track_data['external_urls']['spotify'].strip()
