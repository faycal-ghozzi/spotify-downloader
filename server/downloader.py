from fastapi import APIRouter, Body, Request, HTTPException
from yt_dlp import YoutubeDL
import yt_dlp
import threading


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

def search_and_download_youtube(query: str, output_dir: str = "downloads"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': '/opt/homebrew/bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            return {"status": "ok", "title": info["title"]}
        except Exception as e:
            return {"status": "error", "error": str(e)}

        
@router.post("/download/track")
async def download_track(request: Request):
    body = await request.json()
    track_name = body.get("name")
    artist_name = body.get("artist")
    if not track_name or not artist_name:
        raise HTTPException(status_code=400, detail="Missing track or artist")

    query = f"{track_name} {artist_name}"
    result = search_and_download_youtube(query)
    return result


@router.post("/download/all")
async def download_all(request: Request):
    body = await request.json()
    tracks = body.get("tracks", [])
    if not tracks:
        raise HTTPException(status_code=400, detail="No tracks provided")

    def background_download():
        for t in tracks:
            name = t.get("name")
            artist = t.get("artists", [{}])[0].get("name")
            if name and artist:
                query = f"{name} {artist}"
                search_and_download_youtube(query)

    threading.Thread(target=background_download).start()

    return {"status": "started", "count": len(tracks)}