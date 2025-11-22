import math
import time
from pyrogram import Client

# Cache bot username so we don't call get_me() repeatedly
BOT_USERNAME = None


async def get_bot_username(client: Client):
    """Fetch and cache bot username."""
    global BOT_USERNAME
    if BOT_USERNAME is None:
        me = await client.get_me()
        BOT_USERNAME = me.username
    return BOT_USERNAME


def human_readable_size(size):
    """Convert bytes → KB/MB/GB readable."""
    if size is None:
        return "0B"
    power = 1024
    n = 0
    Dic_powerN = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}

    while size > power and n < 4:
        size /= power
        n += 1
    return f"{size:.2f} {Dic_powerN[n]}"


def human_eta(secs):
    """Convert seconds → mm:ss format."""
    secs = int(secs)
    if secs <= 0:
        return "00:00"
    m, s = divmod(secs, 60)
    return f"{m:02d}:{s:02d}"


def make_progress_bar(percentage):
    """Generate 10-block bar using ▰ and ▱."""
    total_blocks = 10
    filled_blocks = int((percentage / 100) * total_blocks)
    empty_blocks = total_blocks - filled_blocks

    return "▰" * filled_blocks + "▱" * empty_blocks


def should_update(prev, current):
    """Avoid spam: update only if percentage changed by ≥1%."""
    if prev is None:
        return True
    return abs(current - prev) >= 1


# =========================================================
#  DOWNLOAD PROGRESS FORMATTER
# =========================================================

async def format_download_progress(client, downloaded, total, speed, eta, last_percentage=None):
    percentage = (downloaded / total) * 100 if total else 0
    percentage = round(percentage, 2)

    if not should_update(last_percentage, percentage):
        return None, last_percentage  # No update needed

    progress_bar = make_progress_bar(percentage)
    bot_username = await get_bot_username(client)

    text = (
        f"<b>\n"
        f" ╭──⌯════🅓︎🅞︎🅦︎🅝︎🅛︎🅞︎🅐︎🅓︎🅘︎🅝︎🅖︎⬇️⬇️═════⌯──╮\n"
        f"├⚡ {progress_bar} |﹝{percentage}%﹞\n"
        f"├🚀 Speed » {human_readable_size(speed)}/s\n"
        f"├📟 Processed » {human_readable_size(downloaded)}\n"
        f"├🧲 Size - ETA » {human_readable_size(total)} - {human_eta(eta)}\n"
        f"├🤖 𝔹ʏ » @{bot_username}\n"
        f"╰─═══ ✪ @theinertbotz ✪ ═══─╯\n"
        f"</b>"
    )

    return text, percentage


# =========================================================
#  UPLOAD PROGRESS FORMATTER
# =========================================================

async def format_upload_progress(client, uploaded, total, speed, eta, last_percentage=None):
    percentage = (uploaded / total) * 100 if total else 0
    percentage = round(percentage, 2)

    if not should_update(last_percentage, percentage):
        return None, last_percentage  # No update needed

    progress_bar = make_progress_bar(percentage)
    bot_username = await get_bot_username(client)

    text = (
        f"<b>\n"
        f" ╭──⌯════🆄︎🅟︎🅛︎🅞︎🅐︎🅓︎🅘︎🅝︎🅖︎⬆️⬆️═════⌯──╮\n"
        f"├⚡ {progress_bar} |﹝{percentage}%﹞\n"
        f"├🚀 Speed » {human_readable_size(speed)}/s\n"
        f"├📟 Processed » {human_readable_size(uploaded)}\n"
        f"├🧲 Size - ETA » {human_readable_size(total)} - {human_eta(eta)}\n"
        f"├🤖 𝔹ʏ » @{bot_username}\n"
        f"╰─═══ ✪ @theinertbotz ✪ ═══─╯\n"
        f"</b>"
    )

    return text, percentage
