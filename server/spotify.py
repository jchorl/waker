import spotipy
import spotipy.util as util

from config import SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID
from secrets import SPOTIFY_CLIENT_SECRET

def get_playlists():
    # this caches and refreshes access tokens
    # the redirect_uri doesnt even matter, as long as it matches spotify because the redirect link will be copy/pasted into the terminal
    token = util.prompt_for_user_token(
            username=SPOTIFY_USERNAME,
            scope='playlist-read-private',
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri='http://localhost:5000/spotify/auth')

    spotify = spotipy.Spotify(auth=token)

    playlists = spotify.user_playlists(SPOTIFY_USERNAME)
    return [playlist for playlist in playlists['items']]
