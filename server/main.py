from flask import Flask, jsonify

from alarms import get_alarms


app = Flask(__name__)

@app.route('/alarms', methods=['GET'])
def get_alarms_handler():
    alarms = get_alarms()
    return jsonify(alarms)
