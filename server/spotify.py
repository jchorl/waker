import json
import spotipy
import spotipy.util as util

from config import SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID
from db import SpotifyConfigValue, get_session
from secrets import SPOTIFY_CLIENT_SECRET


DEFAULT_PLAYLIST_KEY = 'default_playlist'
NEXT_WAKEUP_SONG_KEY = 'next_wakeup_song'

MODIFY_PLAYBACK_SCOPE = 'user-modify-playback-state'
READ_PLAYBACK_SCOPE = 'user-read-playback-state'
PLAYLIST_READ_SCOPE = 'playlist-read-private'

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
        return json.loads(confValue.value)
    return None

def set_next_wakeup_song(song_info):
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(NEXT_WAKEUP_SONG_KEY)

    if confValue is None:
        confValue = SpotifyConfigValue(NEXT_WAKEUP_SONG_KEY, json.dumps(song_info))
        session.add(confValue)
    else:
        confValue.value = json.dumps(song_info)

    session.commit()
    return song_info

def get_playlists():
    token = __get_token(PLAYLIST_READ_SCOPE)
    spotify = spotipy.Spotify(auth=token)

    playlists = spotify.user_playlists(SPOTIFY_USERNAME)
    return [playlist for playlist in playlists['items']]

def get_default_playlist():
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(DEFAULT_PLAYLIST_KEY)
    if confValue is not None:
        return json.loads(confValue.value)
    return None

def get_num_tracks_in_playlist(playlist_uri):
    token = __get_token(READ_PLAYBACK_SCOPE)
    spotify = spotipy.Spotify(auth=token)
    playlist = spotify.user_playlist(SPOTIFY_USERNAME, playlist_uri)
    return playlist['tracks']['total']

def set_default_playlist(playlist):
    session = get_session()
    confValue = session.query(SpotifyConfigValue).get(DEFAULT_PLAYLIST_KEY)

    if confValue is None:
        confValue = SpotifyConfigValue(DEFAULT_PLAYLIST_KEY, json.dumps(playlist))
        session.add(confValue)
    else:
        confValue.value = json.dumps(playlist)

    session.commit()
    return playlist

def get_devices():
    token = __get_token(READ_PLAYBACK_SCOPE)
    spotify = spotipy.Spotify(auth=token)
    return spotify.devices()['devices']

def play_track(track_uri, device_id):
    token = __get_token(MODIFY_PLAYBACK_SCOPE)
    spotify = spotipy.Spotify(auth=token)
    spotify.start_playback(device_id=device_id, uris=[track_uri])

def play_playlist(playlist_uri, offset, device_id):
    token = __get_token(MODIFY_PLAYBACK_SCOPE)
    spotify = spotipy.Spotify(auth=token)
    spotify.start_playback(device_id=device_id, context_uri=playlist_uri, offset={'position': offset})

def current_playback():
    token = __get_token(READ_PLAYBACK_SCOPE)
    spotify = spotipy.Spotify(auth=token)
    return spotify.current_playback()

def pause_playback():
    token = __get_token(MODIFY_PLAYBACK_SCOPE)
    spotify = spotipy.Spotify(auth=token)
    spotify.pause_playback()

def volume(volume_percent, device_id):
    token = __get_token(MODIFY_PLAYBACK_SCOPE)
    spotify = spotipy.Spotify(auth=token)
    spotify.volume(volume_percent, device_id)

def __get_token(scope=None):
    # this caches and refreshes access tokens
    # the redirect_uri doesnt even matter, as long as it matches spotify because the redirect link will be copy/pasted into the terminal
    token = util.prompt_for_user_token(
            username=SPOTIFY_USERNAME,
            scope=scope,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri='http://localhost:5000/spotify/auth',
            cache_path='.cache-{}-{}'.format(SPOTIFY_USERNAME, scope))
    return token
