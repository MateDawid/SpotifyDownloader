import os


class PlaylistComparator:
    def __init__(self, downloaded_playlist, spotify_playlist):
        self.downloaded_playlist = downloaded_playlist.downloaded_playlist
        self.spotify_playlist = spotify_playlist.playlist
        self.spotify_song_titles = [song[0] for song in self.spotify_playlist]
        self.spotify_song_ids = [song[1] for song in self.spotify_playlist]
        self.spotify_title_mapping = {}
        self.generate_spotify_titles_mapping()
        self.not_liked_songs = []
        self.not_downloaded_songs = []
        self.get_not_downloaded_songs()
        self.get_not_liked_songs()

    def get_not_downloaded_songs(self):
        for song in self.spotify_playlist:
            if song[0] not in self.downloaded_playlist:
                self.not_downloaded_songs.append(song)

    def print_not_downloaded_songs(self):
        if self.not_downloaded_songs:
            print("NOT DOWNLOADED SONGS FROM PLAYLIST:")
            for idx, song in enumerate(self.not_downloaded_songs, start=1):
                print(f'{idx}. {song[0]}')
        else:
            print("ALL SONGS ALREADY DOWNLOADED.")

    def generate_spotify_titles_mapping(self):
        for song in self.spotify_song_titles:
            self.spotify_title_mapping[song.lower().replace] = song

    def get_not_liked_songs(self):
        for song in self.downloaded_playlist:
            if song not in self.spotify_song_titles:
                if song.lower() in self.spotify_title_mapping:
                    old_title = f'{self.downloaded_playlist.directory}\\{song}.mp3'
                    new_title = f'{self.downloaded_playlist.directory}\\{self.spotify_title_mapping[song.lower()]}.mp3'
                    os.rename(old_title, new_title)
                else:
                    self.not_liked_songs.append(song)

    def print_not_liked_songs(self):
        if self.not_liked_songs:
            print(f"NOT LIKED SONGS FROM DIRECTORY:")
            for idx, song in enumerate(self.not_liked_songs, start=1):
                print(f'{idx}. {song}')
        else:
            print("ALL SONGS ALREADY LIKED.")

    def download_songs_from_list(self):
        if self.spotify_song_ids:
            for url in self.spotify_song_ids:
                os.system(f'spotdl {url}') # NOQA
        else:
            print("NO SONGS TO DOWNLOAD.")
