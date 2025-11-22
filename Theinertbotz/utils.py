import re
from pyrogram.types import Message
from typing import List
from config import logger

# domains to accept (add more if needed)
_DOMAINS = [
    r"1024terabox\.com",
    r"terabox\.com",
    r"terasharefile\.com",
    r"terabox",
    r"teraapi"
]

URL_RE = re.compile(
    r"(https?://[^\s)>\]]+)",
    re.IGNORECASE
)

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
    # check entities for URLs (covers text with emoji attached too)
    if msg.entities:
        for e in msg.entities:
            if hasattr(e, "url") and e.url:
                if _is_terabox_url(e.url):
                    links.append(e.url)
            # entity.type may be "url" or "text_link"
            # for "url" entity, we must slice from text
            if e.type in ("url", "text_link"):
                try:
                    text = msg.text or msg.caption or ""
                    if e.type == "url":
                        offset = e.offset
                        length = e.length
                        u = text[offset:offset+length]
                        if _is_terabox_url(u):
                            links.append(u)
                except Exception:
                    continue

    # fallback: regex scan full text and caption
    if hasattr(msg, "text") and msg.text:
        links += extract_links_from_text(msg.text)
    if hasattr(msg, "caption") and msg.caption:
        links += extract_links_from_text(msg.caption)

    # forwarded messages: check fwd_from / forwarded_from
    # Pyrogram gives forwarded messages as normal message with same fields
    # so above checks already handle forwarded posts.

    # remove duplicates preserving order
    seen = set()
    out = []
    for u in links:
        if u not in seen:
            seen.add(u)
            out.append(u)
    logger.debug(f"Extracted links: {out}")
    return out
