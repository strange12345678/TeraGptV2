# Theinertbotz/secondary_api.py
import re
import requests
import logging

log = logging.getLogger("TeraBoxBot")

def fetch_iteraplay_html(url: str, timeout=20):
    """
    Fetch HTML from iTeraPlay API endpoint.
    Returns HTML content that contains HLS video player.
    """
    api_url = f"https://iteraplay.com/api/play.php?url={url}&key=iTeraPlay2025"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        r = requests.get(api_url, timeout=timeout, headers=headers)
        r.raise_for_status()
        return r.text
    except Exception as e:
        log.error(f"Failed to fetch iTeraPlay HTML: {e}")
        raise


def extract_m3u8_from_html(html: str):
    """
    Extract m3u8 URL from iTeraPlay HTML page.
    Searches for patterns like:
    - hls.loadSource("https://...index.m3u8")
    - fast_stream_url: "https://...m3u8"
    - Quality URLs (360p, 480p, 720p, 1080p)
    - Direct .m3u8 links
    - Video source in script tags
    """
    if not html:
        return None
    
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
        # Try to extract any video stream URL as fallback
        video_patterns = [
            r'(https?://[^\s"\'<>]*?/stream[^\s"\'<>]*)',
            r'(https?://[^\s"\'<>]*?video[^\s"\'<>]*)',
        ]
        for pattern in video_patterns:
            try:
                matches = re.finditer(pattern, html, re.IGNORECASE)
                for match in matches:
                    url = match.group(1).strip()
                    if url.startswith(('http://', 'https://')):
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


def extract_video_info_from_html(html: str):
    """
    Extract video title/filename from iTeraPlay HTML.
    """
    try:
        # Try to extract title from HTML
        title_patterns = [
            r'<title>([^<]+)</title>',
            r'data-title="([^"]+)"',
            r'class="title"[^>]*>([^<]+)<',
            r'"title"\s*:\s*"([^"]+)"',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if title and len(title) > 3:
                    return title
    except Exception as e:
        log.warning(f"Failed to extract video info: {e}")
    
    return None
