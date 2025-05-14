from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os, requests
from urllib.parse import urlencode
import base64
from dotenv import load_dotenv


load_dotenv()


router = APIRouter()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://127.0.0.1:8000/auth/callback")

@router.get("/auth/token")
def get_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return JSONResponse(content=res.json(), status_code=res.status_code)

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
