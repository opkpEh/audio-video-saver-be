import yt_dlp
import json

def download_video(url: str, format_id: str, output_path_template: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': format_id,
        'outtmpl': output_path_template,
        'ignoreerrors': True,   
        'yesplaylist': True,   
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            
            if 'entries' in info_dict:
                files = []
                for entry in info_dict['entries']:
                    if entry is None:
                        continue
                    filepath = ydl.prepare_filename(entry)
                    files.append(filepath)
                return {"status": "success", "paths": files}
            else:
                filepath = ydl.prepare_filename(info_dict)
                return {"status": "success", "paths": [filepath]}
    except yt_dlp.utils.DownloadError:
        return {"error": "Failed to download video"}


def download_audio_with_metadata(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'writethumbnail': True,
        'embed-thumbnail': True,
        'addmetadata': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True
            },
            {
                'key': 'EmbedThumbnail',
            }
        ],
        'ignoreerrors': True,
        'yesplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            files = []
            if 'entries' in info_dict:
                for entry in info_dict['entries']:
                    if entry is None:
                        continue
                    filepath = ydl.prepare_filename(entry).rsplit(".", 1)[0] + ".mp3"
                    files.append(filepath)
            else:
                filepath = ydl.prepare_filename(info_dict).rsplit(".", 1)[0] + ".mp3"
                files.append(filepath)
            return {"status": "success", "paths": files}
    except yt_dlp.utils.DownloadError:
        return {"error": "Failed to download audio"}

def get_video_formats(url: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError:
            return {'error': 'Video not found or unavailable'}

        formats = info_dict.get('formats', [])
        
        best_video_audio = None
        audio_only = None
        video_480p_audio = None

        for f in formats:
            vcodec = f.get("vcodec")
            acodec = f.get("acodec")
            height = f.get("height")

            if vcodec == "none" and acodec != "none":
                if not audio_only or (f.get("abr") or 0) > (audio_only.get("abr") or 0):
                    audio_only = f

            if vcodec != "none" and acodec != "none":
                if not best_video_audio or f.get("height", 0) > best_video_audio.get("height", 0):
                    best_video_audio = f

                if height == 480 and not video_480p_audio:
                    video_480p_audio = f

        result = {
            "title": info_dict.get("title"),
            "uploader": info_dict.get("uploader"),
            "duration_sec": info_dict.get("duration"),
            "best_video_audio": extract_format_info(best_video_audio),
            "best_audio_only": extract_format_info(audio_only)
        }

        return result

def extract_format_info(format_obj):
    if not format_obj:
        return None
    return {
        'format_id': format_obj.get('format_id'),
        'ext': format_obj.get('ext'),
        'resolution': f"{format_obj.get('width')}x{format_obj.get('height')}" if format_obj.get('height') else None,
        'fps': format_obj.get('fps'),
        'filesize': format_obj.get('filesize'),
        'video_codec': format_obj.get('vcodec'),
        'audio_codec': format_obj.get('acodec'),
    }