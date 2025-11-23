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
from plugins.buttons import LIMIT_REACHED_BUTTONS

log = logging.getLogger("TeraBoxBot")

# Global semaphore to limit concurrent downloads (max 2 simultaneous)
download_semaphore = asyncio.Semaphore(2)

TERABOX_RE = re.compile(r"(https?://(?:www\.)?[^\s]*(?:terabox|1024terabox|terasharefile|tera\.co|terabox\.co|mirrobox|nephobox|freeterabox|4funbox|terabox\.app|terabox\.fun|momerybox|teraboxapp|tibibox)[^\s]*)", re.IGNORECASE)

def extract_links(text: str):
    if not text:
        return []
    return TERABOX_RE.findall(text)

def register_handlers(app):
    @app.on_message(filters.private & ~filters.command("start") & ~filters.command("help") & ~filters.command("rename") & ~filters.command("set_rename") & ~filters.command("premium") & ~filters.command("admin") & ~filters.command("addpremium") & ~filters.command("removepremium") & ~filters.command("checkuser") & ~filters.command("set_upload_channel") & ~filters.command("remove_upload_channel") & ~filters.command("auto_delete") & ~filters.command("set_auto_delete") & ~filters.command("remove_auto_delete"))
    async def main_handler(client, message: Message):
        try:
            from plugins.premium import PremiumManager
            text = message.text or message.caption or ""
            links = extract_links(text)
            if not links:
                await message.reply(Script.NO_LINK, parse_mode=enums.ParseMode.HTML)
                return

            user_id = message.from_user.id

            # Show processing status
            status_msg = await message.reply(f"⏳ Processing {len(links)} link{'s' if len(links) > 1 else ''}...")
            
            # Process links with concurrency limit (max 2 simultaneous)
            for idx, link in enumerate(links):
                # Check download limit for each link
                can_download, limit_msg = PremiumManager.check_download_limit(user_id)
                if not can_download:
                    try:
                        await message.reply(f"⏹️ <b>Link {idx+1} skipped:</b> {limit_msg}", reply_markup=LIMIT_REACHED_BUTTONS, parse_mode=enums.ParseMode.HTML)
                    except:
                        pass
                    continue
                
                # Use semaphore to limit concurrent downloads
                async with download_semaphore:
                    log.info(f"Processing link {idx+1}/{len(links)}: {link} from user {user_id}")
                    try:
                        await process_video(client, message, link.strip())
                        db.increment_daily_downloads(user_id)
                        # Small delay between links to avoid overwhelming the system
                        await asyncio.sleep(1)
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
