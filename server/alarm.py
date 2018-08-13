import random
import schedule
import time

from config import SPOTIFY_DEVICE_NAME, SPOTIFY_VOLUME
from gcalendar import get_calendar_events
from spotify import clear_next_wakeup_song, current_playback, get_default_playlist, get_devices, get_next_wakeup_song, get_num_tracks_in_playlist, pause_playback, play_playlist, play_track, volume
from text_to_speech import synthesize_text


def alarm_job():
    __play_song()

    cal_event_string = get_calendar_events()
    synthesize_text(cal_event_string)

def alarm_job_once():
    alarm_job()
    return schedule.CancelJob

def __play_song():
    # select the device to play on
    devices = get_devices()
    device = next(d for d in devices if d['name'] == SPOTIFY_DEVICE_NAME)

    # get a song, if the song has been set
    wakeup_song = get_next_wakeup_song()

    # start at 0 volume and work up later
    cur_vol = 0
    volume(cur_vol, device['id'])

    # if the song was chosen, use it
    if wakeup_song is not None:
        play_track(wakeup_song, device['id'])
        clear_next_wakeup_song()
    # otherwise use the default playlist
    else:
        playlist_uri = get_default_playlist()
        num_tracks = get_num_tracks_in_playlist(playlist_uri)
        offset = random.randint(0, num_tracks)
        play_playlist(playlist_uri, offset, device['id'])

    cur_song_id = None

    # start polling to wait until the song is over
    while True:
        # slowly crank the volume
        if cur_vol <= SPOTIFY_VOLUME - 10:
            cur_vol += 10
            volume(cur_vol, device['id'])
        elif cur_vol != SPOTIFY_VOLUME:
            cur_vol = SPOTIFY_VOLUME
            volume(cur_vol, device['id'])

        playback = current_playback()

        # check if at the end of the song
        progress_ms = playback['progress_ms']
        duration_ms = playback['item']['duration_ms']
        if progress_ms >= duration_ms - 1500:
            break

        # check if onto the next song
        if cur_song_id is None:
            cur_song_id = playback['item']['id']
        elif cur_song_id != playback['item']['id']:
            break

        time.sleep(1)

    # pause the song
    pause_playback()
