import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up authentication
SPOTIFY_CLIENT_ID = '6195c285300143c3b453e9ddf60d3fad'
SPOTIFY_CLIENT_SECRET = 'f3067bc3408f49b99c8c23f284862b2b'
SPOTIFY_REDIRECT_URI = 'https://open.spotify.com/'

scope = "user-top-read"

# Authenticate
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

# Fetch user top tracks and artists
def get_top_items():
    print("Fetching your Spotify Wrapped...")

    # Get top tracks
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='long_term')
    print("\nYour Top 50 Tracks:")
    for idx, item in enumerate(top_tracks['items']):
        print(f"{idx + 1}. {item['name']} by {', '.join(artist['name'] for artist in item['artists'])}")

    # Get top artists

    top_artists = sp.current_user_top_artists(limit=50, time_range='long_term')
    print("\nYour Top 50 Artists:")
    for idx, artist in enumerate(top_artists['items']):
        print(f"{idx + 1}. {artist['name']}")

# Run the program
if __name__ == "__main__":
    get_top_items()
