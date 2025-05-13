from fastapi import APIRouter, Body
from yt_dlp import YoutubeDL

router = APIRouter()

@router.post("/download")
def download(track: dict = Body(...)):
    query = f"{track['artist']} - {track['name']}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"./downloads/%(title)s.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])
    return {"status": "Downloaded", "query": query}
