import os
import re
from math import ceil
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '6351cad0cd984110b83b21c1b4d4bce7'
CLIENT_SECRET = '5f793eda0269453d94ff8a1d822b9640'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000'



def connect_with_spotify_user(client_id, client_secret, redirect_uri):
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-read user-library-modify"
    )
    spotify_user = spotipy.Spotify(auth_manager=auth_manager)
    return spotify_user


def get_songs_sublist(user, offset=0, limit=50):
    return user.current_user_saved_tracks(limit=limit, offset=offset)


def get_favourite_songs(user, limit_step=50):
    tracks = []
    max_range = int(ceil(get_songs_sublist(user, limit=1)['total']/50)*50)
    for offset in range(0, max_range, limit_step):
        results = get_songs_sublist(user, offset=offset, limit=limit_step)
        for item in results['items']:
            tracks.append(item)
    return tracks


def get_song_url(song_details):
    return song_details['track']['external_urls']['spotify']


def get_spotify_songs_list(user):
    tracks = get_favourite_songs(user)
    return [(f"{item['track']['artists'][0]['name']} - {item['track']['name']}", get_song_url(item)) for item in tracks]


def get_downloaded_songs_list(directory):
    arr = os.listdir(directory)
    songs = filter(lambda x: (x.endswith('.mp3')), arr)
    return [song[:-4] for song in songs]


def format_downloaded_songs_title(downloaded_playlist):
    others = []
    for song in downloaded_playlist:
        if not re.match('^.*[^ ] - [^ ].*$', song):
            title_parts = song.split('-')
            if len(title_parts) == 2:
                old_title = f'{DOWNLOADED_SONGS_DIRECTORY}\\{song}.mp3'
                new_title = f'{DOWNLOADED_SONGS_DIRECTORY}\\{title_parts[0].strip()} - {title_parts[1].strip()}.mp3'
                os.rename(old_title, new_title)
            else:
                others.append(f'{DOWNLOADED_SONGS_DIRECTORY}\\{song}.mp3')
    if others:
        print("UNFORMATTED DOWNLOADED SONGS:")
        for idx, song in enumerate(others, start=1):
            print(f'{idx}. {song}')


def get_not_downloaded_songs(spotify_playlist, downloaded_playlist):
    to_download = []
    for song in spotify_playlist:
        if song[0] not in downloaded_playlist:
            to_download.append(song)


def get_not_liked_songs(spotify_playlist, downloaded_playlist):
    to_like = []
    spotify_titles = [song[0] for song in spotify_playlist]
    spotify_title_mapping = {}
    for song in spotify_titles:
        spotify_title_mapping[song.lower()] = song
    for song in downloaded_playlist:
        if song not in spotify_titles:
            if song.lower() in spotify_title_mapping:
                old_title = f'{DOWNLOADED_SONGS_DIRECTORY}\\{song}.mp3'
                new_title = f'{DOWNLOADED_SONGS_DIRECTORY}\\{spotify_title_mapping[song.lower()]}.mp3'
                os.rename(old_title, new_title)
            else:
                to_like.append(song)
    return to_like


def download_songs_from_list(url_list):
    for url in url_list:
        os.system(f'spotdl {url}')


if __name__ == '__main__':
    user = connect_with_spotify_user(CLIENT_ID, CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    spotify_playlist = get_spotify_songs_list(user)
    downloaded_playlist = get_downloaded_songs_list(DOWNLOADED_SONGS_DIRECTORY)
    format_downloaded_songs_title(downloaded_playlist)
    # get_not_downloaded_songs(spotify_playlist, downloaded_playlist)
    unliked_songs = get_not_liked_songs(spotify_playlist, downloaded_playlist)