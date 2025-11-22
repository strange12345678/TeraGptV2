import requests
import re
from typing import Optional
from config import Config, logger

API_BASE = "https://teraapi.boogafantastic.workers.dev/play?url="

def fetch_play_html(url: str, timeout: int = 30) -> str:
    api_url = API_BASE + url
    logger.info(f"Fetching play page via API: {api_url}")
    r = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    return r.text

def extract_direct_url_from_html(html: str) -> Optional[str]:
    # try common patterns
    patterns = [
        r'href="(https?://data[^"]+)"',
        r'"(https?://data\.[^"]+)"',
        r"streamUrl\s*[:=]\s*'([^']+)'",
        r"streamUrl\s*[:=]\s*\"([^\"]+)\"",
    ]
    for p in patterns:
        m = re.search(p, html)
        if m:
            return m.group(1)
    return None

def extract_filename(html: str, direct_url: Optional[str] = None) -> str:
    # try title tag
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        # sanitize title
        title = re.sub(r"[\n\r]+", " ", title)
        return title or (direct_url.split("/")[-1] if direct_url else "file.bin")
    if direct_url:
        return direct_url.split("/")[-1].split("?")[0]
    return "file.bin"
