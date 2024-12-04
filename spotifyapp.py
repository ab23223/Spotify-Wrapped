from flask import Flask, jsonify, send_from_directory
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Spotify API credentials
SPOTIFY_CLIENT_ID = '6195c285300143c3b453e9ddf60d3fad'
SPOTIFY_CLIENT_SECRET = 'f3067bc3408f49b99c8c23f284862b2b'
SPOTIFY_REDIRECT_URI = 'https://open.spotify.com/'

# Spotify authentication scope
scope = "user-top-read"

# Spotipy client setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

@app.route('/')
def index():
    return send_from_directory('/spotify_wrapped.html')  # Serve the HTML page

@app.route('/get-top-items')
def get_top_items():
    try:
        # Fetch top tracks
        top_tracks_data = sp.current_user_top_tracks(limit=10, time_range='medium_term')
        top_tracks = [
            {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']]
            }
            for track in top_tracks_data['items']
        ]

        # Fetch top artists
        top_artists_data = sp.current_user_top_artists(limit=10, time_range='medium_term')
        top_artists = [
            {'name': artist['name']}
            for artist in top_artists_data['items']
        ]

        return jsonify({'topTracks': top_tracks, 'topArtists': top_artists})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
