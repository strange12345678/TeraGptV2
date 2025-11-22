import os
import subprocess
import logging

log = logging.getLogger("TeraBoxBot")

def generate_thumbnail(video_path: str, output_path: str = None) -> str:
    """
    Generate thumbnail from video file at 25% into the video.
    Returns path to thumbnail or None if failed.
    """
    if not output_path:
        base_name = os.path.splitext(video_path)[0]
        output_path = f"{base_name}_thumb.jpg"
    
    try:
        # Get video duration first
        duration_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1:nokey=1",
            video_path
        ]
        
        try:
            result = subprocess.run(duration_cmd, capture_output=True, text=True, timeout=10)
            duration = float(result.stdout.strip())
        except:
            duration = 5  # fallback: capture at 5 seconds
        
        # Capture at 25% of duration
        seek_time = max(2, int(duration * 0.25))
        
        cmd = [
            "ffmpeg", "-i", video_path,
            "-ss", str(seek_time),
            "-vframes", "1",
            "-vf", "scale=320:180",
            "-y",  # overwrite
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(output_path):
            log.info(f"Thumbnail generated: {output_path}")
            return output_path
        else:
            log.warning(f"ffmpeg failed: {result.stderr.decode()}")
            return None
            
    except Exception as e:
        log.warning(f"Thumbnail generation failed: {e}")
        return None

__all__ = ["generate_thumbnail"]
