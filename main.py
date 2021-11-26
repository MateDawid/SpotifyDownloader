from downloaded_playlist import DownloadedPlaylist


if __name__ == '__main__':
    downloaded_playlist = DownloadedPlaylist()
    downloaded_playlist.set_directory('E:\[MUZYKA]\WSZYSTKIE')
    downloaded_playlist.get_playlist()
    downloaded_playlist.print_playlist()