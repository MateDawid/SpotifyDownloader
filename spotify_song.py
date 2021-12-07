class SpotifySong:
    def __init__(self, track_data):
        self.name = self.set_name(track_data)
        self.artists = self.set_artists(track_data)
        self.release_date = self.set_release_date(track_data)
        self.track_number = self.set_track_number(track_data)
        self.url = self.set_url(track_data)

    def __repr__(self):
        return f'{", ".join(self.artists)} - {self.name}'

    @staticmethod
    def set_name(track_data):
        return track_data['name'].strip()

    @staticmethod
    def set_artists(track_data):
        return [artist['name'].strip() for artist in track_data['artists']]

    @staticmethod
    def set_release_date(track_data):
        return track_data['album']['release_date'].strip()

    @staticmethod
    def set_track_number(track_data):
        return track_data['track_number']

    @staticmethod
    def set_url(track_data):
        return track_data['external_urls']['spotify'].strip()
