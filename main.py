from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import Form
from utility import get_video_formats, download_video, download_audio_with_metadata
from fastapi.responses import FileResponse
import uvicorn
from fastapi import HTTPException
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@app.post("/info")
def info(url: str):
    return get_video_formats(url)

@app.post("/download")
def download(url: str = Form(...), format_id: str = Form(...)):
    output_template = 'downloads/%(title)s.%(ext)s'
    result = download_video(url, format_id, output_path_template=output_template)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    files = result.get("paths", [])
    urls = [f"http://122.182.161.97:9600/downloads/{os.path.basename(f)}" for f in files]

    return {"status": "success", "download_urls": urls}

@app.post('/music_download')
def music_download(url: str = Form(...)):
    result = download_audio_with_metadata(url)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    files = result.get("paths", [])
    urls = [f"http://122.182.161.97:9600/downloads/{os.path.basename(f)}" for f in files]

    return {"status": "success", "download_urls": urls}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    