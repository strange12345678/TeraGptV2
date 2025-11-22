import asyncio
from pyrogram.errors import FloodWait, RPCError
import os
from config import logger
from typing import Optional

async def _edit_progress(message, text):
    try:
        await message.edit(text)
    except Exception:
        pass

def _make_progress_cb(message, prefix=""):
    def cb(current, total):
        try:
            percent = (current/total)*100 if total else 0.0
            bar = "▓" * int(percent/10) + "░" * (10 - int(percent/10))
            text = f"{prefix}{percent:.1f}%\n[{bar}]"
            asyncio.get_event_loop().create_task(_edit_progress(message, text))
        except Exception:
            pass
    return cb

async def send_with_fallback(client, chat_id, path, thumb, caption, width=None, height=None, duration=None, progress_message=None):
    progress_cb = _make_progress_cb(progress_message, prefix="📤 Uploading: ")
    # decide whether to send as video (mp4) or document
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".mp4":
            return await client.send_video(
                chat_id=chat_id,
                video=path,
                thumb=thumb,
                caption=caption,
                width=width,
                height=height,
                duration=int(duration) if duration else None,
                supports_streaming=True,
                progress=progress_cb,
                progress_args=()
            )
        else:
            return await client.send_document(
                chat_id=chat_id,
                document=path,
                caption=caption,
                progress=progress_cb,
                progress_args=()
            )
    except FloodWait as fw:
        logger.info(f"FloodWait {fw.x}s; sleeping")
        await asyncio.sleep(fw.x)
        return await send_with_fallback(client, chat_id, path, thumb, caption, width, height, duration, progress_message)
    except RPCError as re:
        logger.warning(f"RPCError during upload: {re}; falling back to document")
        try:
            return await client.send_document(chat_id=chat_id, document=path, caption=caption, progress=progress_cb, progress_args=())
        except Exception:
            raise
    except Exception:
        # fallback to document
        try:
            return await client.send_document(chat_id=chat_id, document=path, caption=caption, progress=progress_cb, progress_args=())
        except Exception:
            raise
