from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
import os, requests
from fastapi import Request

from urllib.parse import urlencode
import base64
from dotenv import load_dotenv


load_dotenv()


router = APIRouter()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://127.0.0.1:8000/auth/callback")
FRONTEND_URL = "http://localhost:5173"


@router.get("/auth/login")
def login():
    url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=user-library-read playlist-read-private"
    )
    return RedirectResponse(url)

@router.get("/auth/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code provided"}

    # Exchange the code for an access token
    token_response = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return {"error": "Failed to obtain access token", "details": token_json}

    return RedirectResponse(f"{FRONTEND_URL}/#access_token={access_token}")
