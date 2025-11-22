# handlers/download_handler.py
import re
import asyncio
import logging
from pyrogram import filters, enums
from pyrogram.types import Message
from config import Config
from Theinertbotz.engine import process_video
from Theinertbotz.database import db
from script import Script

log = logging.getLogger("TeraBoxBot")

TERABOX_RE = re.compile(r"(https?://[^\s]+(?:terabox|1024terabox|terasharefile)[^\s]*)", re.IGNORECASE)

def extract_links(text: str):
    if not text:
        return []
    return TERABOX_RE.findall(text)

def register_handlers(app):
    @app.on_message(filters.private & ~filters.command("start") & ~filters.command("help") & ~filters.command("rename") & ~filters.command("set_rename") & ~filters.command("premium") & ~filters.command("admin") & ~filters.command("addpremium") & ~filters.command("removepremium") & ~filters.command("checkuser") & ~filters.command("set_upload_channel") & ~filters.command("remove_upload_channel"))
    async def main_handler(client, message: Message):
        try:
            from plugins.premium import PremiumManager
            text = message.text or message.caption or ""
            links = extract_links(text)
            if not links:
                await message.reply(Script.NO_LINK, parse_mode=enums.ParseMode.HTML)
                return

            user_id = message.from_user.id
            
            # Check download limit for each link
            can_download, status_msg = PremiumManager.check_download_limit(user_id)
            if not can_download:
                await message.reply(status_msg, parse_mode=enums.ParseMode.HTML)
                return

            # Show processing status
            status_msg = await message.reply(f"⏳ Processing {len(links)} link{'s' if len(links) > 1 else ''}...")
            
            # Process one by one
            for idx, link in enumerate(links):
                log.info(f"Processing link {idx+1}/{len(links)}: {link} from user {user_id}")
                try:
                    await process_video(client, message, link.strip())
                    db.increment_daily_downloads(user_id)
                except Exception as e:
                    log.exception(f"Error processing link: {link}")
                    try:
                        await message.reply(f"⚠️ <b>Failed to process link {idx+1}</b>\n\n{str(e)[:100]}", parse_mode=enums.ParseMode.HTML)
                    except:
                        pass
            
            # Clean up status message
            try:
                await status_msg.delete()
            except:
                pass
                
        except Exception as e:
            log.exception("main_handler error")
            try:
                await message.reply(Script.UNEXPECTED_ERROR, parse_mode=enums.ParseMode.HTML)
            except:
                pass
