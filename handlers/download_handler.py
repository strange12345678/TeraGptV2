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
        self.queue = deque()  # Queue of {client, message, link, user_id, status_msg}
        self.processing = False
        self.global_counter = 0  # Global counter for all links ever added
        self.current_status_msg = None
        self.add_lock = asyncio.Lock()  # CRITICAL: Prevent concurrent queue modifications
    
    async def add(self, client, message, links, user_id, status_msg):
        """Add a batch of links to the queue (thread-safe with lock)"""
        async with self.add_lock:  # CRITICAL: Ensure only one handler adds to queue at a time
            total = len(links)
            
            # Each link gets a unique global number
            for idx, link in enumerate(links, 1):
                self.global_counter += 1
                self.queue.append({
                    'client': client,
                    'message': message,
                    'link': link,
                    'user_id': user_id,
                    'status_msg': status_msg,
                    'global_num': self.global_counter
                })
            
            log.info(f"[QUEUE] Added {total} link(s). Global: #{self.global_counter}. Pending: {len(self.queue)}")
            
            # Start worker if not already running
            if not self.processing:
                asyncio.create_task(self._worker())
    
    async def _worker(self):
        """Global worker that processes one link at a time with retry logic"""
        if self.processing:
            return
        
        self.processing = True
        log.info("[QUEUE] Worker STARTED - Processing links sequentially with auto-retry")
        
        try:
            while self.queue:
                # Get next link from queue
                item = self.queue.popleft()
                remaining = len(self.queue)
                
                max_retries = 2
                retry_count = 0
                
                while retry_count <= max_retries:
                    try:
                        log.info(f"[QUEUE] ★ PROCESSING Link #{item['global_num']}: {item['link']} (Remaining: {remaining}, Attempt: {retry_count + 1}/{max_retries + 1})")
                        
                        # Update status with queue position and retry attempt
                        if item['status_msg']:
                            try:
                                status_text = f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Link #{item['global_num']}"
                                if remaining > 0:
                                    status_text += f"\nQueue: {remaining} pending"
                                if retry_count > 0:
                                    status_text += f"\nAttempt: {retry_count + 1}/{max_retries + 1}"
                                status_text += "</i>"
                                await item['status_msg'].edit(status_text, parse_mode=enums.ParseMode.HTML)
                            except:
                                pass
                        
                        # Process the link - ATOMIC: No concurrent downloads
                        current_api = db.get_current_api()
                        if current_api == "secondary":
                            log.info(f"[QUEUE] Using SECONDARY API for link #{item['global_num']} (attempt {retry_count + 1})")
                            await process_video_secondary(item['client'], item['message'], item['link'].strip(), status_msg=item['status_msg'])
                        else:
                            log.info(f"[QUEUE] Using PRIMARY API for link #{item['global_num']} (attempt {retry_count + 1})")
                            await process_video(item['client'], item['message'], item['link'].strip(), status_msg=item['status_msg'])
                        
                        log.info(f"[QUEUE] ✅ COMPLETED Link #{item['global_num']} on attempt {retry_count + 1}")
                        break  # Success! Move to next link
                        
                    except Exception as e:
                        retry_count += 1
                        log.warning(f"[QUEUE] ⚠️ Attempt {retry_count}/{max_retries + 1} FAILED for Link #{item['global_num']}: {str(e)[:100]}")
                        
                        if retry_count > max_retries:
                            # All retries exhausted
                            log.error(f"[QUEUE] ❌ FAILED Link #{item['global_num']} after {max_retries + 1} attempts")
                            try:
                                if item['status_msg']:
                                    await item['status_msg'].edit(f"⚠️ <b>Failed link #{item['global_num']}</b>\n<i>Tried {max_retries + 1} times</i>", parse_mode=enums.ParseMode.HTML)
                            except:
                                pass
                            break  # Give up on this link
                        else:
                            # Retry with exponential backoff: 2s, 4s
                            backoff = 2 ** retry_count
                            log.info(f"[QUEUE] Retrying in {backoff}s...")
                            await asyncio.sleep(backoff)
                
                # Add 2-second delay between queue items (rate limiting)
                if self.queue:
                    log.info("[QUEUE] Waiting 2s before next item (rate limiting)...")
                    await asyncio.sleep(2)
            
            log.info("[QUEUE] Worker FINISHED - queue empty")
        
        finally:
            self.processing = False
            log.info("[QUEUE] Worker cleanup - processing flag reset")

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
                status_msg = await message.reply(f"⏳ <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...</b>\n<i>Queued {len(links)} link(s) for sequential processing...</i>", parse_mode=enums.ParseMode.HTML)
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
