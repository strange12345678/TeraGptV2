class Script:
    # ===== Welcome & Start =====
    START_TEXT = """
<b>🎬 TeraBox Downloader Bot</b>

<b>⚡ Ultra-Fast File Downloads</b>

Simply send a <code>TeraBox</code> link and I'll:
✅ Download the file instantly
✅ Send it directly to your chat
✅ Generate thumbnails for videos
✅ Track download progress
✅ Support all file types

<b>📝 Quick Start:</b>
<code>https://1024terabox.com/s/1abc123def456ghi</code>

<b>🎛️ Advanced Features:</b>
• <code>/rename</code> - Customize file naming
• <code>/set_rename &lt;pattern&gt;</code> - Custom patterns
• <code>/help</code> - View all commands

<b>💡 Pro Tips:</b>
💬 Send multiple links at once
🎬 Videos get automatic thumbnails
⚡ Progress tracked in real-time
"""

    # ===== Help & Commands =====
    COMMANDS_TEXT = """
<b>📋 All Available Commands:</b>

<b>🎯 User Commands:</b>
<b>/start</b> - Show welcome message
<b>/help</b> - Show all commands
<b>/premium</b> - Premium info & upgrade options
<b>/rename</b> - View/manage rename settings
<b>/set_rename &lt;pattern&gt;</b> - Set custom file naming

<b>💎 Premium Commands:</b>
<b>/set_upload_channel &lt;channel_id&gt;</b> - Auto-upload to channel
<b>/remove_upload_channel</b> - Remove auto-upload channel

<b>⏰ Auto-Delete Commands (Admin):</b>
<b>/auto_delete</b> - Show auto-delete info & options
<b>/set_auto_delete &lt;time&gt;</b> - Set auto-delete time (30s, 5m, 1h)
<b>/remove_auto_delete</b> - Disable auto-delete

<b>📌 Rename Variables:</b>
• {file_name} • {file_size}
• {username} • {user_id}
• {date} • {time} • {timestamp}

<b>💡 Example Patterns:</b>
<code>/set_rename @Theinertbotz_{file_name}_{file_size}</code>
<code>/set_rename {{username}}_{{date}}_{{file_name}}</code>

<b>📊 How It Works:</b>
Simply send TeraBox links and the bot will download & send them with:
✅ Auto-generated video thumbnails
✅ Real-time progress tracking
✅ Custom file naming
✅ Multi-file support
"""

    # ===== About =====
    ABOUT_TEXT = """
<b>ℹ️ About TeraBox Bot</b>

A powerful Telegram bot for downloading files from TeraBox with advanced features:

<b>✨ Features:</b>
• Lightning-fast downloads
• Automatic video thumbnails
• Custom file naming with variables
• Real-time progress tracking
• Multi-file support
• Secure API integration

<b>🛠️ Built with:</b>
Pyrogram 2.0.106 • Python 3.11 • MongoDB

<b>📊 Status:</b>
✅ All systems operational

<b>👨‍💻 Developer:</b>
@Theinertbotz
"""

    # ===== Dashboard =====
    DASHBOARD_TEXT = """<b>📊 ᴅᴀsʜʙᴏᴀʀᴅ ᴏᴠᴇʀᴠɪᴇᴡ</b>

👤 <b>User:</b> {user_name}  
🆔 <b>User ID:</b> <code>{user_id}</code>  
💠 <b>Premium:</b> {premium_status}  
⏳ <b>Expiry:</b> {premium_expiry}

━━━━━━━━━━━━━━━━━━

📁 <b>Your Usage</b>  
🔹 ᴛᴏᴅᴀʏ's ᴅᴏᴡɴʟᴏᴀᴅs: <b>{today_downloads}</b>  
🔹 ᴛᴏᴅᴀʏ ʀᴇᴍᴀɪɴɪɴɢ: <b>{today_remaining}</b>  
🔹 ᴛᴏᴛᴀʟ ꜰɪʟᴇs ᴘʀᴏᴄᴇssᴇᴅ: <b>{total_downloads}</b>  
🔹 ᴅᴀᴛᴀ ᴜsᴇᴅ: <b>{total_data_used}</b>  
🔹 ꜱᴛᴏʀᴀɢᴇ ʟᴇꜰᴛ: <b>{storage_remaining}</b>

━━━━━━━━━━━━━━━━━━

⚙️ <b>Bot Status</b>  
🔆 ᴀᴘɪ sᴛᴀᴛᴜs: <b>{api_status}</b>  
📡 ᴘɪɴɢ: <b>{ping_ms} ms</b>  
⏱️ ᴜᴘᴛɪᴍᴇ: <b>{bot_uptime}</b>  
🧵 ᴀᴄᴛɪᴠᴇ ᴡᴏʀᴋᴇʀs: <b>{workers_active}</b>  
📥 ǫᴜᴇᴜᴇ sɪᴢᴇ: <b>{queue_size}</b>

━━━━━━━━━━━━━━━━━━

🧾 <b>Logs</b>  
  
📊 sᴜᴄᴄᴇss ʀᴀᴛᴇ: <b>{task_success_rate}%</b>

━━━━━━━━━━━━━━━━━━

<b>✨ ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜsɪɴɢ {bot_name}!</b>

<code>━━━━━━━━━━━━━━━━━━━━━━</code>
<u><b>𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 :</b></u> <a href="https://t.me/TheInertBotz">The Inert Botz</a>
<code>━━━━━━━━━━━━━━━━━━━━━━</code>"""

    # ===== Settings =====
    SETTINGS_TEXT = """
<b>⚙️ Settings</b>

<b>🎛️ Available Settings:</b>
• <code>/rename</code> - File naming preferences
• <code>/set_rename &lt;pattern&gt;</code> - Custom patterns
• Premium settings in <code>/premium</code>

<b>💡 Tip:</b>
All your settings are automatically saved and synced across devices.
"""

    # ===== Premium Info =====
    PREMIUM_INFO = """
<b>💎 Premium Membership</b>

<b>🎯 Unlock Premium Features:</b>
• ✅ Unlimited downloads (no daily limits)
• ✅ Priority support & faster responses
• ✅ Advanced file naming options
• ✅ Custom branding
• ✅ No ads or watermarks

<b>📊 Current Plan:</b>
• Free: 5 downloads per day
• Premium: Unlimited downloads

<b>💰 Upgrade Options:</b>
• Monthly: $4.99/month
• Yearly: $39.99/year (Save 33%)

Click the button below to upgrade now!
"""

    # ===== Rename Settings =====
    RENAME_HELP_TEXT = """
<b>🔄 Auto-Rename Settings</b>

<b>Current Status:</b> {status}

━━━━━━━━━━━━━━━━━━━━

<b>⚡ Quick Options:</b>
<code>/rename on</code> - Timestamp (YYYYMMDD_HHMMSS)
<code>/rename datetime</code> - DateTime (YYYY-MM-DD_HH-MM-SS)
<code>/rename off</code> - Disable renaming

<b>✨ Custom Naming:</b>
<code>/set_rename &lt;your_pattern&gt;</code>

<b>📝 Available Variables:</b>
{{file_name}} • {{file_size}} • {{username}}
{{user_id}} • {{date}} • {{time}}
{{timestamp}} • {{ext}}

<b>💡 Pattern Examples:</b>
<code>@Theinertbotz_{{file_name}}_{{file_size}}</code>
→ @Theinertbotz_video_42MB.mp4

<code>{{username}}_{{date}}_{{file_name}}</code>
→ admin_2025-11-22_video.mp4

<code>Archive_{{timestamp}}</code>
→ Archive_20251122_082326.zip

━━━━━━━━━━━━━━━━━━━━
"""

    # ===== Status Messages =====
    EXTRACTING = "🔎 Extracting direct link..."
    DOWNLOADING = "📥 Downloading..."
    UPLOADING = "📤 Uploading..."
    PREPARING = "📤 Preparing thumbnail & metadata..."
    COMPLETED = "✅ Completed."
    ERROR = "❌ Something went wrong. Check logs or contact admin."
    NO_LINK = """❌ <b>No TeraBox link detected</b>

Please send a valid TeraBox link:
<code>https://1024terabox.com/s/...</code>

Type <code>/help</code> for more info."""

    UNEXPECTED_ERROR = """❌ <b>An unexpected error occurred</b>

Please try again or contact support."""

    # ===== Rename Confirmations =====
    RENAME_ON = """✅ <b>Auto-rename Enabled</b>

📌 Format: <code>filename_YYYYMMDD_HHMMSS.ext</code>
💾 Applied to all downloads
Type <code>/rename</code> to change"""

    RENAME_DATETIME = """✅ <b>Auto-rename Enabled</b>

📌 Format: <code>filename_YYYY-MM-DD_HH-MM-SS.ext</code>
💾 Applied to all downloads
Type <code>/rename</code> to change"""

    RENAME_OFF = """❌ <b>Auto-rename Disabled</b>

📌 Files will keep original names
Use <code>/rename on</code> to enable again"""

    INVALID_OPTION = """❓ <b>Unknown Option</b>

Type <code>/rename</code> for help or examples."""

    CUSTOM_PATTERN_SAVED = """✅ <b>Custom Pattern Saved!</b>

📝 <b>Your Pattern:</b>
<code>{pattern}</code>

💾 <b>Applied to:</b> All future downloads

📌 <b>Example:</b>
<code>your_renamed_file.mp4</code>"""

    CUSTOM_PATTERN_USAGE = """❌ <b>Usage:</b> <code>/set_rename &lt;pattern&gt;</code>

Example: <code>/set_rename @Theinertbotz_{{file_name}}_{{file_size}}</code>

Type <code>/rename</code> for available variables."""

    CUSTOM_PATTERN_ERROR = """❌ Pattern must contain at least one variable.
Example: <code>/set_rename @Bot_{{file_name}}_{{file_size}}</code>"""

    RENAME_RESTRICTED = """❌ <b>Auto-Rename Feature Restricted</b>

This feature is only available for:
👑 Premium Members
🔐 Admins

<b>To unlock this feature:</b>
• <code>/premium</code> - Upgrade to premium
• Contact admin for more details

💡 Other features are still available for all users!"""

    # ===== Premium System =====
    LIMIT_REACHED = """❌ <b>Daily Limit Reached</b>

📊 Free users can download <b>{daily_limit} videos per day</b>

💎 <b>Upgrade to Premium for:</b>
• Unlimited downloads
• Unlimited storage
• Priority support
• No daily limits
• Special features

Type <code>/premium</code> to upgrade!"""

    PREMIUM_TEXT = """
<b>💎 Premium Features</b>

<b>✨ What's Included:</b>
• ✅ Unlimited downloads
• ✅ Unlimited video storage
• ✅ Priority support
• ✅ No daily limits
• ✅ Custom branding
• ✅ Advanced analytics

<b>📊 Free Plan Limits:</b>
• 5 downloads per day
• Basic features
• Standard support

<b>💳 Pricing:</b>
Coming soon...

Click button below to upgrade!
"""

    PREMIUM_STATUS = """
<b>👤 Your Account Status</b>

{status}

<code>/premium</code> - Premium info
<code>/rename</code> - Rename settings
"""

    UPGRADE_TEXT = """
<b>💳 Premium Membership</b>

<b>🎯 Get Premium Access:</b>
• Unlimited downloads
• Priority support
• Advanced features
• Save time & effort

<b>💰 Plans:</b>
• Monthly: $4.99/month
• Yearly: $39.99/year (Save 33%)

<b>Contact:</b>
DM @Theinertbotz for details
"""

    # ===== Admin Panel =====
    ADMIN_PANEL_TEXT = """
<b>🛠️ Admin Panel</b>

<b>⚙️ Options:</b>
• 👥 Manage Premium Users
• 🔍 Check User Status
• 📊 View System Info

Use buttons below to manage users.
"""

    ADMIN_MANAGE_TEXT = """
<b>👥 Premium User Management</b>

<b>📋 Commands:</b>
• <code>/addpremium &lt;user_id&gt; [days]</code> - Add premium
• <code>/removepremium &lt;user_id&gt;</code> - Remove premium
• <code>/checkuser &lt;user_id&gt;</code> - Check status

<b>Examples:</b>
<code>/addpremium 123456789</code> - Permanent
<code>/addpremium 123456789 30</code> - 30 days
"""
    
    AUTO_DELETE_ON = "✅ Auto-delete <b>ENABLED</b>\n\nDownloaded files will be deleted after upload to save storage."
    AUTO_DELETE_OFF = "❌ Auto-delete <b>DISABLED</b>\n\nDownloaded files will be kept after upload."
