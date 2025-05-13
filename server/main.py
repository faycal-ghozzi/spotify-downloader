from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import os
import requests

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "user-library-read playlist-read-private"

app = FastAPI()

@app.get("/login")
def login():
    url = f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    return RedirectResponse(url)

