import subprocess
import os
from typing import Tuple, Optional
from config import logger

def generate_thumbnail(video_path: str, at_sec: int = 2) -> Optional[str]:
    thumb = video_path + ".jpg"
    try:
        cmd = [
            "ffmpeg",
            "-ss", f"00:00:{at_sec:02d}",
            "-i", video_path,
            "-vframes", "1",
            "-vf", "scale=320:-1",
            "-y",
            thumb
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if os.path.exists(thumb):
            return thumb
    except Exception as e:
        logger.error(f"Thumbnail generation failed: {e}")
    return None

def get_metadata(video_path: str) -> Tuple[int,int,float]:
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration",
            "-of", "csv=p=0",
            video_path
        ], stderr=subprocess.PIPE).decode().strip().split(",")
        width = int(out[0]) if out and out[0] else 720
        height = int(out[1]) if len(out) > 1 and out[1] else 1280
        duration = float(out[2]) if len(out) > 2 and out[2] else 1.0
        if duration < 1:
            duration = 1.0
        return width, height, duration
    except Exception as e:
        logger.warning(f"Metadata extraction failed: {e}")
        return 720, 1280, 60.0

def human_size(path: str) -> str:
    try:
        s = os.path.getsize(path)
        mb = s / (1024*1024)
        if mb < 1:
            return f"{s/1024:.2f} KB"
        return f"{mb:.2f} MB"
    except:
        return "Unknown"
