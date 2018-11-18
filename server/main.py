from flask import Flask, jsonify, request
import requests
import schedule
import threading
import time

from alarms import delete_alarm, get_alarms, new_alarm
from db import db_session, init_db
from spotify import get_playlists, get_default_playlist, get_next_wakeup_song, set_default_playlist, set_next_wakeup_song, search, get_devices
import watchdog_pb2


# Flask routing
app = Flask(__name__)

@app.route('/alarms', methods=['GET'])
def get_alarms_handler():
    alarms = get_alarms()
    return jsonify(alarms)

@app.route('/alarms', methods=['POST'])
def post_alarm_handler():
    alarm = new_alarm(request.get_json())
    return jsonify(alarm)

@app.route('/alarms/<uuid:alarm_id>', methods=['DELETE'])
def delete_alarm_handler(alarm_id):
    alarm_id = delete_alarm(str(alarm_id))
    return alarm_id

@app.route('/spotify/playlists', methods=['GET'])
def get_playlists_handler():
    playlists = get_playlists()
    return jsonify(playlists)

@app.route('/spotify/default_playlist', methods=['GET'])
def get_default_playlist_handler():
    playlist = get_default_playlist()
    return jsonify(playlist)

@app.route('/spotify/default_playlist', methods=['PUT'])
def set_default_playlist_handler():
    playlist = set_default_playlist(request.get_json())
    return jsonify(playlist)

@app.route('/spotify/next_wakeup_song', methods=['GET'])
def get_next_wakeup_song_handler():
    next_wakeup_song = get_next_wakeup_song()
    return jsonify(next_wakeup_song)

@app.route('/spotify/next_wakeup_song', methods=['PUT'])
def set_next_wakeup_song_handler():
    next_wakeup_song = set_next_wakeup_song(request.get_json())
    return jsonify(next_wakeup_song)

@app.route('/spotify/search', methods=['GET'])
def search_handler():
    results = search(request.args.get('q'))
    return jsonify(results)

@app.route('/spotify/devices', methods=['GET'])
def get_devices_handler():
    return jsonify(get_devices())

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def notify_watchdog():
    watch = watchdog_pb2.Watch()
    watch.name = "waker"
    watch.frequency = watchdog_pb2.Watch.DAILY
    requests.post('https://watchdog.joshchorlton.com/ping', data = watch.SerializeToString())

init_db()

# alarm execution thread
class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
        while True:
            schedule.run_pending()
            time.sleep(60)

continuous_thread = ScheduleThread()
continuous_thread.start()

schedule.every().hour.do(notify_watchdog)
