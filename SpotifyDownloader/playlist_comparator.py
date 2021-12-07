import os


class PlaylistComparator:
    def __init__(self, download_directory, spotify_client):
        self.download_directory = download_directory
        self.downloaded_playlist = self.download_directory.downloaded_playlist
        self.spotify_playlist = spotify_client.favourite_playlist
        self.forbidden_signs = {'<', '>', ':', '"', '/', '\\', '|', '?', '*'}
        self.spotify_formatted_playlist = self.generate_formatted_spotify_playlist()
        self.not_liked_songs = self.get_not_liked_songs()
        self.not_downloaded_songs = self.get_not_downloaded_songs()

    def generate_formatted_downloaded_playlist(self):
        return [str(downloaded_song).lower() for downloaded_song in self.downloaded_playlist]

    def get_not_downloaded_songs(self):
        not_downloaded_songs = []
        formatted_downloaded_playlist = self.generate_formatted_downloaded_playlist()
        for spotify_song in self.spotify_playlist:
            if str(spotify_song).lower in formatted_downloaded_playlist:
                continue
            downloaded = False
            for downloaded_song in self.downloaded_playlist:
                name_condition = self.replace_forbidden_file_signs(spotify_song.name) == downloaded_song.name
                artists_condition = any(artist in spotify_song.artists for artist in downloaded_song.artists)
                if name_condition and artists_condition:
                    downloaded = True
                    break
            if downloaded:
                continue
            not_downloaded_songs.append(spotify_song)
        return not_downloaded_songs

    def print_not_downloaded_songs(self):
        if self.not_downloaded_songs:
            print("NOT DOWNLOADED SONGS FROM PLAYLIST:")
            for idx, song in enumerate(self.not_downloaded_songs, start=1):
                print(f'{idx}. {song}')
        else:
            print("ALL SONGS ALREADY DOWNLOADED.")

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

    def generate_formatted_spotify_playlist(self):
        return [self.replace_forbidden_file_signs(str(spotify_song)).lower() for spotify_song in self.spotify_playlist]

    def get_not_liked_songs(self):
        not_liked_songs = []
        formatted_spotify_playlist = self.generate_formatted_spotify_playlist()
        for downloaded_song in self.downloaded_playlist:
            if str(downloaded_song).lower() in formatted_spotify_playlist:
                continue
            liked = False
            for spotify_song in self.spotify_playlist:
                name_condition = self.replace_forbidden_file_signs(spotify_song.name) == downloaded_song.name
                artists_condition = any(artist in spotify_song.artists for artist in downloaded_song.artists)
                if name_condition and artists_condition:
                    liked = True
                    break
            if liked:
                continue
            not_liked_songs.append(downloaded_song)
        return not_liked_songs

    def print_not_liked_songs(self):
        if self.not_liked_songs:
            print(f"NOT LIKED SONGS FROM DIRECTORY {self.download_directory.directory_path}:")
            for idx, song in enumerate(self.not_liked_songs, start=1):
                print(f'{idx}. {song}')
        else:
            print("ALL SONGS ALREADY LIKED.")

    def download_songs_from_list(self):
        if self.not_downloaded_songs:
            for song in self.not_downloaded_songs:
                os.system(f'spotdl {song.url}') # NOQA
        else:
            print("NO SONGS TO DOWNLOAD.")
