from flask import Flask, jsonify, send_from_directory, render_template, request
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotifyapp

app = Flask(__name__)

# Spotify API credentials
SPOTIFY_CLIENT_ID = '6195c285300143c3b453e9ddf60d3fad'
SPOTIFY_CLIENT_SECRET = 'f3067bc3408f49b99c8c23f284862b2b'
SPOTIFY_REDIRECT_URI = 'https://open.spotify.com/'

# Spotify authentication scope

scope = "user-top-read user-read-recently-played"



# Spotipy client setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/get-recently-played')
def get_recently_played():
    try:
        limit = int(request.args.get('limit', 10))
        limit = max(1, min(limit, 50))  # Ensure the limit is between 1 and 50

        # Fetch recently played tracks (Spotify allows up to 50 recently played tracks)
        recent_tracks_data = sp.current_user_recently_played(limit=limit - 1)  # Fetch one less to include the custom track

        # Extract track names, artist names, and track URLs
        recently_played = [
            {
                'name': track['track']['name'],
                'artists': [artist['name'] for artist in track['track']['artists']],
                'url': track['track']['external_urls']['spotify']
            }
            for track in recent_tracks_data['items']
        ]

        # Add the custom song
        custom_song = {
            'name': "Stand Up (Kick Love into Motion)",
            'artists': ["Def Leppard"],
            'url': "https://open.spotify.com/track/0dr71rw5oIcPtUHRJES6gP?si=6766bb5ae24f4d50"
            
        }
        recently_played.insert(0, custom_song)  # Add the custom song at the top of the list

        return jsonify({'recentlyPlayed': recently_played})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get-top-items')
def get_top_items():
    try:
        # Get the limit from query parameters (default to 10 if not provided)
        limit = int(request.args.get('limit', 10))
        limit = max(1, min(limit, 50))  # Ensure the limit is between 1 and 200

        # Fetch top tracks
        top_tracks_data = sp.current_user_top_tracks(limit=limit, time_range='long_term')
        top_tracks = [
            {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']]
            }
            for track in top_tracks_data['items']
        ]

        # Fetch top artists
        top_artists_data = sp.current_user_top_artists(limit=limit, time_range='long_term')
        top_artists = [
            {'name': artist['name']}
            for artist in top_artists_data['items']
        ]

        # Calculate total listening time
        total_minutes = sum(track['duration_ms'] for track in top_tracks_data['items']) // 60000


        # Aggregate genres from top artists
        genre_count = {}
        for artist in top_artists_data['items']:
            for genre in artist['genres']:
                genre_count[genre] = genre_count.get(genre, 0) + 1

        # Sort genres by count
        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        top_genres = [{'genre': genre, 'count': count} for genre, count in sorted_genres]


        # Favorite track and artist
        favorite_track = top_tracks[0] if top_tracks else None
        favorite_artist = top_artists[0] if top_artists else None

        return jsonify({
            'topTracks': top_tracks,
            'topArtists': top_artists,
            'topGenres': top_genres,
            'totalMinutes': total_minutes,
            'favoriteTrack': favorite_track,
            'favoriteArtist': favorite_artist
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
