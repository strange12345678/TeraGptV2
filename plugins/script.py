# plugins/script.py
# Centralized text and scripts

class Script:
    # Welcome and Help
    START = "👋 <b>Welcome to TeraBox Bot!</b>\n\nSend me any TeraBox link and I'll download and upload it for you.\n\n📱 <b>Features:</b>\n• Direct download from TeraBox\n• Auto-rename files\n• Premium mode with unlimited downloads\n• File backup to storage"
    
    HELP = "<b>📚 Available Commands:</b>\n\n/start - Welcome\n/help - This message\n/premium - Premium info\n/rename - Auto-rename settings\n/admin - Admin panel\n/auto_delete - Toggle message auto-delete"
    
    NO_LINK = "❌ <b>No TeraBox link found!</b>\n\nPlease send a valid TeraBox link."
    
    UNEXPECTED_ERROR = "❌ <b>Unexpected Error:</b>\n\nPlease try again later or contact support."
    
    # Auto-delete messages
    AUTO_DELETE_ENABLED = "✅ <b>ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴇɴᴀʙʟᴇᴅ</b>\n\n⏱️ Video messages will auto-delete in <b>5 seconds</b> to help prevent copyright issues.\n\n📌 <i>Premium & Free users: Both will have auto-delete enabled</i>"
    
    AUTO_DELETE_DISABLED = "⏹️ <b>ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴅɪsᴀʙʟᴇᴅ</b>\n\n⏱️ Video messages will <b>NOT</b> auto-delete.\n\n⚠️ <i>Remember to manage your storage manually</i>"
    
    AUTO_DELETE_NOTIFY = "⏰ <b>ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ɪɴ 5 sᴇᴄᴏɴᴅs</b> 🗑️\n\n💡 <i>This helps prevent copyright issues on Telegram</i>"

