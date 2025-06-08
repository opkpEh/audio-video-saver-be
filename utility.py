import yt_dlp
import os
import urllib.parse

def get_video_formats(url):
    """
    Get video information and available formats
    Make sure to include thumbnail URL in the response
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            # Check if info extraction was successful
            if not isinstance(info, dict):
                return {'error': f'Failed to extract video info: {info}'}
            
            # Extract relevant information
            video_info = {
                'title': info.get('title', 'Unknown Title'),
                'uploader': info.get('uploader', 'Unknown'),
                'duration_sec': info.get('duration', 0),
                'thumbnail': info.get('thumbnail'),
                'thumbnail_url': info.get('thumbnail'),
                'formats': info.get('formats', []),
                'best_video_audio': None
            }
            
            # Find best video+audio format with better error handling
            formats = info.get('formats', [])
            if not formats:
                print("DEBUG: No formats found")
                return video_info
            
            for fmt in formats:
                try:
                    # Check if format has both video and audio
                    vcodec = fmt.get('vcodec', 'none')
                    acodec = fmt.get('acodec', 'none')
                    format_id = fmt.get('format_id')
                    
                    print(f"DEBUG: Checking format {format_id}: vcodec={vcodec}, acodc={acodec}")
                    
                    if (vcodec != 'none' and acodec != 'none' and 
                        vcodec is not None and acodec is not None and
                        format_id is not None):
                        
                        video_info['best_video_audio'] = {
                            'format_id': str(format_id),  # Ensure it's a string
                            'ext': fmt.get('ext', 'mp4'),
                            'resolution': fmt.get('resolution', 'Unknown')
                        }
                        print(f"DEBUG: Selected format: {video_info['best_video_audio']}")
                        break
                        
                except Exception as fmt_error:
                    print(f"DEBUG: Error processing format {fmt}: {fmt_error}")
                    continue
            
            # If no combined format found, try to find separate video and audio
            if video_info['best_video_audio'] is None:
                print("DEBUG: No combined format found, looking for video-only format")
                for fmt in formats:
                    try:
                        vcodec = fmt.get('vcodec', 'none')
                        format_id = fmt.get('format_id')
                        
                        if (vcodec != 'none' and vcodec is not None and 
                            format_id is not None):
                            
                            video_info['best_video_audio'] = {
                                'format_id': str(format_id),
                                'ext': fmt.get('ext', 'mp4'),
                                'resolution': fmt.get('resolution', 'Unknown')
                            }
                            print(f"DEBUG: Selected video-only format: {video_info['best_video_audio']}")
                            break
                            
                    except Exception as fmt_error:
                        print(f"DEBUG: Error processing video format {fmt}: {fmt_error}")
                        continue
            
            return video_info
            
        except Exception as e:
            print(f"DEBUG: Exception in get_video_formats: {e}")
            return {'error': str(e)}

def download_video(url: str, format_id, output_path_template='downloads/%(title)s.%(ext)s'):
    """
    Download video with specified format
    Use sanitized filenames to handle non-English characters
    """
    ydl_opts = {
        'format': format_id,
        'outtmpl': output_path_template,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract info first to get the filename
            info = ydl.extract_info(url, download=False)
            
            # Check if info is actually a dictionary - this is the key fix
            if not isinstance(info, dict):
                print(f"DEBUG: extract_info returned non-dict: {type(info)} - {info}")
                return {'error': f'Failed to extract video info: {info}'}
            
            # Additional check to ensure we have the required data
            if not info:
                return {'error': 'No video information could be extracted'}
            
            # Create sanitized filename
            title = info.get('title', 'video')
            
            # Find the format to get the extension
            ext = 'mp4'  # default
            formats = info.get('formats', [])
            for fmt in formats:
                if fmt.get('format_id') == format_id:
                    ext = fmt.get('ext', 'mp4')
                    break
            
            # Sanitize filename for filesystem
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_title:
                safe_title = 'video'
            
            filename = f"{safe_title}.{ext}"
            filepath = os.path.join('downloads', filename)
            
            # Make sure downloads directory exists
            os.makedirs('downloads', exist_ok=True)
            
            # Update output template with sanitized filename
            ydl_opts['outtmpl'] = filepath
            
            # Create new YoutubeDL instance with updated options for actual download
            with yt_dlp.YoutubeDL(ydl_opts) as download_ydl:
                download_ydl.download([url])
            
            return {
                'status': 'success',
                'paths': [filepath]
            }
            
        except Exception as e:
            print(f"DEBUG: Exception in download_video: {e}")
            return {'error': str(e)}

def download_audio_with_metadata(url):
    """
    Download audio with metadata
    Use sanitized filenames to handle non-English characters
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract info first to get the filename
            info = ydl.extract_info(url, download=False)
            
            # Check if info is actually a dictionary - this is the key fix
            if not isinstance(info, dict):
                print(f"DEBUG: extract_info returned non-dict: {type(info)} - {info}")
                return {'error': f'Failed to extract audio info: {info}'}
            
            # Additional check to ensure we have the required data
            if not info:
                return {'error': 'No video information could be extracted'}
                
            # Create sanitized filename
            title = info.get('title', 'audio')
            
            # Sanitize filename for filesystem
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_title:
                safe_title = 'audio'
            
            filename = f"{safe_title}.mp3"
            filepath = os.path.join('downloads', filename)
            
            # Make sure downloads directory exists
            os.makedirs('downloads', exist_ok=True)
            
            # Update output template with sanitized filename
            ydl_opts['outtmpl'] = filepath.replace('.mp3', '.%(ext)s')
            
            # Create new YoutubeDL instance with updated options for actual download
            with yt_dlp.YoutubeDL(ydl_opts) as download_ydl:
                download_ydl.download([url])
            
            return {
                'status': 'success',
                'paths': [filepath]
            }
            
        except Exception as e:
            print(f"DEBUG: Exception in download_audio_with_metadata: {e}")
            return {'error': str(e)}