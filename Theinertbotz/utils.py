import re
from pyrogram.types import Message
from typing import List
from config import logger

_DOMAINS = [
    r"1024terabox\.com",
    r"terabox\.com",
    r"terasharelink\.com",
    r"terasharefile\.com",
    r"tera"
]

URL_RE = re.compile(r"(https?://[^\s)>\]]+)", re.IGNORECASE)

def _is_terabox_url(url: str) -> bool:
    for d in _DOMAINS:
        if re.search(d, url, re.IGNORECASE):
            return True
    return False

def extract_links_from_text(text: str):
    found = URL_RE.findall(text or "")
    return [u.rstrip(".,)\"'") for u in found if _is_terabox_url(u)]

def extract_links_from_message(msg: Message) -> List[str]:
    links = []

    # entities (text_link/url)
    if getattr(msg, "entities", None):
        try:
            for e in msg.entities:
                if e.type == "text_link" and getattr(e, "url", None):
                    if _is_terabox_url(e.url):
                        links.append(e.url)
                elif e.type == "url":
                    text = msg.text or msg.caption or ""
                    u = text[e.offset:e.offset+e.length]
                    if _is_terabox_url(u):
                        links.append(u)
        except Exception:
            pass

    # fallback regex on text & caption
    if getattr(msg, "text", None):
        links += extract_links_from_text(msg.text)
    if getattr(msg, "caption", None):
        links += extract_links_from_text(msg.caption)

    # dedupe preserving order
    seen = set()
    out = []
    for u in links:
        if u not in seen:
            seen.add(u)
            out.append(u)
    logger.debug(f"Extracted links: {out}")
    return out
