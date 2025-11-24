# Theinertbotz/api.py
import requests
from config import Config

def fetch_play_html(url: str, timeout=20):
    """
    Fetch the HTML returned by the teraapi play endpoint.
    Caller should handle exceptions (HTTPError, Timeout, etc).
    """
    api_url = Config.TERAAPI_PLAY.format(url=url)
    r = requests.get(api_url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text
