# handlers/download_handler.py
import re
import asyncio
import logging
from pyrogram import filters, enums
from pyrogram.types import Message
from config import Config
from Theinertbotz.engine import process_video
from Theinertbotz.secondary_engine import process_video_secondary
from Theinertbotz.database import db
from script import Script
from plugins.buttons import LIMIT_REACHED_BUTTONS

log = logging.getLogger("TeraBoxBot")

# Global semaphore to limit concurrent downloads (max 1 simultaneous - process one link at a time)
download_semaphore = asyncio.Semaphore(1)

TERABOX_RE = re.compile(r"(https?://(?:www\.)?[^\s]*(?:terabox|1024terabox|terasharefile|tera\.co|terabox\.co|mirrobox|nephobox|freeterabox|4funbox|terabox\.app|terabox\.fun|momerybox|teraboxapp|tibibox)[^\s]*)", re.IGNORECASE)

def extract_links(text: str):
    if not text:
        return []
    return TERABOX_RE.findall(text)

async def _process_link_background(client, message, link, user_id):
    """Background task to process download without blocking"""
    try:
        # Use semaphore to limit concurrent downloads
        async with download_semaphore:
            log.info(f"Processing link: {link} from user {user_id}")
            try:
                # Check which API to use
                current_api = db.get_current_api()
                if current_api == "secondary":
                    await process_video_secondary(client, message, link.strip())
                else:
                    await process_video(client, message, link.strip())
            except Exception as e:
                log.exception(f"Error processing link: {link}")
                try:
                    await message.reply(f"⚠️ <b>Failed to process</b>\n\n{str(e)[:100]}", parse_mode=enums.ParseMode.HTML)
                except:
                    pass
    except Exception as e:
        log.exception(f"Background task error: {e}")

def register_handlers(app):
    @app.on_message(filters.private & ~filters.command("start") & ~filters.command("help") & ~filters.command("rename") & ~filters.command("set_rename") & ~filters.command("premium") & ~filters.command("admin") & ~filters.command("addpremium") & ~filters.command("removepremium") & ~filters.command("checkuser") & ~filters.command("set_upload_channel") & ~filters.command("remove_upload_channel") & ~filters.command("toggle_autodelete") & ~filters.command("auto_delete") & ~filters.command("set_auto_delete") & ~filters.command("remove_auto_delete"))
    async def main_handler(client, message: Message):
        try:
            from plugins.premium import PremiumManager
            text = message.text or message.caption or ""
            links = extract_links(text)
            if not links:
                await message.reply(Script.NO_LINK, parse_mode=enums.ParseMode.HTML)
                return

            user_id = message.from_user.id

            # Only process the FIRST link, ignore bulk URLs
            link = links[0]
            
            # Check download limit
            can_download, limit_msg = PremiumManager.check_download_limit(user_id)
            if not can_download:
                try:
                    await message.reply(f"⏹️ <b>Download limit reached:</b> {limit_msg}", reply_markup=LIMIT_REACHED_BUTTONS, parse_mode=enums.ParseMode.HTML)
                except:
                    pass
                return
            
            # Start download in background (return immediately for instant response)
            asyncio.create_task(_process_link_background(client, message, link, user_id))
                
        except Exception as e:
            log.exception("main_handler error")
            try:
                await message.reply(Script.UNEXPECTED_ERROR, parse_mode=enums.ParseMode.HTML)
            except:
                pass
