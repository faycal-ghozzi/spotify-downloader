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
    return RedirectResponse(
        f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code"
        f"&redirect_uri={REDIRECT_URI}&scope=user-library-read playlist-read-private"
    )

@app.get("/callback")
def callback(code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
    return r.json()
