import os


class PlaylistComparator:
    def __init__(self, download_directory, spotify_client):
        self.download_directory = download_directory
        self.spotify_client = spotify_client
        self.downloaded_playlist = self.download_directory.downloaded_playlist
        self.spotify_playlist = spotify_client.spotify_playlist
        self.forbidden_signs = {'<', '>', ':', '"', '/', '\\', '|', '?', '*'}
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
        """
        Generates dictionary with processed titles to match directory song title with Spotify title in case
        of different case of letters or the presence of forbidden signs in file name.
        """
        for song_title in self.spotify_song_titles:
            formatted_song_title = self.replace_forbidden_file_signs(song_title)
            self.spotify_title_mapping[formatted_song_title.lower()] = formatted_song_title

    def replace_forbidden_file_signs(self, song_title):
        """
        Replaces forbidden signs from Spotify song title.
        """
        file_signs = set(song_title)
        new_title = song_title
        found_forbidden_signs = file_signs.intersection(self.forbidden_signs)
        if found_forbidden_signs:
            for forbidden_sign in found_forbidden_signs:
                if forbidden_sign == '?':
                    new_title = new_title.replace(forbidden_sign, '')
                elif forbidden_sign == '"':
                    new_title = new_title.replace(forbidden_sign, "'")
                else:
                    new_title = new_title.replace(forbidden_sign, '-')
        return new_title

    def get_not_liked_songs(self):
        for song in self.downloaded_playlist:
            if song not in self.spotify_song_titles:
                if song.lower() in self.spotify_title_mapping:
                    old_title = f'{self.download_directory.directory_path}\\{song}.mp3'
                    new_title = f'{self.download_directory.directory_path}\\' \
                                f'{self.spotify_title_mapping[song.lower()]}.mp3'
                    os.rename(old_title, new_title)
                else:
                    self.not_liked_songs.append(song)

    def print_not_liked_songs(self):
        if self.not_liked_songs:
            print(f"NOT LIKED SONGS FROM DIRECTORY {self.download_directory.directory_path}:")
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
