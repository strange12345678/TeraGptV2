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

# Global lock to ensure only ONE message batch processes at a time
handler_lock = asyncio.Lock()

TERABOX_RE = re.compile(r"(https?://(?:www\.)?[^\s]*(?:terabox|1024terabox|terasharefile|tera\.co|terabox\.co|mirrobox|nephobox|freeterabox|4funbox|terabox\.app|terabox\.fun|momerybox|teraboxapp|tibibox)[^\s]*)", re.IGNORECASE)

def extract_links(text: str):
    if not text:
        return []
    return TERABOX_RE.findall(text)


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

            # Check download limit
            can_download, limit_msg = PremiumManager.check_download_limit(user_id)
            if not can_download:
                try:
                    await message.reply(f"⏹️ <b>Download limit reached:</b> {limit_msg}", reply_markup=LIMIT_REACHED_BUTTONS, parse_mode=enums.ParseMode.HTML)
                except:
                    pass
                return
            
            # Acquire global lock to process one batch at a time
            async with handler_lock:
                # Create status message for THIS message
                status_msg = None
                try:
                    status_msg = await message.reply(f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Processing {len(links)} link(s)...</i>", parse_mode=enums.ParseMode.HTML)
                except:
                    pass
                
                # Process links one by one sequentially
                for idx, link in enumerate(links, 1):
                    try:
                        log.info(f"[DOWNLOAD] ★ PROCESSING Link #{idx}/{len(links)}: {link}")
                        
                        # Update status
                        if status_msg:
                            try:
                                remaining = len(links) - idx
                                status_text = f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Link #{idx}/{len(links)}"
                                if remaining > 0:
                                    status_text += f" | Remaining: {remaining}"
                                status_text += "</i>"
                                await status_msg.edit(status_text, parse_mode=enums.ParseMode.HTML)
                            except:
                                pass
                        
                        # Process the link
                        current_api = db.get_current_api()
                        if current_api == "secondary":
                            log.info(f"[DOWNLOAD] Using SECONDARY API for link #{idx}")
                            await process_video_secondary(client, message, link.strip(), status_msg=status_msg)
                        else:
                            log.info(f"[DOWNLOAD] Using PRIMARY API for link #{idx}")
                            await process_video(client, message, link.strip(), status_msg=status_msg)
                        
                        log.info(f"[DOWNLOAD] ✅ COMPLETED Link #{idx}")
                        
                    except Exception as e:
                        log.exception(f"[DOWNLOAD] ❌ ERROR Link #{idx}: {e}")
                        try:
                            if status_msg:
                                await status_msg.edit(f"⚠️ <b>Failed link #{idx}</b>", parse_mode=enums.ParseMode.HTML)
                        except:
                            pass
                    
                    # Wait before next link (1 second delay)
                    if idx < len(links):
                        log.info("[DOWNLOAD] Waiting 1s before next link...")
                        await asyncio.sleep(1)
                
        except Exception as e:
            log.exception("main_handler error")
            try:
                await message.reply(Script.UNEXPECTED_ERROR, parse_mode=enums.ParseMode.HTML)
            except:
                pass
