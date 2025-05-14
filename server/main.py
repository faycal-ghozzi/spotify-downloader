from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from spotify import router as spotify_router
from downloader import router as downloader_router
import subprocess
import shlex


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/preview")
async def get_preview(request: Request):
    data = await request.json()
    track = data.get("name")
    artist = data.get("artist")

    if not track or not artist:
        return {"error": "Missing name or artist"}

    try:
        escaped_track = shlex.quote(track)
        escaped_artist = shlex.quote(artist)

        cmd = f"node get_preview.js {escaped_track} {escaped_artist}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return {"preview_url": result.stdout.strip()}
        else:
            return {"error": result.stderr.strip()}
    except Exception as e:
        return {"error": str(e)}

app.include_router(auth_router)
app.include_router(spotify_router)
app.include_router(downloader_router)
