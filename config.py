from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore')
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv()
SPOTIFY_CLIENT_SECRET = os.getenv()
OPENAI_API_KEY = os.getenv()

assert SPOTIFY_CLIENT_ID != "your_client_id_here", "Set your Spotify Client ID in .env"
assert SPOTIFY_CLIENT_SECRET != "your_client_secret_here", "Set your Spotify Client Secret in .env"

print("Configurations set.")

