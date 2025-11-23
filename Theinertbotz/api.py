# Theinertbotz/api.py
import requests
import logging
from urllib.parse import quote
from config import Config

log = logging.getLogger("TeraBoxBot")

def fetch_play_html(url: str, timeout=20):
    """
    Fetch the HTML returned by TeraBox API with failover support.
    Returns tuple: (html_content, api_source) where api_source is 'teraapi' or 'iteraplay'
    Tries primary API first, then falls back to secondary API if primary fails.
    Caller should handle exceptions (HTTPError, Timeout, etc).
    """
    from Theinertbotz.database import db
    
    # URL-encode the parameters properly
    encoded_url = quote(url, safe=':/?=&')
    
    # Get primary and secondary APIs from database
    primary_api = db.get_primary_api()
    secondary_api = db.get_secondary_api()
    
    # Build API URLs based on settings
    api_map = {
        "teraapi": ("TeraAPI", Config.TERAAPI_PLAY.format(url=encoded_url)),
        "iteraplay": ("iTeraPlay", Config.ITERAPLAY_API.format(url=encoded_url))
    }
    
    apis = [
        (primary_api, f"Primary ({api_map[primary_api][0]})", api_map[primary_api][1]),
        (secondary_api, f"Secondary ({api_map[secondary_api][0]})", api_map[secondary_api][1])
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}
    last_error = None
    
    for api_type, api_name, api_url in apis:
        try:
            log.info(f"Trying {api_name}: {api_url[:60]}...")
            r = requests.get(api_url, timeout=timeout, headers=headers)
            r.raise_for_status()
            log.info(f"✅ {api_name} succeeded (response: {len(r.text)} bytes)")
            return r.text, api_type  # Return both content and API type
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
