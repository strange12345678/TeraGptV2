# Theinertbotz/secondary_api.py
import re
import requests
import logging
import asyncio
import json
from urllib.parse import quote

log = logging.getLogger("TeraBoxBot")

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
        
        # Log first 500 chars for debugging if no m3u8 found
        if html and '.m3u8' not in html.lower() and 'error' in html.lower():
            log.warning(f"iTeraPlay returned error HTML: {html[:500]}")
        
        return html
    except Exception as e:
        log.error(f"Failed to fetch iTeraPlay HTML: {e}")
        raise


async def extract_m3u8_with_browser(url: str, timeout=30):
    """
    Extract m3u8 using Playwright headless browser (executes JavaScript).
    This is needed because iTeraPlay loads the m3u8 URL via JavaScript.
    """
    try:
        from playwright.async_api import async_playwright
        
        encoded_url = quote(url, safe=':/')
        api_url = f"https://iteraplay.com/api/play.php?url={encoded_url}&key=iTeraPlay2025"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Navigate to the page
                await page.goto(api_url, wait_until="networkidle", timeout=timeout*1000)
                
                # Wait for video player to load
                await asyncio.sleep(3)
                
                # Try to extract m3u8 from page content
                content = await page.content()
                m3u8 = extract_m3u8_from_html(content)
                
                if m3u8:
                    log.info(f"Extracted m3u8 via browser: {m3u8}")
                    return m3u8
                
                # Try to intercept XHR/fetch requests for the m3u8
                async def handle_response(response):
                    try:
                        if 'm3u8' in response.url.lower():
                            log.info(f"Intercepted m3u8 request: {response.url}")
                            return response.url
                    except:
                        pass
                    return None
                
                # Check network requests
                requests_log = page.context.tracing
                log.info(f"Page content length: {len(content)}")
                
            finally:
                await browser.close()
                
    except ImportError:
        log.warning("Playwright not installed, skipping browser extraction")
        return None
    except Exception as e:
        log.error(f"Browser extraction failed: {e}")
        return None
    
    return None


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
        
        # Check if HTML is an error page
        if 'error' in html.lower() or 'not found' in html.lower() or len(html) < 1000:
            log.error(f"iTeraPlay returned error/empty response (len={len(html)})")
            return None
        
        # Try to extract any video stream URL as fallback
        video_patterns = [
            r'(https?://[^\s"\'<>]*?\.m3u8[^\s"\'<>]*)',  # m3u8 with different encoding
            r'(https?://[^\s"\'<>]*?/stream[^\s"\'<>]*)',
            r'(https?://[^\s"\'<>]*?video[^\s"\'<>]*)',
            r'(https?://[^\s"\'<>]*?hls[^\s"\'<>]*)',
            r'(https?://[^\s"\'<>]*?\.cdnext\.[^\s"\'<>]*)',  # CDN streams
            r'(https?://[^\s"\'<>]*?cdn[^\s"\'<>]*)',
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
