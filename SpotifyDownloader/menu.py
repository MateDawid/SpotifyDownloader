from download_directory import DownloadDirectory
from spotify_client import SpotifyClient
from playlist_comparator import PlaylistComparator


if __name__ == '__main__':
    download_directory = DownloadDirectory('E:\[MUZYKA]\WSZYSTKIE')
    spotify_client = SpotifyClient()
    playlist_comparator = PlaylistComparator(download_directory, spotify_client)
    playlist_comparator.print_not_downloaded_songs()