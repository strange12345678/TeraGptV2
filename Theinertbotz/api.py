# Theinertbotz/api.py
import requests
import logging
from config import Config

log = logging.getLogger("TeraBoxBot")

def fetch_play_html(url: str, timeout=20):
    """
    Fetch the HTML returned by TeraBox API with failover support.
    Tries primary API first, then falls back to secondary API if primary fails.
    Caller should handle exceptions (HTTPError, Timeout, etc).
    """
    apis = [
        ("Primary (TeraAPI)", Config.TERAAPI_PLAY.format(url=url)),
        ("Secondary (iTeraPlay)", Config.ITERAPLAY_API.format(url=url))
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}
    last_error = None
    
    for api_name, api_url in apis:
        try:
            log.info(f"Trying {api_name}: {api_url[:50]}...")
            r = requests.get(api_url, timeout=timeout, headers=headers)
            r.raise_for_status()
            log.info(f"✅ {api_name} succeeded")
            return r.text
        except requests.exceptions.Timeout:
            last_error = f"{api_name} - Timeout"
            log.warning(f"❌ {api_name} timeout, trying next API...")
        except requests.exceptions.ConnectionError:
            last_error = f"{api_name} - Connection Error"
            log.warning(f"❌ {api_name} connection error, trying next API...")
        except requests.exceptions.HTTPError as e:
            last_error = f"{api_name} - HTTP {e.response.status_code}"
            log.warning(f"❌ {api_name} HTTP error {e.response.status_code}, trying next API...")
        except Exception as e:
            last_error = f"{api_name} - {str(e)}"
            log.warning(f"❌ {api_name} error: {str(e)}, trying next API...")
    
    # All APIs failed
    log.error(f"All APIs failed. Last error: {last_error}")
    raise Exception(f"Both APIs failed. Last error: {last_error}")
