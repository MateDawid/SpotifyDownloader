from download_directory import DownloadDirectory
from spotify_client import SpotifyClient
from playlist_comparator import PlaylistComparator


if __name__ == '__main__':
    download_directory = DownloadDirectory('E:\[MUZYKA]\WSZYSTKIE')
    spotify_client = SpotifyClient()
    playlist_comparator = PlaylistComparator(download_directory, spotify_client)

    # test1 = spotify_client.sort_playlist(spotify_client.favourite_playlist, 'artist-release_date-track_number')
    # test2 = spotify_client.sort_playlist(spotify_client.favourite_playlist, 'artist-song_age')
    # test3 = spotify_client.sort_playlist(spotify_client.favourite_playlist, 'artist-song_name')
    # test4 = spotify_client.sort_playlist(spotify_client.favourite_playlist, 'song_name')
    # test5 = spotify_client.sort_playlist(spotify_client.favourite_playlist, 'release_date')

    spotify_client.sort_favourite_playlist('artist-release_date-track_number')

