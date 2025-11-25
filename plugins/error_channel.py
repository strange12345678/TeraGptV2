import logging
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

async def log_error(client, error_text: str) -> None:
    log.error(f"ERROR: {error_text}")
    channel = Config.ERROR_CHANNEL
    
    # Validate channel configuration
    if not channel:
        log.debug(f"ERROR_CHANNEL not configured (None), skipping error log")
        return
    if channel == 0:
        log.debug(f"ERROR_CHANNEL not configured (0), skipping error log")
        return
    
    # Validate channel ID format
    if not validate_channel_id(channel):
        log.error(f"ERROR_CHANNEL {channel} is invalid format. Must be a negative integer like -1001234567890")
        return
    
    try:
        msg = f"<b>❌ Error Report</b>\n<pre>{error_text}</pre>"
        log.debug(f"Attempting to send error to channel {channel}")
        
        # Try to get chat info first for better error diagnosis
        try:
            chat_info = await client.get_chat(channel)
            log.debug(f"Channel found: {chat_info.title if hasattr(chat_info, 'title') else 'Unknown'}")
        except Exception as chat_err:
            log.warning(f"Could not get chat info for {channel}: {chat_err}")
        
        await client.send_message(chat_id=channel, text=msg, parse_mode=enums.ParseMode.HTML)
        log.debug(f"Error sent to channel {channel}")
    except Exception as e:
        error_str = str(e)
        log.error(f"ERROR_CHANNEL send error: {type(e).__name__}: {error_str}")
        log.error(f"Channel ID being used: {channel} (type: {type(channel)})")
        
        if "Peer id invalid" in error_str or "chat not found" in error_str.lower():
            log.error(f"❌ TROUBLESHOOTING for ERROR_CHANNEL {channel}:")
            log.error(f"   1. Verify bot is added to the channel/group")
            log.error(f"   2. Make bot an ADMINISTRATOR with 'Post Messages' permission")
            log.error(f"   3. If private channel, forward a message from the channel to @RawDataBot to verify the ID")
            log.error(f"   4. Try sending /start or any message to the bot from the channel")
        elif "USER_RESTRICTED" in error_str or "CHAT_SEND_PLAIN_FORBIDDEN" in error_str:
            log.error(f"Failed to send to ERROR_CHANNEL {channel}: Bot doesn't have permission to post. Check bot admin rights.")
        elif "auth" in error_str.lower() or "unauthorized" in error_str.lower():
            log.error(f"Failed to send to ERROR_CHANNEL {channel}: Authentication issue - bot may not be properly authenticated.")
        else:
            log.error(f"Failed to send to ERROR_CHANNEL {channel}: {type(e).__name__} - {error_str}")
