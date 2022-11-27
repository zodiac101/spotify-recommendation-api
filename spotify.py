import base64

import requests


# Get the token from the Spotify API
def get_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token?grant_type=client_credentials"
    headers = {
        "Authorization": "Basic {}".format(base64.b64encode(client_id+':'+client_secret)),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers)
    return response.json()['access_token']


# Search for a track
def search_track(token, track_name):
    url = "https://api.spotify.com/v1/search?q={}&type=track".format(track_name)
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.get(url, headers=headers)
    return response.json()


# Get the track's Information
def get_track_id(token, track_name, track_data=None):
    if track_data is None:
        track_data = search_track(token, track_name)
    track_id = track_data['tracks']['items'][0]['id']
    track_name = track_data['tracks']['items'][0]['name']
    track_explicit = track_data['tracks']['items'][0]['explicit']
    track_duration = track_data['tracks']['items'][0]['duration_ms']
    track_release_date = track_data['tracks']['items'][0]['album']['release_date']

    return track_id, track_name, track_explicit, track_duration, track_release_date


# Get the track's audio features
def get_track_features(token, track_id):
    url = "https://api.spotify.com/v1/audio-features/{}".format(track_id)
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_track_info(token, track_name):
    track_data = search_track(token, track_name)
    if len(track_data['tracks']['items']) == 0:
        return None
    track_id, track_name, track_explicit, track_duration, track_release_date = \
        get_track_id(token, track_name, track_data)
    track_features = get_track_features(token, track_id)

    return {
        "explicit": track_explicit,
        "danceability": track_features['danceability'],
        "energy": track_features['energy'],
        "key": track_features['key'],
        "loudness": track_features['loudness'],
        "mode": track_features['mode'],
        "speechiness": track_features['speechiness'],
        "acousticness": track_features['acousticness'],
        "instrumentalness": track_features['instrumentalness'],
        "liveness": track_features['liveness'],
        "valence": track_features['valence'],
        "tempo": track_features['tempo'],
        "duration_ms": track_duration,
        "time_signature": track_features['time_signature'],
        "year": track_release_date[:4]
    }

