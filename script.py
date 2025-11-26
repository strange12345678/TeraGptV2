class Script:
    # ===== Welcome & Start =====
    START_TEXT = """
<b>🎬 ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ</b>

ᴡᴇʟᴄᴏᴍᴇ! sᴇɴᴅ ᴀ <code>ᴛᴇʀᴀʙᴏx</code> ʟɪɴᴋ ᴀɴᴅ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ.

<b>✨ ꜰᴇᴀᴛᴜʀᴇs:</b>
• ᴀᴜᴛᴏ-ɢᴇɴᴇʀᴀᴛᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟs
• ᴀᴜᴛᴏ-ʀᴇɴᴀᴍᴇ sᴜᴘᴘᴏʀᴛ
• ᴘʀᴇᴍɪᴜᴍ ᴛɪᴇʀ sʏsᴛᴇᴍ
"""

    # ===== Help & Commands =====
    COMMANDS_TEXT = """
<b>📋 ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:</b>

<b>🎯 ʙᴀsɪᴄ:</b>
<b>/start</b> - ᴡᴇʟᴄᴏᴍᴇ
<b>/premium</b> - ᴘʀᴇᴍɪᴜᴍ ɪɴꜰᴏ
<b>/rename</b> - ʀᴇɴᴀᴍᴇ sᴇᴛᴛɪɴɢs

<b>⚙️ ʀᴇɴᴀᴍᴇ:</b>
<b>/set_rename &lt;pattern&gt;</b>
ᴠᴀʀɪᴀʙʟᴇs: {file_name}, {file_size}
ᴇxᴀᴍᴘʟᴇ: /set_rename @Bot_{file_name}

<b>🗑️ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ:</b>
<b>/auto_delete on|off</b>
<b>/set_auto_delete &lt;time&gt;</b>
ᴛɪᴍᴇ: 30s, 5m, 1h

<b>💎 ᴘʀᴇᴍɪᴜᴍ:</b>
<b>/set_upload_channel</b>
<b>/remove_upload_channel</b>

<b>🛠️ ᴀᴅᴍɪɴ:</b>
<b>/admin</b> - ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ
<b>/addpremium</b> - ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ
<b>/checkuser</b> - ᴄʜᴇᴄᴋ sᴛᴀᴛᴜs
"""

    # ===== About =====
    ABOUT_TEXT = """
<b>ℹ️ ᴀʙᴏᴜᴛ ᴛᴇʀᴀʙᴏx ʙᴏᴛ</b>

ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ꜰɪʟᴇs ꜰʀᴏᴍ ᴛᴇʀᴀʙᴏx ᴡɪᴛʜ ᴀᴅᴠᴀɴᴄᴇᴅ ꜰᴇᴀᴛᴜʀᴇs:

<b>✨ ꜰᴇᴀᴛᴜʀᴇs:</b>
• ʟɪɢʜᴛɴɪɴɢ-ꜰᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅs
• ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴠɪᴅᴇᴏ ᴛʜᴜᴍʙɴᴀɪʟs
• ᴄᴜsᴛᴏᴍ ꜰɪʟᴇ ɴᴀᴍɪɴɢ ᴡɪᴛʜ ᴠᴀʀɪᴀʙʟᴇs
• ʀᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏɢʀᴇss ᴛʀᴀᴄᴋɪɴɢ
• ᴍᴜʟᴛɪ-ꜰɪʟᴇ sᴜᴘᴘᴏʀᴛ
• sᴇᴄᴜʀᴇ ᴀᴘɪ ɪɴᴛᴇɢʀᴀᴛɪᴏɴ

<b>🛠️ ʙᴜɪʟᴛ ᴡɪᴛʜ:</b>
Pyrogram 2.0.106 • Python 3.11 • MongoDB

<b>📊 sᴛᴀᴛᴜs:</b>
✅ ᴀʟʟ sʏsᴛᴇᴍs ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ

<b>👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b>
@Theinertbotz
"""

    # ===== Dashboard =====
    DASHBOARD_TEXT = """<b>📊 ᴅᴀsʜʙᴏᴀʀᴅ ᴏᴠᴇʀᴠɪᴇᴡ</b>

👤 <b>ᴜsᴇʀ:</b> {user_name}  
🆔 <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>  
💠 <b>ᴘʀᴇᴍɪᴜᴍ:</b> {premium_status}  
⏳ <b>ᴇxᴘɪʀʏ:</b> {premium_expiry}

━━━━━━━━━━━━━━━━━━

📁 <b>ʏᴏᴜʀ ᴜsᴀɢᴇ</b>  
🔹 ᴛᴏᴅᴀʏ's ᴅᴏᴡɴʟᴏᴀᴅs: <b>{today_downloads}</b>  
🔹 ᴛᴏᴅᴀʏ ʀᴇᴍᴀɪɴɪɴɢ: <b>{today_remaining}</b>  
🔹 ᴛᴏᴛᴀʟ ꜰɪʟᴇs ᴘʀᴏᴄᴇssᴇᴅ: <b>{total_downloads}</b>  
🔹 ᴅᴀᴛᴀ ᴜsᴇᴅ: <b>{total_data_used}</b>  
🔹 ꜱᴛᴏʀᴀɢᴇ ʟᴇꜰᴛ: <b>{storage_remaining}</b>

━━━━━━━━━━━━━━━━━━

⚙️ <b>ʙᴏᴛ sᴛᴀᴛᴜs</b>  
🔆 ᴀᴘɪ sᴛᴀᴛᴜs: <b>{api_status}</b>  
📡 ᴘɪɴɢ: <b>{ping_ms} ms</b>  
⏱️ ᴜᴘᴛɪᴍᴇ: <b>{bot_uptime}</b>  
🧵 ᴀᴄᴛɪᴠᴇ ᴡᴏʀᴋᴇʀs: <b>{workers_active}</b>  
📥 ǫᴜᴇᴜᴇ sɪᴢᴇ: <b>{queue_size}</b>

━━━━━━━━━━━━━━━━━━

🧾 <b>ʟᴏɢs</b>  
  
📊 sᴜᴄᴄᴇss ʀᴀᴛᴇ: <b>{task_success_rate}%</b>

━━━━━━━━━━━━━━━━━━

<b>✨ ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜsɪɴɢ {bot_name}!</b>

<code>━━━━━━━━━━━━━━━━━━━━━━</code>
<u><b>𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆 :</b></u> <a href="https://t.me/TheInertBotz">ᴛʜᴇ ɪɴᴇʀᴛ ʙᴏᴛᴢ</a>
<code>━━━━━━━━━━━━━━━━━━━━━━</code>"""

    # ===== Settings =====
    SETTINGS_TEXT = """
<b>⚙️ sᴇᴛᴛɪɴɢs</b>

<b>🎛️ ᴀᴠᴀɪʟᴀʙʟᴇ sᴇᴛᴛɪɴɢs:</b>
• <code>/rename</code> - ꜰɪʟᴇ ɴᴀᴍɪɴɢ ᴘʀᴇꜰᴇʀᴇɴᴄᴇs
• <code>/set_rename &lt;pattern&gt;</code> - ᴄᴜsᴛᴏᴍ ᴘᴀᴛᴛᴇʀɴs
• ᴘʀᴇᴍɪᴜᴍ sᴇᴛᴛɪɴɢs ɪɴ <code>/premium</code>

<b>💡 ᴛɪᴘ:</b>
ᴀʟʟ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ᴀʀᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ sᴀᴠᴇᴅ ᴀɴᴅ sʏɴᴄᴇᴅ ᴀᴄʀᴏss ᴅᴇᴠɪᴄᴇs.
"""

    # ===== Admin Storage Rename Commands =====
    ADMIN_STORE_RENAME_HELP = """
<b>📝 Storage Channel Rename Commands</b>

<b>Available Commands:</b>
• <code>/store_rename</code> - Show current status
• <code>/store_rename on</code> - Enable rename
• <code>/store_rename off</code> - Disable rename
• <code>/set_store_rename [pattern]</code> - Set custom pattern
• <code>/remove_store_rename</code> - Reset to default

<b>Available Variables:</b>
• <code>{file_name}</code> - Original filename with extension
• <code>{file_size}</code> - File size (e.g., "2.6 MB")
• <code>{date}</code> - Current date (YYYY-MM-DD)
• <code>{timestamp}</code> - Timestamp (YYYYMMDD_HHMMSS)
• <code>{time}</code> - Current time (HH-MM-SS)
• <code>{datetime}</code> - Full datetime (YYYY-MM-DD_HH-MM-SS)
• <code>{user_id}</code> - User ID
• <code>{username}</code> - Username

<b>Examples:</b>
<code>/set_store_rename [STORAGE] {file_name}_{date}</code>
<code>/set_store_rename {username}_{file_name}_{timestamp}</code>
<code>/set_store_rename BACKUP_{date}_{file_name}</code>
"""

    # ===== Premium Info =====
    PREMIUM_INFO = """
<b>💎 ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀsʜɪᴘ</b>

<b>🎯 ᴜɴʟᴏᴄᴋ ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇs:</b>
• ✅ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅs (ɴᴏ ᴅᴀɪʟʏ ʟɪᴍɪᴛs)
• ✅ ᴘʀɪᴏʀɪᴛʏ sᴜᴘᴘᴏʀᴛ & ꜰᴀsᴛᴇʀ ʀᴇsᴘᴏɴsᴇs
• ✅ ᴀᴅᴠᴀɴᴄᴇᴅ ꜰɪʟᴇ ɴᴀᴍɪɴɢ ᴏᴘᴛɪᴏɴs
• ✅ ᴄᴜsᴛᴏᴍ ʙʀᴀɴᴅɪɴɢ
• ✅ ɴᴏ ᴀᴅs ᴏʀ ᴡᴀᴛᴇʀᴍᴀʀᴋs

<b>📊 ᴄᴜʀʀᴇɴᴛ ᴘʟᴀɴ:</b>
• ꜰʀᴇᴇ: 5 ᴅᴏᴡɴʟᴏᴀᴅs ᴘᴇʀ ᴅᴀʏ
• ᴘʀᴇᴍɪᴜᴍ: ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅs

<b>💰 ᴜᴘɢʀᴀᴅᴇ ᴏᴘᴛɪᴏɴs:</b>
• ᴍᴏɴᴛʜʟʏ: $4.99/month
• ʏᴇᴀʀʟʏ: $39.99/year (sᴀᴠᴇ 33%)

ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴜᴘɢʀᴀᴅᴇ ɴᴏᴡ!
"""

    # ===== Rename Settings =====
    RENAME_HELP_TEXT = """
<b>🔄 ᴀᴜᴛᴏ-ʀᴇɴᴀᴍᴇ sᴇᴛᴛɪɴɢs</b>

<b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs:</b> {status}

━━━━━━━━━━━━━━━━━━━━

<b>⚡ qᴜɪᴄᴋ ᴏᴘᴛɪᴏɴs:</b>
<code>/rename on</code> - ᴛɪᴍᴇsᴛᴀᴍᴘ (YYYYMMDD_HHMMSS)
<code>/rename datetime</code> - ᴅᴀᴛᴇᴛɪᴍᴇ (YYYY-MM-DD_HH-MM-SS)
<code>/rename off</code> - ᴅɪsᴀʙʟᴇ ʀᴇɴᴀᴍɪɴɢ

<b>✨ ᴄᴜsᴛᴏᴍ ɴᴀᴍɪɴɢ:</b>
<code>/set_rename &lt;your_pattern&gt;</code>

<b>📝 ᴀᴠᴀɪʟᴀʙʟᴇ ᴠᴀʀɪᴀʙʟᴇs:</b>

<b>ꜰɪʟᴇ ɪɴꜰᴏ:</b>
• {{file_name}} - ᴏʀɪɢɪɴᴀʟ ꜰɪʟᴇɴᴀᴍᴇ (ᴡɪᴛʜ ᴇxᴛ)
• {{file_size}} - ꜰɪʟᴇ sɪᴢᴇ (ᴇ.ɢ. 5.2ᴍʙ)

<b>ᴅᴀᴛᴇ & ᴛɪᴍᴇ:</b>
• {{date}} - ᴅᴀᴛᴇ (YYYY-MM-DD)
• {{timestamp}} - ᴛɪᴍᴇsᴛᴀᴍᴘ (YYYYMMDDHHMMss)
• {{datetime}} - ᴅᴀᴛᴇ+ᴛɪᴍᴇ (YYYY-MM-DD_HH-MM-SS)
• {{time}} - ᴛɪᴍᴇ ᴏɴʟʏ (HH-MM-SS)

<b>ᴜsᴇʀ ɪɴꜰᴏ:</b>
• {{user_id}} - ʏᴏᴜʀ ᴜsᴇʀ ɪᴅ
• {{username}} - ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴜsᴇʀɴᴀᴍᴇ

<b>💡 ᴘᴀᴛᴛᴇʀɴ ᴇxᴀᴍᴘʟᴇs:</b>
<code>{{file_name}}_{{date}}</code>
→ movie.mp4_2025-11-24

<code>Download_{{file_name}}</code>
→ Download_movie.mp4

<code>{{username}}_{{timestamp}}_{{file_name}}</code>
→ john_20251124_145230_movie.mp4

━━━━━━━━━━━━━━━━━━━━
"""

    # ===== Status Messages =====
    EXTRACTING = "🔎 ᴇxᴛʀᴀᴄᴛɪɴɢ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ..."
    DOWNLOADING = "📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ..."
    UPLOADING = "📤 ᴜᴘʟᴏᴀᴅɪɴɢ..."
    PREPARING = "📤 ᴘʀᴇᴘᴀʀɪɴɢ ᴛʜᴜᴍʙɴᴀɪʟ & ᴍᴇᴛᴀᴅᴀᴛᴀ..."
    COMPLETED = "✅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ."
    ERROR = "❌ sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ᴄʜᴇᴄᴋ ʟᴏɢs ᴏʀ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ."
    NO_LINK = """❌ <b>ɴᴏ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ</b>

ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ:
<code>https://1024terabox.com/s/...</code>

ᴛʏᴘᴇ <code>/help</code> ꜰᴏʀ ᴍᴏʀᴇ ɪɴꜰᴏ."""

    UNEXPECTED_ERROR = """❌ <b>ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ</b>

ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ."""

    # ===== Rename Confirmations =====
    RENAME_ON = """✅ <b>ᴀᴜᴛᴏ-ʀᴇɴᴀᴍᴇ ᴇɴᴀʙʟᴇᴅ</b>

📌 ꜰᴏʀᴍᴀᴛ: <code>filename_YYYYMMDD_HHMMSS.ext</code>
💾 ᴀᴘᴘʟɪᴇᴅ ᴛᴏ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅs
ᴛʏᴘᴇ <code>/rename</code> ᴛᴏ ᴄʜᴀɴɢᴇ"""

    RENAME_DATETIME = """✅ <b>ᴀᴜᴛᴏ-ʀᴇɴᴀᴍᴇ ᴇɴᴀʙʟᴇᴅ</b>

📌 ꜰᴏʀᴍᴀᴛ: <code>filename_YYYY-MM-DD_HH-MM-SS.ext</code>
💾 ᴀᴘᴘʟɪᴇᴅ ᴛᴏ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅs
ᴛʏᴘᴇ <code>/rename</code> ᴛᴏ ᴄʜᴀɴɢᴇ"""

    RENAME_OFF = """❌ <b>ᴀᴜᴛᴏ-ʀᴇɴᴀᴍᴇ ᴅɪsᴀʙʟᴇᴅ</b>

📌 ꜰɪʟᴇs ᴡɪʟʟ ᴋᴇᴇᴘ ᴏʀɪɢɪɴᴀʟ ɴᴀᴍᴇs
ᴜsᴇ <code>/rename on</code> ᴛᴏ ᴇɴᴀʙʟᴇ ᴀɢᴀɪɴ"""

    INVALID_OPTION = """❓ <b>ᴜɴᴋɴᴏᴡɴ ᴏᴘᴛɪᴏɴ</b>

ᴛʏᴘᴇ <code>/rename</code> ꜰᴏʀ ʜᴇʟᴘ ᴏʀ ᴇxᴀᴍᴘʟᴇs."""

    CUSTOM_PATTERN_SAVED = """✅ <b>ᴄᴜsᴛᴏᴍ ᴘᴀᴛᴛᴇʀɴ sᴀᴠᴇᴅ!</b>

📝 <b>ʏᴏᴜʀ ᴘᴀᴛᴛᴇʀɴ:</b>
<code>{pattern}</code>

💾 <b>ᴀᴘᴘʟɪᴇᴅ ᴛᴏ:</b> ᴀʟʟ ꜰᴜᴛᴜʀᴇ ᴅᴏᴡɴʟᴏᴀᴅs

📌 <b>ᴇxᴀᴍᴘʟᴇ:</b>
<code>your_renamed_file.mp4</code>"""

    CUSTOM_PATTERN_USAGE = """❌ <b>ᴜsᴀɢᴇ:</b> <code>/set_rename &lt;pattern&gt;</code>

ᴇxᴀᴍᴘʟᴇ: <code>/set_rename @Theinertbotz_{{file_name}}_{{file_size}}</code>

ᴛʏᴘᴇ <code>/rename</code> ꜰᴏʀ ᴀᴠᴀɪʟᴀʙʟᴇ ᴠᴀʀɪᴀʙʟᴇs."""

    CUSTOM_PATTERN_ERROR = """❌ ᴘᴀᴛᴛᴇʀɴ ᴍᴜsᴛ ᴄᴏɴᴛᴀɪɴ ᴀᴛ ʟᴇᴀsᴛ ᴏɴᴇ ᴠᴀʀɪᴀʙʟᴇ.
ᴇxᴀᴍᴘʟᴇ: <code>/set_rename @Bot_{{file_name}}_{{file_size}}</code>"""

    RENAME_RESTRICTED = """❌ <b>ᴀᴜᴛᴏ-ʀᴇɴᴀᴍᴇ ꜰᴇᴀᴛᴜʀᴇ ʀᴇsᴛʀɪᴄᴛᴇᴅ</b>

ᴛʜɪs ꜰᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ:
👑 ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀs
🔐 ᴀᴅᴍɪɴs

<b>ᴛᴏ ᴜɴʟᴏᴄᴋ ᴛʜɪs ꜰᴇᴀᴛᴜʀᴇ:</b>
• <code>/premium</code> - ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ
• ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ꜰᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs

💡 ᴏᴛʜᴇʀ ꜰᴇᴀᴛᴜʀᴇs ᴀʀᴇ sᴛɪʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴀʟʟ ᴜsᴇʀs!"""

    UPLOAD_CHANNEL_RESTRICTED = """❌ <b>ᴀᴜᴛᴏ-ᴜᴘʟᴏᴀᴅ ꜰᴇᴀᴛᴜʀᴇ ʀᴇsᴛʀɪᴄᴛᴇᴅ</b>

ᴛʜɪs ꜰᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ:
👑 ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀs
🔐 ᴀᴅᴍɪɴs

<b>ᴛᴏ ᴜɴʟᴏᴄᴋ ᴛʜɪs ꜰᴇᴀᴛᴜʀᴇ:</b>
• <code>/premium</code> - ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ
• ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ꜰᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs

💡 ʏᴏᴜʀ ᴅᴏᴡɴʟᴏᴀᴅs ᴀʀᴇ sᴛɪʟʟ ᴘʀᴏᴄᴇssᴇᴅ ɴᴏʀᴍᴀʟʟʏ!"""

    UPLOAD_CHANNEL_ALREADY_SET = """⚠️ <b>ᴜᴘʟᴏᴀᴅ ᴄʜᴀɴɴᴇʟ ᴀʟʀᴇᴀᴅʏ ᴄᴏɴꜰɪɢᴜʀᴇᴅ</b>

📍 <b>ᴄᴜʀʀᴇɴᴛ ᴄʜᴀɴɴᴇʟ:</b> {current_channel}
🔗 <b>ᴄʜᴀɴɴᴇʟ ɪᴅ:</b> <code>{channel_id}</code>

<b>✅ ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ɪᴛ:</b>
<code>/set_upload_channel &lt;new_channel_id&gt;</code>

<b>❌ ᴛᴏ ʀᴇᴍᴏᴠᴇ ɪᴛ:</b>
<code>/remove_upload_channel</code>"""

    # ===== Premium System =====
    LIMIT_REACHED = """❌ <b>ᴅᴀɪʟʏ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ</b>

📊 ꜰʀᴇᴇ ᴜsᴇʀs ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ <b>{daily_limit} ᴠɪᴅᴇᴏs ᴘᴇʀ ᴅᴀʏ</b>

💎 <b>ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ꜰᴏʀ:</b>
• ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅs
• ᴜɴʟɪᴍɪᴛᴇᴅ sᴛᴏʀᴀɢᴇ
• ᴘʀɪᴏʀɪᴛʏ sᴜᴘᴘᴏʀᴛ
• ɴᴏ ᴅᴀɪʟʏ ʟɪᴍɪᴛs
• sᴘᴇᴄɪᴀʟ ꜰᴇᴀᴛᴜʀᴇs

ᴛʏᴘᴇ <code>/premium</code> ᴛᴏ ᴜᴘɢʀᴀᴅᴇ!"""

    PREMIUM_TEXT = """
<b>💎 ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇs</b>

<b>✨ ᴡʜᴀᴛ's ɪɴᴄʟᴜᴅᴇᴅ:</b>
• ✅ ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅs
• ✅ ᴜɴʟɪᴍɪᴛᴇᴅ ᴠɪᴅᴇᴏ sᴛᴏʀᴀɢᴇ
• ✅ ᴘʀɪᴏʀɪᴛʏ sᴜᴘᴘᴏʀᴛ
• ✅ ɴᴏ ᴅᴀɪʟʏ ʟɪᴍɪᴛs
• ✅ ᴄᴜsᴛᴏᴍ ʙʀᴀɴᴅɪɴɢ
• ✅ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴀʟʏᴛɪᴄs

<b>📊 ꜰʀᴇᴇ ᴘʟᴀɴ ʟɪᴍɪᴛs:</b>
• 5 ᴅᴏᴡɴʟᴏᴀᴅs ᴘᴇʀ ᴅᴀʏ
• ʙᴀsɪᴄ ꜰᴇᴀᴛᴜʀᴇs
• sᴛᴀɴᴅᴀʀᴅ sᴜᴘᴘᴏʀᴛ

<b>💳 ᴘʀɪᴄɪɴɢ:</b>
ᴄᴏᴍɪɴɢ sᴏᴏɴ...

ᴄʟɪᴄᴋ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴜᴘɢʀᴀᴅᴇ!
"""

    PREMIUM_STATUS = """
<b>👤 ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ sᴛᴀᴛᴜs</b>

{status}

<code>/premium</code> - ᴘʀᴇᴍɪᴜᴍ ɪɴꜰᴏ
<code>/rename</code> - ʀᴇɴᴀᴍᴇ sᴇᴛᴛɪɴɢs
"""

    UPGRADE_TEXT = """
<b>💳 ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀsʜɪᴘ</b>

<b>🎯 ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss:</b>
• ᴜɴʟɪᴍɪᴛᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅs
• ᴘʀɪᴏʀɪᴛʏ sᴜᴘᴘᴏʀᴛ
• ᴀᴅᴠᴀɴᴄᴇᴅ ꜰᴇᴀᴛᴜʀᴇs
• sᴀᴠᴇ ᴛɪᴍᴇ & ᴇꜰꜰᴏʀᴛ

<b>💰 ᴘʟᴀɴs:</b>
• ᴍᴏɴᴛʜʟʏ: $4.99/month
• ʏᴇᴀʀʟʏ: $39.99/year (sᴀᴠᴇ 33%)

<b>ᴄᴏɴᴛᴀᴄᴛ:</b>
ᴅᴍ @Theinertbotz ꜰᴏʀ ᴅᴇᴛᴀɪʟs
"""

    # ===== Admin Panel =====
    ADMIN_PANEL_TEXT = """
<b>🛠️ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ</b>

<b>⚙️ ᴏᴘᴛɪᴏɴs:</b>
• 👥 ᴍᴀɴᴀɢᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs
• 🔍 ᴄʜᴇᴄᴋ ᴜsᴇʀ sᴛᴀᴛᴜs
• 📊 ᴠɪᴇᴡ sʏsᴛᴇᴍ ɪɴꜰᴏ

ᴜsᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴜsᴇʀs.
"""

    ADMIN_MANAGE_TEXT = """
<b>👥 ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ</b>

<b>📋 ᴄᴏᴍᴍᴀɴᴅs:</b>
• <code>/addpremium &lt;user_id&gt; [days]</code> - ᴀᴅᴅ ᴘʀᴇᴍɪᴜᴍ
• <code>/removepremium &lt;user_id&gt;</code> - ʀᴇᴍᴏᴠᴇ ᴘʀᴇᴍɪᴜᴍ
• <code>/checkuser &lt;user_id&gt;</code> - ᴄʜᴇᴄᴋ sᴛᴀᴛᴜs

<b>ᴇxᴀᴍᴘʟᴇs:</b>
<code>/addpremium 123456789</code> - ᴘᴇʀᴍᴀɴᴇɴᴛ
<code>/addpremium 123456789 30</code> - 30 ᴅᴀʏs
"""
    
    AUTO_DELETE_ON = "✅ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ <b>ᴇɴᴀʙʟᴇᴅ</b>\n\nᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜰɪʟᴇs ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀꜰᴛᴇʀ ᴜᴘʟᴏᴀᴅ ᴛᴏ sᴀᴠᴇ sᴛᴏʀᴀɢᴇ."
    AUTO_DELETE_OFF = "❌ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ <b>ᴅɪsᴀʙʟᴇᴅ</b>\n\nᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜰɪʟᴇs ᴡɪʟʟ ʙᴇ ᴋᴇᴘᴛ ᴀꜰᴛᴇʀ ᴜᴘʟᴏᴀᴅ."
    
    # ===== API Switching =====
    API_SWITCHED = "🔄 <b>ᴀᴘɪ sᴡɪᴛᴄʜᴇᴅ</b>\n\n📡 ᴄᴜʀʀᴇɴᴛ ᴀᴘɪ: <b>{current_api}</b>\n\nᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴜsᴇ ᴛʜɪs ᴀᴘɪ ꜰᴏʀ ᴀʟʟ ꜰᴜᴛᴜʀᴇ ᴅᴏᴡɴʟᴏᴀᴅs."
    
    # ===== User Auto-Delete Messages =====
    AUTO_DELETE_ENABLED = "✅ <b>ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴇɴᴀʙʟᴇᴅ</b>\n\n⏱️ ᴠɪᴅᴇᴏ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ɪɴ <b>5 sᴇᴄᴏɴᴅs</b> ᴛᴏ ʜᴇʟᴘ ᴘʀᴇᴠᴇɴᴛ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.\n\n📌 <i>ᴘʀᴇᴍɪᴜᴍ & ꜰʀᴇᴇ ᴜsᴇʀs: ʙᴏᴛʜ ᴡɪʟʟ ʜᴀᴠᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴇɴᴀʙʟᴇᴅ</i>"
    
    AUTO_DELETE_DISABLED = "⏹️ <b>ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴅɪsᴀʙʟᴇᴅ</b>\n\n⏱️ ᴠɪᴅᴇᴏ ᴍᴇssᴀɢᴇs ᴡɪʟʟ <b>ɴᴏᴛ</b> ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ.\n\n⚠️ <i>ʀᴇᴍᴇᴍʙᴇʀ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ sᴛᴏʀᴀɢᴇ ᴍᴀɴᴜᴀʟʟʏ</i>"
    
    AUTO_DELETE_NOTIFY = "⏰ <b>ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ɪɴ {time}</b> 🗑️\n\n💡 <i>ᴛʜɪs ʜᴇʟᴘs ᴘʀᴇᴠᴇɴᴛ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ</i>"
    
    SET_AUTO_DELETE_USAGE = """<b>⏱️ sᴇᴛ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ</b>

<b>ᴜsᴀɢᴇ:</b> <code>/set_auto_delete &lt;time&gt;</code>

<b>ꜰᴏʀᴍᴀᴛ:</b>
• <code>s</code> = sᴇᴄᴏɴᴅs
• <code>m</code> = ᴍɪɴᴜᴛᴇs
• <code>h</code> = ʜᴏᴜʀs

<b>ᴇxᴀᴍᴘʟᴇs:</b>
<code>/set_auto_delete 30s</code> - ᴅᴇʟᴇᴛᴇ ɪɴ 30 sᴇᴄᴏɴᴅs
<code>/set_auto_delete 5m</code> - ᴅᴇʟᴇᴛᴇ ɪɴ 5 ᴍɪɴᴜᴛᴇs
<code>/set_auto_delete 1h</code> - ᴅᴇʟᴇᴛᴇ ɪɴ 1 ʜᴏᴜʀ

<code>/remove_auto_delete</code> - ᴅɪsᴀʙʟᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ"""
