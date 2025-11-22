import requests
import os
from typing import Callable, Optional
from config import logger

CHUNK = 1024 * 256

def download_file(url: str, dest: str,
                  progress: Optional[Callable[[int,int], None]] = None,
                  max_retries: int = 2) -> str:
    """
    Synchronous downloader (safe to run inside asyncio.to_thread).
    Calls progress(downloaded, total) if provided (sync).
    """
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                total = int(r.headers.get("Content-Length", 0) or 0)
                downloaded = 0
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(CHUNK):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress:
                            try:
                                progress(downloaded, total)
                            except Exception:
                                logger.debug("Progress callback error ignored")
                                pass
            return dest
        except Exception as e:
            last_exc = e
            logger.warning(f"Download attempt {attempt} failed: {e}")
            if attempt == max_retries:
                raise
    raise last_exc
