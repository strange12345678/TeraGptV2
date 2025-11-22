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
<b>📋 Available Commands:</b>

<b>/start</b> - Show welcome message
<b>/help</b> - Show this message
<b>/rename</b> - View rename settings
<b>/set_rename &lt;pattern&gt;</b> - Set custom naming

<b>📌 Rename Variables:</b>
• {file_name} • {file_size}
• {username} • {user_id}
• {date} • {time} • {timestamp}

<b>💡 Example:</b>
<code>/set_rename @Theinertbotz_{file_name}_{file_size}</code>
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
