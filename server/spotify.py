from fastapi import APIRouter, Header
import requests

router = APIRouter()

@router.get("/spotify/playlists")
def get_playlists(authorization: str = Header(...)):
    headers = {"Authorization": authorization}
    res = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    return res.json()

@router.get("/spotify/liked")
def get_liked(authorization: str = Header(...)):
    headers = {"Authorization": authorization}
    res = requests.get("https://api.spotify.com/v1/me/tracks", headers=headers)
    return res.json()
