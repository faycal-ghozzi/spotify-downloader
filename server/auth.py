from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os, requests
from urllib.parse import urlencode

router = APIRouter()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")

@router.get("/auth/login")
def login():
    scope = "user-library-read playlist-read-private"
    query = urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope
    })
    return RedirectResponse(f"https://accounts.spotify.com/authorize?{query}")

@router.get("/auth/callback")
def callback(code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
    return res.json()
