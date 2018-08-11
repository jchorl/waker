import spotipy
import spotipy.util as util

from config import SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID
from db import SpotifyConfigValue, get_session
from secrets import SPOTIFY_CLIENT_SECRET


DEFAULT_PLAYLIST_KEY = 'default_playlist'
NEXT_WAKEUP_SONG_KEY = 'next_wakeup_song'

def search(term):
    token = __get_token()
    spotify = spotipy.Spotify(auth=token)
    result = spotify.search(term)
    return result

def clear_next_wakeup_song():
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(NEXT_WAKEUP_SONG_KEY)
    if confValue is not None:
        session.delete(confValue)
        session.commit()

def get_next_wakeup_song():
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(NEXT_WAKEUP_SONG_KEY)
    if confValue is not None:
        return confValue.value
    return None

def set_next_wakeup_song(song_uri):
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(NEXT_WAKEUP_SONG_KEY)

    if confValue is None:
        confValue = SpotifyConfigValue(NEXT_WAKEUP_SONG_KEY, song_uri)
        session.add(confValue)
    else:
        confValue.value = song_uri

    session.commit()
    return song_uri

def get_playlists():
    token = __get_token()
    spotify = spotipy.Spotify(auth=token)

    playlists = spotify.user_playlists(SPOTIFY_USERNAME)
    return [playlist for playlist in playlists['items']]

def get_default_playlist():
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(DEFAULT_PLAYLIST_KEY)
    return confValue.value

def set_default_playlist(playlist_uri):
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(DEFAULT_PLAYLIST_KEY)

    if confValue is None:
        confValue = SpotifyConfigValue(DEFAULT_PLAYLIST_KEY, playlist_uri)
        session.add(confValue)
    else:
        confValue.value = playlist_uri

    session.commit()
    return playlist_uri

def __get_token():
    # this caches and refreshes access tokens
    # the redirect_uri doesnt even matter, as long as it matches spotify because the redirect link will be copy/pasted into the terminal
    token = util.prompt_for_user_token(
            username=SPOTIFY_USERNAME,
            scope='playlist-read-private',
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri='http://localhost:5000/spotify/auth')
    return token
