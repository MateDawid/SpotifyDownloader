from downloaded_playlist import DownloadedPlaylist
from spotify_playlist import SpotifyPlaylist

CLIENT_ID = '6351cad0cd984110b83b21c1b4d4bce7'
CLIENT_SECRET = '5f793eda0269453d94ff8a1d822b9640'


if __name__ == '__main__':
    # downloaded_playlist = DownloadedPlaylist()
    # downloaded_playlist.set_directory('E:\[MUZYKA]\WSZYSTKIE')
    # downloaded_playlist.get_playlist()
    # downloaded_playlist.print_playlist()
    spotify_playlist = SpotifyPlaylist(CLIENT_ID, CLIENT_SECRET)
    spotify_playlist.print_playlist()