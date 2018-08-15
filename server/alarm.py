import pygame
import random
import schedule
import time

from config import SPOTIFY_DEVICE_NAME, SPOTIFY_VOLUME
from gcalendar import get_calendar_events
from spotify import clear_next_wakeup_song, current_playback, get_default_playlist, get_devices, get_next_wakeup_song, get_num_tracks_in_playlist, pause_playback, play_playlist, play_track, volume
from text_to_speech import synthesize_text
from weather_forecast import get_forecast


def alarm_job():
    __play_song()

    forecast_string = get_forecast()
    cal_event_string = get_calendar_events()
    speech_string = forecast_string + cal_event_string
    synthesize_text(speech_string)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('./output.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

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
        play_track(wakeup_song['uri'], device['id'])
        clear_next_wakeup_song()
    # otherwise use the default playlist
    else:
        playlist_uri = get_default_playlist()['uri']
        num_tracks = get_num_tracks_in_playlist(playlist_uri)
        offset = random.randint(0, num_tracks)
        play_playlist(playlist_uri, offset, device['id'])

    duration_ms = None

    # start polling to wait until the song is over
    while True:
        if duration_ms is None:
            playback = current_playback()
            duration_ms = playback['item']['duration_ms']
        elif duration_ms <= 2000:
            break
        else:
            duration_ms -= 1000

        # slowly crank the volume
        if cur_vol <= SPOTIFY_VOLUME - 10:
            cur_vol += 10
            volume(cur_vol, device['id'])
        elif cur_vol != SPOTIFY_VOLUME:
            cur_vol = SPOTIFY_VOLUME
            volume(cur_vol, device['id'])

        time.sleep(1)

    # pause the song
    pause_playback()
