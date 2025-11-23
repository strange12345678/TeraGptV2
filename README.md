# 🎬 TeraBox Telegram Bot

A powerful and feature-rich Telegram bot for downloading files from TeraBox links with advanced features including auto-rename, premium tier system, video thumbnails, real-time progress tracking, and automatic message deletion for copyright protection.

**Bot Username:** @Theinertbotz  
**Developer:** [The Inert Botz](https://t.me/TheInertBotz)  
**Support & Contact:** [@Theinertbotz](https://t.me/Theinertbotz)

---

## ✨ Key Features

### 📥 Download & Processing
- **Multi-Domain Support**: Works with 21+ TeraBox domains and variants
  - terabox.com, 1024terabox.com, terasharefile.com, mirrobox.com, nephobox.com, and more
- **Direct Link Extraction**: Advanced HTML parsing for reliable link extraction
- **Batch Processing**: Send multiple TeraBox links at once
- **Auto-Rename**: Customize file naming with variables or timestamps
- **Video Thumbnails**: Auto-generated for videos with preserved aspect ratios
- **File Size Detection**: Accurate file size calculation before upload
- **Progress Tracking**: Real-time download/upload speed and progress display

### 🎥 Video Features
- **Automatic Thumbnails**: Generated for all video files (MP4, MKV, MOV, WebM)
- **Duration Extraction**: Automatically detects video length with ffprobe
- **Aspect Ratio Preservation**: Thumbnails maintain original video proportions
- **Streaming Support**: Videos support Telegram streaming for quick preview

### 💎 Premium System
- **Time-Based Expiration**: Set temporary or permanent premium status
- **Unlimited Downloads**: Premium users get unlimited daily downloads
- **Auto-Upload Channel**: Premium users can set auto-upload channel per account
- **Admin Status Checking**: Verify user tier and download statistics
- **Automatic Downgrade**: Premium automatically downgrades when expired
- **Daily Limits**: Free users limited to 5 downloads/day, premium unlimited

### 🗑️ Auto-Delete Feature (New!)
- **Configurable Delete Time**: Set custom auto-delete time for messages
  - Format: `30s`, `5m`, `1h` (seconds, minutes, hours)
- **Per-User Toggle**: Users can enable/disable auto-delete with commands
- **Media & Notification Deletion**: Both video message and notification auto-delete
- **Copyright Protection**: Helps prevent copyright issues on Telegram
- **Toggle Commands**: Simple on/off control with `/auto_delete on/off`

### 📊 Dashboard & Statistics
- **User Dashboard**: View premium status, daily downloads, and stats
- **Activity Logging**: All downloads logged with timestamps
- **Success Metrics**: Overall system success rate tracking
- **User Analytics**: Per-user download history and data usage

### 🔐 Security & Privacy
- **Encrypted Secrets**: All API keys stored as encrypted secrets
- **No Hardcoded Credentials**: Configuration via environment variables
- **Session Management**: Secure Pyrogram session files (auto-generated)
- **MongoDB Integration**: Secure database for user data storage

### 📱 Channel Integration
- **Log Channel**: Activity logging (successful downloads)
- **Error Channel**: Error reporting and debugging
- **Storage Channel**: File backup for recovery
- **Premium Upload Channel**: Auto-forward premium user downloads

---

## 🚀 Installation & Setup

### Requirements
- Python 3.11+
- Pyrogram 2.0.106
- MongoDB (via MONGO_URI)
- Telegram Bot Token (@BotFather)
- Telegram API credentials

### Environment Setup

**Required Secrets:**
```
BOT_TOKEN          # Telegram bot token from @BotFather
API_HASH           # From https://my.telegram.org
MONGO_URI          # MongoDB connection string
```

**Required Environment Variables:**
```
API_ID             # Telegram API ID (numeric)
LOG_CHANNEL        # Log channel ID (format: -1001234567890)
ERROR_CHANNEL      # Error channel ID
STORAGE_CHANNEL    # Storage backup channel ID
```

**Optional Environment Variables:**
```
MONGO_DB           # MongoDB database name (default: "teraboxbot")
DOWNLOAD_DIR       # Download directory (default: "downloads")
WORKERS            # Worker threads (default: 20)
AUTO_DELETE        # Auto-delete feature (default: "True")
DAILY_LIMIT        # Free user daily limit (default: 5)
```

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables and secrets
# (Use Replit Secrets panel or export commands)

# Run the bot
python main.py
```

---

## 📋 Commands

### User Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `/start` | `/start` | Welcome message with quick start guide |
| `/help` | `/help` | Show all available commands |
| `/premium` | `/premium` | View premium info and pricing |
| `/rename` | `/rename` | View/manage auto-rename settings |
| `/set_rename <pattern>` | `/set_rename @Bot_{file_name}_{file_size}` | Set custom file naming pattern |
| `/auto_delete` | `/auto_delete` | Show current auto-delete status |
| `/auto_delete on` | `/auto_delete on` | Enable auto-delete notifications |
| `/auto_delete off` | `/auto_delete off` | Disable auto-delete notifications |

### Admin Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `/admin` | `/admin` | Open admin control panel |
| `/addpremium <user_id> [days]` | `/addpremium 123456789 30` | Add premium (days optional) |
| `/removepremium <user_id>` | `/removepremium 123456789` | Remove premium from user |
| `/checkuser <user_id>` | `/checkuser 123456789` | Check user tier and stats |
| `/set_upload_channel <channel_id>` | `/set_upload_channel -1001234567890` | Set premium upload channel |
| `/remove_upload_channel` | `/remove_upload_channel` | Remove upload channel |
| `/set_auto_delete <time>` | `/set_auto_delete 5m` | Set global auto-delete time |
| `/remove_auto_delete` | `/remove_auto_delete` | Disable auto-delete globally |
| `/toggle_autodelete` | `/toggle_autodelete` | Toggle admin auto-delete setting |
| `/checkchannels` | `/checkchannels` | Verify bot access to channels |

### Auto-Delete Configuration

**Set Custom Delete Time:**
```
/set_auto_delete 30s   # Delete in 30 seconds
/set_auto_delete 5m    # Delete in 5 minutes
/set_auto_delete 1h    # Delete in 1 hour
```

**Time Format:**
- `s` = seconds
- `m` = minutes
- `h` = hours

---

## 💎 Premium Features

### What's Included
- ✅ **Unlimited Downloads**: No daily limits
- ✅ **Priority Processing**: Faster download speeds
- ✅ **Auto-Upload Channel**: Files auto-upload to your channel
- ✅ **Advanced Naming**: Full custom rename support
- ✅ **Priority Support**: Get faster responses to issues

### Pricing
- **Monthly**: $4.99/month
- **Yearly**: $39.99/year (33% savings)
- **Lifetime**: Contact for special offers

### How to Upgrade
1. Use `/premium` command in bot
2. Scan the QR code or visit payment link
3. DM [@Theinertbotz](https://t.me/Theinertbotz) with proof of payment
4. Get premium status instantly!

---

## 📝 File Naming (Auto-Rename)

### Available Variables
```
{file_name}      # Original filename
{file_size}      # File size (e.g., "42MB")
{original_name}  # Full original name
{ext}            # File extension
```

### Examples
```
/set_rename @Bot_{file_name}_{file_size}
→ @Bot_video_42MB.mp4

/set_rename Download_{original_name}
→ Download_video.mp4

/set_rename {file_name}_{ext}
→ video_mp4
```

---

## 🔄 How It Works

### Download Flow
1. User sends TeraBox link(s)
2. Bot extracts direct download link from TeraBox
3. File downloads to server with progress tracking
4. Auto-rename applied based on user settings
5. Video thumbnail generated (if applicable)
6. File uploaded to user with original message link
7. Auto-delete notification shown with countdown
8. After set time: video message + notification deleted
9. File backed up to storage channel
10. Premium users: auto-uploaded to their upload channel
11. Downloaded file auto-deleted from disk (if enabled)

### Storage & Deletion
- **Server Storage**: Files kept temporarily during processing
- **Auto-Delete**: Deleted after upload (if enabled)
- **Backup**: Always kept in STORAGE_CHANNEL for recovery
- **Premium Upload**: Forwarded to user's premium channel
- **Message Deletion**: Configurable via `/set_auto_delete`

---

## ⚙️ Configuration

### Default Settings
- **Auto-Delete**: Enabled (5 seconds default)
- **Daily Limit (Free)**: 5 downloads
- **Daily Limit (Premium)**: Unlimited
- **Download Timeout**: 30 seconds for large files
- **Worker Threads**: 20 concurrent handlers

### Customization
All settings can be changed via:
- Environment variables
- Admin commands
- MongoDB settings collection

---

## 🐛 Troubleshooting

### "No TeraBox link detected"
- Make sure the link is from a supported domain
- Check that the link format is correct

### "Failed to extract direct link"
- TeraBox link may have expired
- Try sharing the file again from TeraBox
- Check bot has proper permissions

### "Upload failed - FLOOD_WAIT"
- Telegram rate limit triggered
- Wait 10-15 minutes before trying again
- This affects the user account, not the bot

### "Auto-delete not working"
- Check that auto-delete is enabled: `/auto_delete on`
- Verify delete time is set: `/auto_delete`
- Ensure you have bot permissions to delete messages

---

## 📊 Database Schema

### MongoDB Collections

**users**
```javascript
{
  _id: user_id,
  tier: "free" | "premium",
  premium_expiry: ISO_DATE | null,
  auto_rename: string,
  custom_rename_pattern: string,
  auto_delete_msgs: boolean,
  downloads_YYYY-MM-DD: number
}
```

**logs**
```javascript
{
  user_id: number,
  file: string,
  timestamp: DATE
}
```

**settings**
```javascript
{
  _id: "auto_delete" | "premium_upload_channel",
  time_seconds: number | null,
  channel_id: number | null
}
```

---

## 🔧 Technical Stack

- **Language**: Python 3.11
- **API Framework**: Pyrogram 2.0.106 (Telegram MTProto)
- **Database**: MongoDB
- **Web Server**: Flask (health checks)
- **Video Processing**: FFprobe (duration/thumbnails)
- **HTTP Client**: aiohttp
- **Async**: asyncio

### Architecture
```
main.py                 # Entry point
├── bot.py              # Pyrogram client initialization
├── health.py           # Flask health server
├── config.py           # Configuration management
├── core/               # Core logic
│   ├── router.py       # Handler registration
│   └── responses.py    # Response utilities
├── handlers/           # Command handlers
│   ├── download_handler.py
│   ├── auto_delete.py
│   ├── premium.py
│   └── admin.py
├── plugins/            # Feature modules
│   ├── script.py       # UI text
│   ├── buttons.py      # Keyboards
│   ├── premium.py      # Premium manager
│   └── [other plugins]
└── Theinertbotz/       # Core engine
    ├── api.py          # API calls
    ├── database.py     # MongoDB ops
    ├── download.py     # Download engine
    ├── uploader.py     # Upload engine
    └── [utilities]
```

---

## 📜 License

This bot is provided as-is for educational and personal use. Please respect TeraBox's terms of service and copyright laws.

---

## 🙏 Credits & Support

### Developer
**The Inert Botz** - [@Theinertbotz](https://t.me/Theinertbotz)

### Support & Contact
All support, bug reports, feature requests, and premium inquiries - DM [@Theinertbotz](https://t.me/Theinertbotz)

### Premium Upgrade
**Pricing & Payment** - DM [@Theinertbotz](https://t.me/Theinertbotz) with details

---

## 📞 Contact

- **Developer & Support**: [@Theinertbotz](https://t.me/Theinertbotz)
- **Bot Telegram**: [@Theinertbotz](https://t.me/Theinertbotz)
- **Premium & All Inquiries**: DM [@Theinertbotz](https://t.me/Theinertbotz)

---

<div align="center">

**Made with ❤️ by The Inert Botz**

[![Telegram](https://img.shields.io/badge/Telegram-@Theinertbotz-blue?style=flat&logo=telegram)](https://t.me/Theinertbotz)
[![Support](https://img.shields.io/badge/Support-@Theinertbotz-blue?style=flat&logo=telegram)](https://t.me/Theinertbotz)

*This bot helps download files from TeraBox with ease and security.*

</div>
