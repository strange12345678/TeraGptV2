# Theinertbotz/secondary_api.py
import re
import requests
import logging
from typing import Optional
from urllib.parse import quote
from Theinertbotz.debug_helper import save_html_debug, extract_error_message

log = logging.getLogger("TeraBoxBot")

def _extract_video_filename(file_data: dict) -> str:
    """Extract the cleanest available filename from API response."""
    # Check multiple fields in order of preference
    filename = (
        file_data.get('server_filename') or  # Full filename with metadata
        file_data.get('filename') or  # Simpler filename
        file_data.get('title') or  # Title field
        file_data.get('name') or  # Generic name field
        'video.mp4'  # Ultimate fallback
    )
    
    log.info(f"API fields available: {list(file_data.keys())}")
    log.info(f"Selected filename: {filename}")
    
    # Ensure .mp4 extension if needed
    if filename and not any(filename.lower().endswith(ext) for ext in ['.mp4', '.mkv', '.webm', '.mov']):
        filename = filename + '.mp4'
    
    return filename


def fetch_video_from_terabox_api(terabox_url: str, timeout=20):
    """
    Call the TeraBox API directly (the one iTeraPlay uses internally).
    Returns the m3u8 URL directly from API response.
    """
    # Use the same API endpoint that iTeraPlay uses
    api_url = "https://api.teraboxdownloader.online/api/get-info"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://iteraplay.com/",
        "Origin": "https://iteraplay.com",
    }
    
    try:
        # Make POST request with form data
        response = requests.post(
            api_url,
            data={'url': terabox_url},
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
        
        log.info(f"TeraBox API response: {data.keys() if isinstance(data, dict) else type(data)}")
        
        # Extract m3u8 from response
        if isinstance(data, dict) and 'list' in data and len(data['list']) > 0:
            file_data = data['list'][0]
            
            # Check fast_stream_url (contains quality options)
            if 'fast_stream_url' in file_data:
                stream_url = file_data['fast_stream_url']
                
                # If it's a dict with quality options
                if isinstance(stream_url, dict):
                    quality_order = ['1080p', '720p', '480p', '360p']
                    for quality in quality_order:
                        if quality in stream_url and stream_url[quality]:
                            log.info(f"Found {quality} stream URL from API")
                            return stream_url[quality], _extract_video_filename(file_data)
                    # Return first available quality
                    for url in stream_url.values():
                        if url:
                            log.info(f"Found stream URL from API (first available)")
                            return url, _extract_video_filename(file_data)
                # If it's a direct string URL
                elif isinstance(stream_url, str) and stream_url:
                    log.info(f"Found stream URL from API (direct)")
                    return stream_url, _extract_video_filename(file_data)
            
            # Fallback to other possible fields
            for field in ['dlink', 'download_url', 'stream_url', 'video_url']:
                if field in file_data and file_data[field]:
                    log.info(f"Found {field} from API")
                    return file_data[field], _extract_video_filename(file_data)
        
        log.warning("No valid stream URL found in API response")
        return None, None
        
    except Exception as e:
        log.error(f"Failed to fetch from TeraBox API: {e}")
        raise

def fetch_iteraplay_html(url: str, timeout=20):
    """
    Fetch HTML from iTeraPlay API endpoint.
    Returns HTML content that contains HLS video player.
    """
    # Properly URL encode the TeraBox link
    encoded_url = quote(url, safe=':/')
    api_url = f"https://iteraplay.com/api/play.php?url={encoded_url}&key=iTeraPlay2025"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://iteraplay.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    try:
        r = requests.get(api_url, timeout=timeout, headers=headers)
        r.raise_for_status()
        html = r.text
        
        if html and '.m3u8' not in html.lower() and 'error' in html.lower():
            log.warning(f"iTeraPlay returned error/unsupported link")
        
        return html
    except Exception as e:
        log.error(f"Failed to fetch iTeraPlay HTML: {e}")
        raise


def extract_m3u8_from_html(html: str):
    """
    Extract m3u8 URL from iTeraPlay HTML page.
    The page makes a POST request to an API endpoint to get video data.
    We need to extract the API endpoint and make the request ourselves.
    """
    if not html:
        return None
    
    # Debug: Save HTML for inspection if needed
    log.debug(f"HTML length: {len(html)} bytes")
    
    # First, try to extract the API endpoint URL from the JavaScript
    api_patterns = [
        r'const\s+apiUrl\s*=\s*["\']([^"\']+)["\']',
        r'apiUrl\s*=\s*["\']([^"\']+)["\']',
        r'fetch\s*\(\s*["\']([^"\']+api[^"\']*)["\']',
    ]
    
    api_endpoint = None
    for pattern in api_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            api_endpoint = match.group(1)
            log.info(f"Found API endpoint: {api_endpoint}")
            break
    
    # If we found an API endpoint, try to extract the TeraBox URL and make the request
    if api_endpoint:
        terabox_url_pattern = r'url\s*=\s*["\']([^"\']+terabox[^"\']*)["\']'
        match = re.search(terabox_url_pattern, html, re.IGNORECASE)
        if match:
            terabox_url = match.group(1)
            log.info(f"Found TeraBox URL in HTML: {terabox_url}")
            
            # Make the API request
            try:
                import requests
                response = requests.post(api_endpoint, data={'url': terabox_url}, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                log.info(f"API response received: {len(str(data))} bytes")
                
                # Extract m3u8 from API response
                if 'list' in data and len(data['list']) > 0:
                    file_data = data['list'][0]
                    
                    # Check fast_stream_url (contains quality options)
                    if 'fast_stream_url' in file_data:
                        stream_url = file_data['fast_stream_url']
                        
                        # If it's a dict with quality options
                        if isinstance(stream_url, dict):
                            quality_order = ['1080p', '720p', '480p', '360p']
                            for quality in quality_order:
                                if quality in stream_url and stream_url[quality]:
                                    log.info(f"Found {quality} stream URL from API")
                                    return stream_url[quality]
                            # Return first available quality
                            for url in stream_url.values():
                                if url:
                                    log.info(f"Found stream URL from API (first available)")
                                    return url
                        # If it's a direct string URL
                        elif isinstance(stream_url, str) and stream_url:
                            log.info(f"Found stream URL from API (direct)")
                            return stream_url
                    
                    # Fallback to other possible fields
                    for field in ['dlink', 'download_url', 'stream_url', 'video_url']:
                        if field in file_data and file_data[field]:
                            log.info(f"Found {field} from API")
                            return file_data[field]
                
            except Exception as e:
                log.error(f"Failed to fetch from API endpoint: {e}")
    
    # Fallback to HTML extraction
    urls_found = []
    
    # Extended pattern list with more variations
    m3u8_patterns = [
        # HLS patterns
        r'hls\.loadSource\s*\(\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'hlsPlayer\.loadSource\s*\(\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        
        # Stream URL patterns
        r'fast_stream_url\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'videoUrl\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'streamUrl\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'stream[_\s]*url\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'video[_\s]*url\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        
        # Source patterns
        r'src\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'url\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'href\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        
        # Data attributes
        r'data-src\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'data-stream\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'data-url\s*[:=]\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        
        # JSON patterns
        r'["\']m3u8["\']\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'["\']playlist["\']\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'["\']hls["\']\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
        
        # Generic m3u8 URL - catch any https URL ending with .m3u8
        r'(https?://[^\s"\'<>]*\.m3u8[^\s"\'<>]*)',
    ]
    
    for pattern in m3u8_patterns:
        try:
            matches = re.finditer(pattern, html, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                url = match.group(1).strip()
                if url and url.startswith(('http://', 'https://')) and '.m3u8' in url.lower():
                    urls_found.append(url)
                    log.debug(f"Found m3u8 URL: {url}")
        except Exception as e:
            log.debug(f"Regex pattern failed: {e}")
            continue
    
    # Try to extract from script tags - look for JSON data
    try:
        script_pattern = r'<script[^>]*>(.*?)</script>'
        for script_match in re.finditer(script_pattern, html, re.DOTALL | re.IGNORECASE):
            script_content = script_match.group(1)
            
            # Look for JSON objects in script
            json_patterns = [
                r'const\s+data\s*=\s*({[^;]+})',
                r'var\s+data\s*=\s*({[^;]+})',
                r'let\s+videoData\s*=\s*({[^;]+})',
            ]
            
            for json_pattern in json_patterns:
                json_match = re.search(json_pattern, script_content)
                if json_match:
                    try:
                        import json
                        json_str = json_match.group(1)
                        # Clean up the JSON string
                        json_str = json_str.replace("'", '"')
                        data = json.loads(json_str)
                        
                        # Look for m3u8 in the JSON
                        if isinstance(data, dict):
                            for key in ['m3u8', 'stream_url', 'video_url', 'url']:
                                if key in data and data[key]:
                                    log.info(f"Found m3u8 in script JSON: {data[key]}")
                                    return data[key]
                    except Exception as e:
                        log.debug(f"Failed to parse JSON from script: {e}")
    except Exception as e:
        log.debug(f"Script extraction failed: {e}")
    
    # Also try to extract from escaped/encoded URLs
    try:
        unescaped_html = html.replace('\\/', '/').replace('\\"', '"').replace("\\'", "'")
        generic_pattern = r'(https?://[^\s"\'<>]*\.m3u8[^\s"\'<>]*)'
        for match in re.finditer(generic_pattern, unescaped_html, re.IGNORECASE):
            url = match.group(1).strip()
            if url and url.startswith(('http://', 'https://')):
                urls_found.append(url)
                log.debug(f"Found m3u8 URL (unescaped): {url}")
    except Exception as e:
        log.debug(f"Unescaped pattern extraction failed: {e}")
    
    # Remove duplicates
    urls_found = list(set(urls_found))
    
    if not urls_found:
        log.warning("No m3u8 URLs found in HTML")
        
        # Save HTML for debugging
        save_html_debug(html, "iteraplay_failed")
        
        # Check if HTML is an error page
        if 'error' in html.lower() or 'not found' in html.lower():
            log.error(f"iTeraPlay returned error response")
            # Try to extract error message
            error_msg = extract_error_message(html)
            if error_msg:
                log.error(f"Error message: {error_msg}")
            return None
        
        if len(html) < 1000:
            log.error(f"Response too short (len={len(html)}), likely an error")
            return None
        
        # Try to extract any video stream URL as fallback
        log.info("Attempting fallback extraction methods...")
        video_patterns = [
            r'(https?://[^\s"\'<>]*?\.m3u8[^\s"\'<>]*)',  # m3u8 with different encoding
            r'(https?://[^\s"\'<>]*?/stream[^\s"\'<>]*)',
            r'(https?://[^\s"\'<>]*?video[^\s"\'<>]*)',
            r'(https?://[^\s"\'<>]*?hls[^\s"\'<>]*)',
            r'(https?://[^\s"\'<>]*?\.cdnext\.[^\s"\'<>]*)',  # CDN streams
            r'(https?://[^\s"\'<>]*?cdn[^\s"\'<>]*\.m3u8[^\s"\'<>]*)',
        ]
        for pattern in video_patterns:
            try:
                matches = re.finditer(pattern, html, re.IGNORECASE)
                for match in matches:
                    url = match.group(1).strip()
                    if url.startswith(('http://', 'https://')) and not url.endswith(('.js', '.css', '.html', '.png', '.jpg')):
                        log.info(f"Found fallback video URL: {url}")
                        return url
            except:
                pass
        return None
    
    # Prefer higher quality if multiple URLs exist
    quality_order = ['1080', '720', '480', '360']
    for quality in quality_order:
        for url in urls_found:
            if quality in url.lower():
                log.info(f"Selected {quality}p m3u8: {url}")
                return url
    
    # Return first/best one
    log.info(f"Selected m3u8: {urls_found[0]}")
    return urls_found[0]


def extract_filename_from_terabox_html(terabox_url: str) -> Optional[str]:
    """
    Extract the actual filename/folder name directly from TeraBox HTML.
    TeraBox HTML contains the file/folder name in title or data attributes.
    """
    try:
        import requests
        import html
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(terabox_url, headers=headers, timeout=10)
        response.raise_for_status()
        page_html = response.text
        
        # Try to extract filename from various sources in TeraBox HTML
        patterns = [
            # From share title in JavaScript (most reliable)
            r'share_title\s*:\s*["\']([^"\']+)["\']',
            # From data in JSON
            r'"name"\s*:\s*"([^"]+)"',
            r'"title"\s*:\s*"([^"]+)"',
            # From folder/file name in data attributes
            r'data-name="([^"]+)"',
            r'data-filename="([^"]+)"',
            # From h1 heading (might be the folder/file name)
            r'<h1[^>]*>([^<]+)</h1>',
            # Title from page title tag (least reliable - has page branding)
            r'<title>([^<]+)</title>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, page_html, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                
                # Decode HTML entities
                title = html.unescape(title)
                
                # Remove TeraBox page branding if present
                if ' - Share Files' in title or ' - ' in title and 'Tera' in title:
                    # Extract just the filename part before the dash
                    parts = title.split(' - ')
                    if parts[0]:
                        title = parts[0].strip()
                
                # Filter out unwanted titles
                excluded = ['video', 'download', 'untitled', 'terabox', 'share files']
                if title and len(title) > 3 and title.lower() not in excluded:
                    # Ensure it looks like a filename (not just words)
                    if any(char.isdigit() or char in '@_-.' for char in title):
                        log.info(f"Extracted filename from TeraBox HTML: {title}")
                        return title
                    
        log.info("No valid filename found in TeraBox HTML")
        return None
    except Exception as e:
        log.debug(f"Failed to extract from TeraBox HTML: {e}")
        return None


def extract_video_info_from_html(html: str):
    """
    Extract video title/filename from iTeraPlay HTML.
    Tries multiple extraction methods to find actual filename.
    """
    try:
        # Try to extract title from HTML with comprehensive patterns
        title_patterns = [
            # JavaScript variables for filename
            r'var\s+filename\s*=\s*["\']([^"\']+)["\']',
            r'filename\s*:\s*["\']([^"\']+)["\']',
            r'data-filename="([^"]+)"',
            # JSON objects with filename/title
            r'"filename"\s*:\s*"([^"]+)"',
            r'"file_name"\s*:\s*"([^"]+)"',
            r'"server_filename"\s*:\s*"([^"]+)"',
            # Meta tags and data attributes
            r'data-title="([^"]+)"',
            r'data-video-title="([^"]+)"',
            # Class-based title
            r'class="title"[^>]*>([^<]+)<',
            r'class="video-title"[^>]*>([^<]+)<',
            # Regular title tag
            r'<title>([^<]+)</title>',
            r'<h1[^>]*>([^<]+)</h1>',
            r'<h2[^>]*>([^<]+)</h2>',
            # Direct title property
            r'"title"\s*:\s*"([^"]+)"',
            r'"name"\s*:\s*"([^"]+)"',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Filter out common junk titles
                if title and len(title) > 3 and title.lower() not in ['video', 'download', 'untitled']:
                    log.info(f"Extracted title from HTML: {title} (pattern: {pattern})")
                    return title
    except Exception as e:
        log.warning(f"Failed to extract video info: {e}")
    
    log.info("No video title found in HTML patterns")
    return None
