from flask import Flask, jsonify, request
import schedule
import threading
import time

from alarms import delete_alarm, get_alarms, new_alarm
from db import init_db
from spotify import get_playlists, set_default_playlist


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
    alarm_id = delete_alarm(alarm_id)
    return alarm_id

@app.route('/spotify/playlists', methods=['GET'])
def get_playlists_handler():
    playlists = get_playlists()
    return jsonify(playlists)

@app.route('/spotify/default_playlist', methods=['GET'])
def get_default_playlist_handler():
    playlist_uri = get_default_playlist()
    return playlist_uri

@app.route('/spotify/default_playlist', methods=['PUT'])
def set_default_playlist_handler():
    playlist_uri = set_default_playlist(request.get_json()['playlist_uri'])
    return playlist_uri

# init db
init_db()

# alarm execution thread
class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
        schedule.run_pending()
        time.sleep(1)

continuous_thread = ScheduleThread()
continuous_thread.start()
