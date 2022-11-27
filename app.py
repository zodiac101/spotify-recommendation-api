import os

from flask import Flask, request

import spotify
from spotify import get_token

app = Flask(__name__)

token = None

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/track/search')
def search_track():
    if request.method == 'GET':
        global token
        if token is None:
            token = get_token(client_id)
            if not token:
                return "Error: Could not get token"

        track_name = request.args.get('track_name')
        track_data = spotify.get_track_info(token, track_name)
        return track_data


if __name__ == '__main__':
    app.run()
