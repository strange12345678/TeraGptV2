import logging
from typing import Optional
from config import Config
from pyrogram import enums

log = logging.getLogger("TeraBoxBot")

def validate_channel_id(channel_id) -> bool:
    """Validate if channel ID is in correct format for Telegram API"""
    if not channel_id:
        return False
    
    # Should be a negative number (group/channel) or positive (user/bot)
    # For channels/groups: -100XXXXXXXXXX or -XXXXXXXXXX
    try:
        ch = int(channel_id)
        if ch == 0:
            return False
        # Channel/group IDs should be negative
        if ch > 0:
            log.warning(f"Channel ID {ch} is positive - should be negative for channels/groups. Attempting to use as-is.")
        return True
    except (ValueError, TypeError):
        return False

async def log_action(client, user_id: Optional[int], text: str) -> None:
    log.info(f"LOG: user={user_id} text={text}")
    channel = Config.LOG_CHANNEL
    
    # Validate channel configuration
    if not channel:
        log.debug(f"LOG_CHANNEL not configured (None), skipping log")
        return
    if channel == 0:
        log.debug(f"LOG_CHANNEL not configured (0), skipping log")
        return
    
    # Validate channel ID format
    if not validate_channel_id(channel):
        log.error(f"LOG_CHANNEL {channel} is invalid format. Must be a negative integer like -1001234567890")
        return
    
    try:
        uid_str = str(user_id) if user_id else "Unknown"
        msg = f"<b>#Action</b>\n<b>User:</b> <code>{uid_str}</code>\n{text}"
        log.debug(f"Attempting to send log to channel {channel}")
        
        # Resolve channel peer first (required for new sessions)
        try:
            chat_info = await client.get_chat(channel)
            log.debug(f"Channel resolved: {chat_info.title if hasattr(chat_info, 'title') else 'Unknown'}")
        except Exception as chat_err:
            log.error(f"Failed to resolve LOG_CHANNEL {channel}: {chat_err}")
            log.error(f"Make sure bot is added as ADMIN to the channel")
            return
        
        await client.send_message(chat_id=channel, text=msg, parse_mode=enums.ParseMode.HTML)
        log.debug(f"Log sent to channel {channel}")
    except Exception as e:
        error_str = str(e)
        log.error(f"LOG_CHANNEL send error: {type(e).__name__}: {error_str}")
        log.error(f"Channel ID being used: {channel} (type: {type(channel)})")
        
        if "Peer id invalid" in error_str or "chat not found" in error_str.lower():
            log.error(f"❌ TROUBLESHOOTING for LOG_CHANNEL {channel}:")
            log.error(f"   1. Verify bot is added to the channel/group")
            log.error(f"   2. Make bot an ADMINISTRATOR with 'Post Messages' permission")
            log.error(f"   3. If private channel, forward a message from the channel to @RawDataBot to verify the ID")
            log.error(f"   4. Try sending /start or any message to the bot from the channel")
        elif "USER_RESTRICTED" in error_str or "CHAT_SEND_PLAIN_FORBIDDEN" in error_str:
            log.error(f"Failed to send to LOG_CHANNEL {channel}: Bot doesn't have permission to post. Check bot admin rights.")
        elif "auth" in error_str.lower() or "unauthorized" in error_str.lower():
            log.error(f"Failed to send to LOG_CHANNEL {channel}: Authentication issue - bot may not be properly authenticated.")
        else:
            log.error(f"Failed to send to LOG_CHANNEL {channel}: {type(e).__name__} - {error_str}")
