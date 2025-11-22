# Theinertbotz/processing.py
import time
import math
import asyncio
import logging
from typing import Optional, Callable

log = logging.getLogger("TeraBoxBot")

# ---------- Helpers ----------
def human_size(num: int) -> str:
    """Return human-readable size (B, KB, MB, GB)."""
    if num is None:
        return "0 B"
    try:
        num = float(num)
    except Exception:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024.0 or unit == "TB":
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} PB"

def format_eta(seconds: float) -> str:
    if seconds is None or seconds == float("inf"):
        return "--:--"
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:d}h {m:02d}m"
    if m:
        return f"{m:02d}m {s:02d}s"
    return f"{s:02d}s"

def build_bar(perc: float, blocks: int, kind: str = "download") -> str:
    """
    Return a progress bar string.
    kind: "download" or "upload" -> different glyphs per request.
    """
    filled = int(round((perc / 100.0) * blocks))
    filled = max(0, min(blocks, filled))
    empty = blocks - filled

    if kind == "download":
        fill_char = "▰"
        empty_char = "▱"
    else:  # upload
        fill_char = "■"
        empty_char = "□"

    return fill_char * filled + empty_char * empty

# ---------- Progress Manager ----------
class ProgressManager:
    """
    Manage and render progress for download/upload tasks.

    Args:
        edit_coro: async function to call to edit the status message.
                   Signature: await edit_coro(text, parse_mode="HTML")
        bot_username: string like "@inert_test_bot" to display in UI
        kind: "download" or "upload"
    """

    def __init__(
        self,
        edit_coro: Callable[[str], asyncio.Future],
        bot_username: str = "@bot",
        kind: str = "download",
        *,
        blocks: int = 10,
    ):
        self.edit_coro = edit_coro
        self.bot_username = bot_username or "@bot"
        self.kind = kind if kind in ("download", "upload") else "download"
        self.blocks = min(10, max(3, int(blocks)))  # clamp, default 10
        # state
        self._last_update_time = 0.0
        self._last_perc = -1.0
        self._created_at = time.time()
        # throttle params
        self._min_interval = 1.0   # seconds between updates (unless perc changed >= delta_perc)
        self._delta_perc = 1.0     # percent change required to force update
        self._lock = asyncio.Lock()

    async def update(self, processed: int, total: Optional[int], speed: Optional[float]):
        """
        Update progress. Call frequently from download/upload loops.
        - processed: bytes processed so far
        - total: total bytes (0 or None if unknown)
        - speed: bytes/sec (may be None)
        """
        async with self._lock:
            now = time.time()
            total = int(total or 0)
            processed = int(processed or 0)

            # compute percent
            if total > 0:
                perc = (processed / total) * 100.0
                perc = max(0.0, min(100.0, perc))
            else:
                # unknown total -> use heuristic percent (cap at 99.9)
                perc = 0.0 if processed == 0 else 99.9

            # throttle: update only when perc changed sufficiently or interval passed
            perc_changed = abs(perc - self._last_perc) >= self._delta_perc
            time_elapsed = now - self._last_update_time
            if not perc_changed and time_elapsed < self._min_interval:
                return  # skip to avoid spam

            self._last_update_time = now
            self._last_perc = perc

            # speed -> human
            try:
                sp = human_size(speed) + "/s" if speed and not math.isnan(speed) else "--"
            except Exception:
                sp = "--"

            # ETA
            eta = None
            if speed and speed > 0 and total > 0:
                rem = max(0, total - processed)
                eta = rem / speed
            eta_str = format_eta(eta) if eta is not None else "--:--"

            # processed/total human
            processed_h = human_size(processed)
            total_h = human_size(total) if total > 0 else "Unknown"

            # build bar
            bar = build_bar(perc, self.blocks, kind=self.kind)

            # percent text
            perc_text = f"{perc:3.1f}%"

            # choose heading label
            heading = "Uᴘʟᴏᴀᴅɪɴɢ" if self.kind == "upload" else "Dᴏᴡɴʟᴏᴀᴅɪɴɢ"

            # Compose HTML (kept compact — safe for telegram edit)
            text = (
                f"<b>\n"
                f" ╭──⌯════{heading}═════⌯──╮\n"
                f"├⚡ {bar} |﹝{perc_text}﹞\n"
                f"├🚀 Speed » {sp}\n"
                f"├📟 Processed » {processed_h}\n"
                f"├🧲 Size - ETA » {total_h} - {eta_str}\n"
                f"├🤖 𝔹ʏ » {self.bot_username}\n"
                f"╰─═══ ✪ @theinertbotz ✪ ═══─╯\n"
                f"</b>"
            )

            # call edit coroutine (guard exceptions)
            try:
                await self._safe_edit(text)
            except Exception:
                log.exception("ProgressManager: edit failed")

    async def _safe_edit(self, text: str):
        """
        Wrap edit_coro in try/except. Keep a fallback and small delay to avoid rate limits.
        """
        try:
            coro = self.edit_coro(text, parse_mode="html")
            if asyncio.iscoroutine(coro):
                await coro
            else:
                # edit_coro returned non-coroutine (unlikely) -> ignore
                return
        except Exception as e:
            log.debug("ProgressManager edit error: %s", e)

# Expose small API
__all__ = ["ProgressManager", "human_size", "format_eta", "build_bar"]
