# handlers/download_handler.py
import re
import asyncio
import logging
from collections import deque
from pyrogram import filters, enums
from pyrogram.types import Message
from config import Config
from Theinertbotz.engine import process_video
from Theinertbotz.secondary_engine import process_video_secondary
from Theinertbotz.database import db
from script import Script
from plugins.buttons import LIMIT_REACHED_BUTTONS

log = logging.getLogger("TeraBoxBot")

# Global queue for sequential link processing - ensures only ONE link processes globally
class LinkQueue:
    def __init__(self):
        self.queue = deque()  # Queue of (client, message, link, user_id, status_msg, link_num, total_links)
        self.processing = False
        self.current_status_msg = None
    
    async def add(self, client, message, links, user_id, status_msg):
        """Add a batch of links to the queue"""
        total = len(links)
        for idx, link in enumerate(links, 1):
            self.queue.append({
                'client': client,
                'message': message,
                'link': link,
                'user_id': user_id,
                'status_msg': status_msg,
                'link_num': idx,
                'total_links': total
            })
        log.info(f"[QUEUE] Added {total} link(s). Queue size: {len(self.queue)}")
        
        # Start worker if not already running
        if not self.processing:
            asyncio.create_task(self._worker())
    
    async def _worker(self):
        """Global worker that processes one link at a time"""
        if self.processing:
            return
        
        self.processing = True
        log.info("[QUEUE] Worker started")
        
        try:
            while self.queue:
                # Get next link from queue
                item = self.queue.popleft()
                remaining = len(self.queue)
                
                try:
                    log.info(f"[QUEUE] Processing {item['link_num']}/{item['total_links']}: {item['link']} (Queue remaining: {remaining})")
                    
                    # Update status if multiple links
                    if item['total_links'] > 1 and item['status_msg']:
                        try:
                            await item['status_msg'].edit(
                                f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Link {item['link_num']}/{item['total_links']}</i>\n<i>Queue: {remaining} pending</i>",
                                parse_mode=enums.ParseMode.HTML
                            )
                        except:
                            pass
                    
                    # Process the link
                    current_api = db.get_current_api()
                    if current_api == "secondary":
                        await process_video_secondary(item['client'], item['message'], item['link'].strip(), status_msg=item['status_msg'])
                    else:
                        await process_video(item['client'], item['message'], item['link'].strip(), status_msg=item['status_msg'])
                    
                except Exception as e:
                    log.exception(f"[QUEUE] Error processing link {item['link_num']}/{item['total_links']}: {e}")
                    try:
                        if item['total_links'] > 1 and item['status_msg']:
                            await item['status_msg'].edit(f"⚠️ <b>Failed link {item['link_num']}/{item['total_links']}</b>", parse_mode=enums.ParseMode.HTML)
                    except:
                        pass
            
            log.info("[QUEUE] Worker finished - queue empty")
        
        finally:
            self.processing = False

# Global instance
link_queue = LinkQueue()

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
            
            # Send immediate feedback to user
            status_msg = None
            try:
                if len(links) == 1:
                    status_msg = await message.reply("⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>", parse_mode=enums.ParseMode.HTML)
                else:
                    status_msg = await message.reply(f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Queued {len(links)} links for sequential processing...</i>", parse_mode=enums.ParseMode.HTML)
            except:
                pass
            
            # Add to global FIFO queue (guaranteed sequential processing)
            await link_queue.add(client, message, links, user_id, status_msg)
                
        except Exception as e:
            log.exception("main_handler error")
            try:
                await message.reply(Script.UNEXPECTED_ERROR, parse_mode=enums.ParseMode.HTML)
            except:
                pass
