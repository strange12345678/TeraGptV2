import asyncio
import os
from pyrogram.errors import FloodWait, RPCError
from config import logger
from typing import Optional

async def _edit_progress(message, text):
    try:
        await message.edit(text)
    except Exception:
        pass

def _make_progress_cb(loop, message, prefix=""):
    def cb(current, total):
        try:
            percent = (current/total)*100 if total else 0.0
            bar = "▓" * int(percent/10) + "░" * (10 - int(percent/10))
            text = f"{prefix}{percent:.1f}%\n[{bar}]"
            loop.call_soon_threadsafe(asyncio.create_task, message.edit(text))
        except Exception:
            pass
    return cb

async def send_with_fallback(client, chat_id, path, thumb, caption, width=None, height=None, duration=None, status_msg=None):
    loop = asyncio.get_running_loop()
    progress_cb = _make_progress_cb(loop, status_msg, prefix="📤 Uploading: ")
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
        return await send_with_fallback(client, chat_id, path, thumb, caption, width, height, duration, status_msg)
    except RPCError as re:
        logger.warning(f"RPCError during upload: {re}; falling back to document")
        return await client.send_document(chat_id=chat_id, document=path, caption=caption, progress=progress_cb, progress_args=())
    except Exception:
        # fallback to document
        return await client.send_document(chat_id=chat_id, document=path, caption=caption, progress=progress_cb, progress_args=())
