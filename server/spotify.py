from fastapi import APIRouter, Header, HTTPException
import requests

router = APIRouter()

@router.get("/spotify/playlists")
def get_playlists(authorization: str = Header(...)):
    headers = {"Authorization": authorization}
    res = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    return res.json()

def get_liked_songs(token: str, limit: int = 50, offset: int = 0):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}"
    response = requests.get(url, headers=headers)
    return response.json()

@router.get("/spotify/liked")
def fetch_liked_songs(
    authorization: str = Header(None),
    limit: int = 50,
    offset: int = 0
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

    token = authorization.split("Bearer ")[1]
    data = get_liked_songs(token, limit=limit, offset=offset)
    return data

def get_playlist_tracks(token: str, playlist_id: str, limit: int = 100, offset: int = 0):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}&offset={offset}"
    response = requests.get(url, headers=headers)
    return response.json()

@router.get("/spotify/playlist-tracks/{playlist_id}")
def fetch_playlist_tracks(
    playlist_id: str,
    authorization: str = Header(None),
    limit: int = 100,
    offset: int = 0
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

    token = authorization.split("Bearer ")[1]
    data = get_playlist_tracks(token, playlist_id, limit=limit, offset=offset)
    return data