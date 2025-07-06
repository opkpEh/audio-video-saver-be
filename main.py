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
    print(f"DEBUG: Received download request")
    print(f"DEBUG: URL: {url}")
    print(f"DEBUG: Format ID: {format_id}")
    
    output_template = 'downloads/%(title)s.%(ext)s'
    result = download_video(url, format_id, output_path_template=output_template)

    print(f"DEBUG: Download result: {result}")

    if "error" in result:
        print(f"DEBUG: Error in download: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])

    files = result.get("paths", [])
<<<<<<< HEAD
    urls = [f"http://zap-save.duckdns.org:9600/downloads/{os.path.basename(f)}" for f in files]
=======
    urls = [f"http://122.182.161.97:9600/downloads/{os.path.basename(f)}" for f in files]
>>>>>>> dc599443c8f5d82a1490edae93fd1639db6fb8b4

    print(f"DEBUG: Generated URLs: {urls}")
    return {"status": "success", "download_urls": urls}

@app.post('/music_download')
def music_download(url: str = Form(...)):
    print(f"DEBUG: Received music download request")
    print(f"DEBUG: URL: {url}")
    
    result = download_audio_with_metadata(url)
    
    print(f"DEBUG: Audio download result: {result}")

    if "error" in result:
        print(f"DEBUG: Error in audio download: {result['error']}")
        raise HTTPException(status_code=400, detail=result["error"])

    files = result.get("paths", [])
<<<<<<< HEAD
    urls = [f"http://zap-save.duckdns.org:9600/downloads/{os.path.basename(f)}" for f in files]
=======
    urls = [f"http://122.182.161.97:9600/downloads/{os.path.basename(f)}" for f in files]
>>>>>>> dc599443c8f5d82a1490edae93fd1639db6fb8b4

    print(f"DEBUG: Generated audio URLs: {urls}")
    return {"status": "success", "download_urls": urls}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9600, log_level="debug")
    
