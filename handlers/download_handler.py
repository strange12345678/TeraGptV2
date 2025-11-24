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

async def _process_single_link(client, message, link, user_id, status_msg=None, link_num=1, total_links=1):
    """Process a single link"""
    try:
        log.info(f"[QUEUE] Processing link {link_num}/{total_links}: {link} from user {user_id}")
        
        # Update status message if we have multiple links
        if total_links > 1 and status_msg:
            try:
                await status_msg.edit(f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Link {link_num}/{total_links}</i>", parse_mode=enums.ParseMode.HTML)
            except:
                pass
        
        # Check which API to use
        current_api = db.get_current_api()
        if current_api == "secondary":
            await process_video_secondary(client, message, link.strip(), status_msg=status_msg)
        else:
            await process_video(client, message, link.strip(), status_msg=status_msg)
            
    except Exception as e:
        log.exception(f"Error processing link {link_num}/{total_links}: {link}")
        try:
            if total_links > 1 and status_msg:
                await status_msg.edit(f"⚠️ <b>Failed link {link_num}/{total_links}:</b> {str(e)[:80]}", parse_mode=enums.ParseMode.HTML)
            else:
                await message.reply(f"⚠️ <b>Failed to process</b>\n\n{str(e)[:100]}", parse_mode=enums.ParseMode.HTML)
        except:
            pass

async def _process_bulk_links_background(client, message, links, user_id, status_msg=None):
    """Background task to process multiple links sequentially"""
    try:
        # Use semaphore to ensure one link at a time
        async with download_semaphore:
            total_links = len(links)
            completed = 0
            failed = 0
            
            for idx, link in enumerate(links, 1):
                try:
                    await _process_single_link(client, message, link, user_id, status_msg=status_msg, link_num=idx, total_links=total_links)
                    completed += 1
                except Exception as e:
                    log.exception(f"Link {idx} failed: {e}")
                    failed += 1
            
            # Final summary
            if total_links > 1 and status_msg:
                try:
                    summary = f"✅ <b>Completed!</b>\n✓ {completed} links processed"
                    if failed > 0:
                        summary += f"\n✗ {failed} links failed"
                    await status_msg.edit(summary, parse_mode=enums.ParseMode.HTML)
                except:
                    pass
                    
    except Exception as e:
        log.exception(f"Bulk processing error: {e}")

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

            # Check download limit (will be checked again for each link)
            can_download, limit_msg = PremiumManager.check_download_limit(user_id)
            if not can_download:
                try:
                    await message.reply(f"⏹️ <b>Download limit reached:</b> {limit_msg}", reply_markup=LIMIT_REACHED_BUTTONS, parse_mode=enums.ParseMode.HTML)
                except:
                    pass
                return
            
            # Send immediate feedback to user FIRST
            status_msg = None
            try:
                if len(links) == 1:
                    status_msg = await message.reply("⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>", parse_mode=enums.ParseMode.HTML)
                else:
                    status_msg = await message.reply(f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Processing {len(links)} links sequentially...</i>", parse_mode=enums.ParseMode.HTML)
            except:
                pass
            
            # Start processing in background (return immediately for instant response)
            # For bulk links, process sequentially; for single link, use same path
            if len(links) == 1:
                asyncio.create_task(_process_single_link(client, message, links[0], user_id, status_msg=status_msg))
            else:
                asyncio.create_task(_process_bulk_links_background(client, message, links, user_id, status_msg=status_msg))
                
        except Exception as e:
            log.exception("main_handler error")
            try:
                await message.reply(Script.UNEXPECTED_ERROR, parse_mode=enums.ParseMode.HTML)
            except:
                pass
