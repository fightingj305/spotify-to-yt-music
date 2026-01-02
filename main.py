import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
# Authenticate
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                               scope=os.getenv("SCOPE")))

# Get the user's Spotify ID
user_id = sp.me()['id']

print(f"ID: {user_id}")

# Fetch user's playlists
playlists = sp.current_user_playlists()['items']

# Find the desired playlist by name
for playlist in playlists:
    if playlist['name'] == os.getenv("DESIRED_PLAYLIST"):
        print(f"Found playlist: {playlist['name']} with ID: {playlist['id']}")
        break
else:
    print(f"Playlist '{os.getenv("DESIRED_PLAYLIST")}' not found.")
    playlist = None



if playlist:
    results = sp.playlist_tracks(playlist['id'])
    tracks = results['items']

    # Handle 100-track limit
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for i, item in enumerate(tracks):
        track = item['track']
        print(f"Track {i+1}: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")