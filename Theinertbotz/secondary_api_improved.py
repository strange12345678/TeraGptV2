import re
import requests
import logging
import asyncio
from urllib.parse import quote
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

log = logging.getLogger("TeraBoxBot")

async def extract_m3u8_with_playwright(terabox_url: str, timeout=45):
    """
    Use Playwright to load the iTeraPlay page and extract the m3u8 URL.
    This handles cookies, JavaScript execution, and network requests properly.
    """
    encoded_url = quote(terabox_url, safe=':/')
    api_url = f"https://iteraplay.com/api/play.php?url={encoded_url}&key=iTeraPlay2025"
    
    m3u8_url = None
    video_title = None
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            # List to capture network requests
            captured_urls = []
            
            async def handle_response(response):
                """Capture API responses that contain video data"""
                try:
                    url = response.url
                    # Look for API responses
                    if 'api' in url.lower() or 'worker' in url.lower():
                        if response.status == 200:
                            try:
                                data = await response.json()
                                log.info(f"Captured API response from: {url}")
                                
                                # Extract m3u8 from the response
                                if isinstance(data, dict) and 'list' in data and len(data['list']) > 0:
                                    file_data = data['list'][0]
                                    
                                    # Get video title
                                    nonlocal video_title
                                    video_title = file_data.get('server_filename', 'video.mp4')
                                    
                                    # Check fast_stream_url
                                    if 'fast_stream_url' in file_data:
                                        stream_url = file_data['fast_stream_url']
                                        
                                        if isinstance(stream_url, dict):
                                            quality_order = ['1080p', '720p', '480p', '360p']
                                            for quality in quality_order:
                                                if quality in stream_url and stream_url[quality]:
                                                    log.info(f"Found {quality} stream URL")
                                                    captured_urls.append(stream_url[quality])
                                                    return
                                            # Get first available
                                            for url_val in stream_url.values():
                                                if url_val:
                                                    captured_urls.append(url_val)
                                                    return
                                        elif isinstance(stream_url, str) and stream_url:
                                            captured_urls.append(stream_url)
                                    
                                    # Fallback fields
                                    for field in ['dlink', 'download_url', 'stream_url', 'video_url']:
                                        if field in file_data and file_data[field]:
                                            captured_urls.append(file_data[field])
                                            break
                            except:
                                pass
                    
                    # Also capture any m3u8 URLs directly
                    if '.m3u8' in url:
                        log.info(f"Captured m3u8 URL from network: {url}")
                        captured_urls.append(url)
                except:
                    pass
            
            # Listen to responses
            page.on('response', handle_response)
            
            log.info(f"Loading iTeraPlay page: {api_url}")
            
            try:
                # Navigate to the page
                await page.goto(api_url, wait_until='domcontentloaded', timeout=timeout * 1000)
                
                # Wait a bit for API calls to complete
                await page.wait_for_timeout(5000)
                
                # Try to extract from the page content as fallback
                if not captured_urls:
                    log.info("No m3u8 captured from network, trying DOM extraction...")
                    
                    # Execute JavaScript to get videoUrl variable
                    try:
                        video_url_from_js = await page.evaluate("""
                            () => {
                                if (typeof videoUrl !== 'undefined' && videoUrl) {
                                    return videoUrl;
                                }
                                if (typeof videoQualities !== 'undefined' && videoQualities) {
                                    const qualities = ['1080p', '720p', '480p', '360p'];
                                    for (const q of qualities) {
                                        if (videoQualities[q]) return videoQualities[q];
                                    }
                                    return Object.values(videoQualities)[0];
                                }
                                return null;
                            }
                        """)
                        
                        if video_url_from_js:
                            log.info(f"Extracted videoUrl from JavaScript: {video_url_from_js[:100]}")
                            captured_urls.append(video_url_from_js)
                    except Exception as e:
                        log.debug(f"Could not extract from JS variables: {e}")
                    
                    # Also try to get video title
                    if not video_title:
                        try:
                            video_title = await page.evaluate("() => typeof videoTitle !== 'undefined' ? videoTitle : null")
                        except:
                            pass
                
            except PlaywrightTimeout:
                log.warning("Page load timeout, but we may have captured network data")
            
            await browser.close()
            
            # Get the best m3u8 URL
            if captured_urls:
                # Remove duplicates
                captured_urls = list(set(captured_urls))
                
                # Prefer higher quality
                quality_order = ['1080', '720', '480', '360']
                for quality in quality_order:
                    for url in captured_urls:
                        if quality in url.lower():
                            m3u8_url = url
                            break
                    if m3u8_url:
                        break
                
                # If no quality preference matched, use first one
                if not m3u8_url:
                    m3u8_url = captured_urls[0]
                
                log.info(f"Selected m3u8 URL: {m3u8_url[:100]}...")
                return m3u8_url, video_title
            else:
                log.error("No m3u8 URL found in network or DOM")
                return None, None
                
    except Exception as e:
        log.error(f"Playwright extraction failed: {e}")
        return None, None


async def fetch_video_with_playwright(terabox_url: str):
    """
    Main entry point for Playwright-based extraction.
    Returns (m3u8_url, video_title) tuple.
    """
    return await extract_m3u8_with_playwright(terabox_url)


def fetch_video_from_iteraplay(terabox_url: str, timeout=20):
    """
    Synchronous wrapper for the async Playwright extraction.
    Use this from synchronous code.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(extract_m3u8_with_playwright(terabox_url, timeout))
