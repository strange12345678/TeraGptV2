
# handlers/admin.py
from pyrogram import filters, enums
from config import Config
from Theinertbotz.database import db
from script import Script
from plugins.buttons import ADMIN_PANEL_BUTTONS, ADMIN_MANAGE_BUTTONS
import logging

log = logging.getLogger("TeraBoxBot")

def is_admin(user_id):
    """Check if user is an admin."""
    return user_id in Config.ADMIN_IDS

def register_handlers(app):
    @app.on_message(filters.command("checkchannels") & filters.private)
    async def check_channels(client, message):
        """Check if bot can access configured channels"""
        from pyrogram import enums
        results = []
        has_errors = False
        
        # Check LOG_CHANNEL
        if Config.LOG_CHANNEL:
            try:
                chat = await client.get_chat(Config.LOG_CHANNEL)
                results.append(f"✅ LOG_CHANNEL: {chat.title} ({Config.LOG_CHANNEL})")
            except Exception as e:
                has_errors = True
                error_msg = "Bot not added to channel" if "Peer id invalid" in str(e) else str(e)
                results.append(f"❌ LOG_CHANNEL ({Config.LOG_CHANNEL}): {error_msg}")
        else:
            results.append("⚠️ LOG_CHANNEL not configured")
        
        # Check ERROR_CHANNEL
        if Config.ERROR_CHANNEL:
            try:
                chat = await client.get_chat(Config.ERROR_CHANNEL)
                results.append(f"✅ ERROR_CHANNEL: {chat.title} ({Config.ERROR_CHANNEL})")
            except Exception as e:
                has_errors = True
                error_msg = "Bot not added to channel" if "Peer id invalid" in str(e) else str(e)
                results.append(f"❌ ERROR_CHANNEL ({Config.ERROR_CHANNEL}): {error_msg}")
        else:
            results.append("⚠️ ERROR_CHANNEL not configured")
        
        # Check STORAGE_CHANNEL
        if Config.STORAGE_CHANNEL:
            try:
                chat = await client.get_chat(Config.STORAGE_CHANNEL)
                results.append(f"✅ STORAGE_CHANNEL: {chat.title} ({Config.STORAGE_CHANNEL})")
            except Exception as e:
                has_errors = True
                error_msg = "Bot not added to channel" if "Peer id invalid" in str(e) else str(e)
                results.append(f"❌ STORAGE_CHANNEL ({Config.STORAGE_CHANNEL}): {error_msg}")
        else:
            results.append("⚠️ STORAGE_CHANNEL not configured")
        
        response = "<b>📊 Channel Status:</b>\n\n" + "\n".join(results)
        
        if has_errors:
            response += "\n\n<b>💡 How to fix:</b>\n1. Open your channel in Telegram\n2. Click channel name → Administrators\n3. Add your bot as admin\n4. Grant 'Post Messages' permission\n5. Run /checkchannels again"
        
        await message.reply(response, parse_mode=enums.ParseMode.HTML)
    
    # ===== /admin Command =====
    @app.on_message(filters.command("admin") & filters.private)
    async def admin_panel(client, message):
        """Admin panel for managing premium users."""
        if not is_admin(message.from_user.id):
            await message.reply("❌ You don't have admin access.", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            await message.reply(Script.ADMIN_PANEL_TEXT, reply_markup=ADMIN_PANEL_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("admin_panel error")
    
    # ===== Admin Panel Callback =====
    @app.on_callback_query(filters.regex("^admin_panel$"))
    async def admin_panel_callback(client, callback_query):
        if not is_admin(callback_query.from_user.id):
            await callback_query.answer("❌ Admin access required", show_alert=True)
            return
        
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.ADMIN_PANEL_TEXT, reply_markup=ADMIN_PANEL_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("admin_panel_callback error")
    
    # ===== Manage Premium Users =====
    @app.on_callback_query(filters.regex("^admin_manage$"))
    async def admin_manage_callback(client, callback_query):
        if not is_admin(callback_query.from_user.id):
            await callback_query.answer("❌ Admin access required", show_alert=True)
            return
        
        try:
            await callback_query.answer()
            await callback_query.message.edit_text(Script.ADMIN_MANAGE_TEXT, reply_markup=ADMIN_MANAGE_BUTTONS, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("admin_manage_callback error")
    
    # ===== Add Premium User =====
    @app.on_message(filters.command("addpremium") & filters.private)
    async def add_premium_cmd(client, message):
        """Add a user to premium. Usage: /addpremium <user_id> [days]"""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            args = message.text.split()
            if len(args) < 2:
                await message.reply("📝 Usage: <code>/addpremium &lt;user_id&gt; [days]</code>\n\n<b>Examples:</b>\n<code>/addpremium 123456789</code> - Permanent\n<code>/addpremium 123456789 30</code> - 30 days", parse_mode=enums.ParseMode.HTML)
                return
            
            user_id = int(args[1])
            days = None
            
            if len(args) > 2:
                days = int(args[2])
                if days <= 0:
                    await message.reply("❌ Days must be greater than 0", parse_mode=enums.ParseMode.HTML)
                    return
            
            db.set_premium_expiry(user_id, days)
            
            if days is None:
                duration = "Permanent"
            else:
                duration = f"{days} days"
            
            await message.reply(f"✅ User {user_id} upgraded to <b>Premium</b> ({duration})", parse_mode=enums.ParseMode.HTML)
            log.info(f"Admin {message.from_user.id} added premium for user {user_id} for {duration}")
        except ValueError as e:
            await message.reply(f"❌ Invalid format. {str(e)}", parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("add_premium_cmd error")
    
    # ===== Remove Premium User =====
    @app.on_message(filters.command("removepremium") & filters.private)
    async def remove_premium_cmd(client, message):
        """Remove premium from a user. Usage: /removepremium <user_id>"""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            args = message.text.split()
            if len(args) < 2:
                await message.reply("📝 Usage: <code>/removepremium &lt;user_id&gt;</code>", parse_mode=enums.ParseMode.HTML)
                return
            
            user_id = int(args[1])
            db.set_user_tier(user_id, "free")
            await message.reply(f"✅ User {user_id} downgraded to <b>Free</b>", parse_mode=enums.ParseMode.HTML)
            log.info(f"Admin {message.from_user.id} removed premium from user {user_id}")
        except ValueError:
            await message.reply("❌ Invalid user ID format", parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("remove_premium_cmd error")
    
    # ===== Check User Status =====
    @app.on_message(filters.command("checkuser") & filters.private)
    async def check_user_cmd(client, message):
        """Check user status. Usage: /checkuser <user_id>"""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            args = message.text.split()
            if len(args) < 2:
                await message.reply("📝 Usage: <code>/checkuser &lt;user_id&gt;</code>", parse_mode=enums.ParseMode.HTML)
                return
            
            user_id = int(args[1])
            tier = db.get_user_tier(user_id)
            daily_downloads = db.get_daily_downloads(user_id)
            
            status = f"""
<b>👤 User Status Report</b>

<b>User ID:</b> <code>{user_id}</code>
<b>Tier:</b> {'👑 Premium' if tier == 'premium' else '🎯 Free'}
<b>Downloads Today:</b> {daily_downloads}
<b>Remaining:</b> {'∞ (Unlimited)' if tier == 'premium' else max(0, 5 - daily_downloads)}
"""
            await message.reply(status, parse_mode=enums.ParseMode.HTML)
        except ValueError:
            await message.reply("❌ Invalid user ID format", parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("check_user_cmd error")
