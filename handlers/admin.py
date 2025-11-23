
# handlers/admin.py
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from Theinertbotz.database import db
from script import Script
from plugins.buttons import ADMIN_PANEL_BUTTONS, ADMIN_MANAGE_BUTTONS, ADMIN_SETTINGS_BUTTONS
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
            panel_text = Script.ADMIN_PANEL_TEXT + "\n\n<b>⚙️ Settings:</b>\n• ♻️ Auto-Delete Files"
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("👥 Manage Premium Users", callback_data="admin_manage")],
                [InlineKeyboardButton("🔍 Check User Status", callback_data="admin_check")],
                [InlineKeyboardButton("⚙️ Settings", callback_data="admin_settings")],
                [InlineKeyboardButton("← Back to Commands", callback_data="help")]
            ])
            await client.send_message(callback_query.message.chat.id, panel_text, reply_markup=buttons, parse_mode=enums.ParseMode.HTML)
            await callback_query.message.delete()
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
            await client.send_message(callback_query.message.chat.id, Script.ADMIN_MANAGE_TEXT, reply_markup=ADMIN_MANAGE_BUTTONS, parse_mode=enums.ParseMode.HTML)
            await callback_query.message.delete()
        except Exception:
            log.exception("admin_manage_callback error")
    
    # ===== Check User Status Callback =====
    @app.on_callback_query(filters.regex("^admin_check$"))
    async def admin_check_callback(client, callback_query):
        if not is_admin(callback_query.from_user.id):
            await callback_query.answer("❌ Admin access required", show_alert=True)
            return
        
        try:
            await callback_query.answer()
            await client.send_message(callback_query.message.chat.id, "📝 <b>Check User Status</b>\n\nReply with: <code>/checkuser &lt;user_id&gt;</code>", reply_markup=ADMIN_PANEL_BUTTONS, parse_mode=enums.ParseMode.HTML)
            await callback_query.message.delete()
        except Exception:
            log.exception("admin_check_callback error")
    
    # ===== Add Premium Callback =====
    @app.on_callback_query(filters.regex("^admin_add_premium$"))
    async def admin_add_premium_callback(client, callback_query):
        if not is_admin(callback_query.from_user.id):
            await callback_query.answer("❌ Admin access required", show_alert=True)
            return
        
        try:
            await callback_query.answer()
            await client.send_message(callback_query.message.chat.id, "➕ <b>Add Premium User</b>\n\nReply with: <code>/addpremium &lt;user_id&gt; [days]</code>", reply_markup=ADMIN_MANAGE_BUTTONS, parse_mode=enums.ParseMode.HTML)
            await callback_query.message.delete()
        except Exception:
            log.exception("admin_add_premium_callback error")
    
    # ===== Remove Premium Callback =====
    @app.on_callback_query(filters.regex("^admin_remove_premium$"))
    async def admin_remove_premium_callback(client, callback_query):
        if not is_admin(callback_query.from_user.id):
            await callback_query.answer("❌ Admin access required", show_alert=True)
            return
        
        try:
            await callback_query.answer()
            await client.send_message(callback_query.message.chat.id, "➖ <b>Remove Premium User</b>\n\nReply with: <code>/removepremium &lt;user_id&gt;</code>", reply_markup=ADMIN_MANAGE_BUTTONS, parse_mode=enums.ParseMode.HTML)
            await callback_query.message.delete()
        except Exception:
            log.exception("admin_remove_premium_callback error")
    
    # ===== Set Upload Channel =====
    @app.on_message(filters.command("set_upload_channel") & filters.private)
    async def set_upload_channel_cmd(client, message):
        """Set premium upload channel. Usage: /set_upload_channel <channel_id>"""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            args = message.text.split()
            if len(args) < 2:
                current = db.get_premium_upload_channel()
                status = f"<code>{current}</code>" if current else "Not set"
                await message.reply(f"📝 Usage: <code>/set_upload_channel &lt;channel_id&gt;</code>\n\n<b>Current Channel:</b> {status}", parse_mode=enums.ParseMode.HTML)
                return
            
            channel_id = int(args[1])
            
            # Verify bot has access to channel
            try:
                chat = await client.get_chat(channel_id)
                db.set_premium_upload_channel(channel_id)
                await message.reply(f"✅ Upload channel set to: <b>{chat.title}</b> (<code>{channel_id}</code>)", parse_mode=enums.ParseMode.HTML)
                log.info(f"Admin {message.from_user.id} set upload channel to {channel_id}")
            except Exception as e:
                error_msg = "Bot not added to channel" if "Peer id invalid" in str(e) else str(e)
                await message.reply(f"❌ Error: {error_msg}\n\n💡 Make sure the bot is added to the channel as admin", parse_mode=enums.ParseMode.HTML)
        except ValueError:
            await message.reply("❌ Invalid channel ID format", parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("set_upload_channel_cmd error")
    
    # ===== Remove Upload Channel =====
    @app.on_message(filters.command("remove_upload_channel") & filters.private)
    async def remove_upload_channel_cmd(client, message):
        """Remove premium upload channel."""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            current = db.get_premium_upload_channel()
            if not current:
                await message.reply("⚠️ No upload channel is currently set", parse_mode=enums.ParseMode.HTML)
                return
            
            db.set_premium_upload_channel(None)
            await message.reply(f"✅ Upload channel removed", parse_mode=enums.ParseMode.HTML)
            log.info(f"Admin {message.from_user.id} removed upload channel")
        except Exception:
            log.exception("remove_upload_channel_cmd error")
    
    # ===== Admin Settings Callback =====
    @app.on_callback_query(filters.regex("^admin_settings$"))
    async def admin_settings_callback(client, callback_query):
        if not is_admin(callback_query.from_user.id):
            await callback_query.answer("❌ Admin access required", show_alert=True)
            return
        
        try:
            await callback_query.answer()
            await client.send_message(callback_query.message.chat.id, "⚙️ <b>Admin Settings</b>", reply_markup=ADMIN_SETTINGS_BUTTONS, parse_mode=enums.ParseMode.HTML)
            await callback_query.message.delete()
        except Exception:
            log.exception("admin_settings_callback error")
    
    # ===== Auto-Delete Toggle Callback =====
    @app.on_callback_query(filters.regex("^admin_auto_delete$"))
    async def admin_auto_delete_callback(client, callback_query):
        if not is_admin(callback_query.from_user.id):
            await callback_query.answer("❌ Admin access required", show_alert=True)
            return
        
        try:
            current_status = db.is_auto_delete_enabled()
            new_status = not current_status
            db.set_auto_delete(new_status)
            
            status_text = Script.AUTO_DELETE_ON if new_status else Script.AUTO_DELETE_OFF
            await callback_query.answer()
            await callback_query.message.edit_text(status_text, reply_markup=ADMIN_SETTINGS_BUTTONS, parse_mode=enums.ParseMode.HTML)
            log.info(f"Admin {callback_query.from_user.id} toggled auto-delete to {new_status}")
        except Exception:
            log.exception("admin_auto_delete_callback error")
    
    # ===== Auto-Delete Info Command =====
    @app.on_message(filters.command("auto_delete") & filters.private)
    async def auto_delete_info_cmd(client, message):
        """Show auto-delete info."""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            auto_delete_time = db.get_auto_delete_time()
            if auto_delete_time is None:
                status = "❌ <b>Disabled</b> - Files kept after upload"
            else:
                # Convert seconds to readable format
                if auto_delete_time < 60:
                    time_str = f"{auto_delete_time}s"
                elif auto_delete_time < 3600:
                    time_str = f"{auto_delete_time // 60}m"
                else:
                    time_str = f"{auto_delete_time // 3600}h"
                status = f"✅ <b>Enabled</b> - Files deleted after {time_str}"
            
            info_text = f"""<b>⏰ Auto-Delete Settings</b>

{status}

<b>📝 Available Commands:</b>
<code>/set_auto_delete &lt;time&gt;</code> - Set auto-delete time
  Examples: <code>/set_auto_delete 30s</code>, <code>/set_auto_delete 5m</code>, <code>/set_auto_delete 1h</code>

<code>/remove_auto_delete</code> - Disable auto-delete

<b>⏱️ Time Format:</b>
• s = seconds (30s = 30 seconds)
• m = minutes (5m = 5 minutes)  
• h = hours (1h = 1 hour)"""
            await message.reply(info_text, parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("auto_delete_info_cmd error")
    
    # ===== Set Auto-Delete Command =====
    @app.on_message(filters.command("set_auto_delete") & filters.private)
    async def set_auto_delete_cmd(client, message):
        """Set auto-delete time. Usage: /set_auto_delete <time>"""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            args = message.text.split()
            if len(args) < 2:
                await message.reply("📝 Usage: <code>/set_auto_delete &lt;time&gt;</code>\n\n<b>Examples:</b>\n<code>/set_auto_delete 30s</code>\n<code>/set_auto_delete 5m</code>\n<code>/set_auto_delete 1h</code>", parse_mode=enums.ParseMode.HTML)
                return
            
            time_str = args[1].strip()
            
            # Parse time string
            if time_str.endswith('s'):
                seconds = int(time_str[:-1])
            elif time_str.endswith('m'):
                seconds = int(time_str[:-1]) * 60
            elif time_str.endswith('h'):
                seconds = int(time_str[:-1]) * 3600
            else:
                await message.reply("❌ Invalid format. Use: 30s, 5m, or 1h", parse_mode=enums.ParseMode.HTML)
                return
            
            if seconds <= 0:
                await message.reply("❌ Time must be greater than 0", parse_mode=enums.ParseMode.HTML)
                return
            
            db.set_auto_delete_time(seconds)
            
            # Convert back to readable format
            if seconds < 60:
                display_time = f"{seconds}s"
            elif seconds < 3600:
                display_time = f"{seconds // 60}m"
            else:
                display_time = f"{seconds // 3600}h"
            
            await message.reply(f"✅ Auto-delete set to: <b>{display_time}</b>\n\nFiles will be deleted {display_time} after successful upload.", parse_mode=enums.ParseMode.HTML)
            log.info(f"Admin {message.from_user.id} set auto-delete time to {seconds}s")
        except ValueError:
            await message.reply("❌ Invalid time value. Use numbers: 30s, 5m, 1d", parse_mode=enums.ParseMode.HTML)
        except Exception:
            log.exception("set_auto_delete_cmd error")
    
    # ===== Remove Auto-Delete Command =====
    @app.on_message(filters.command("remove_auto_delete") & filters.private)
    async def remove_auto_delete_cmd(client, message):
        """Remove/disable auto-delete."""
        if not is_admin(message.from_user.id):
            await message.reply("❌ Admin access required", parse_mode=enums.ParseMode.HTML)
            return
        
        try:
            db.set_auto_delete_time(None)
            await message.reply("✅ Auto-delete <b>disabled</b>\n\nFiles will be kept after upload.", parse_mode=enums.ParseMode.HTML)
            log.info(f"Admin {message.from_user.id} disabled auto-delete")
        except Exception:
            log.exception("remove_auto_delete_cmd error")
    
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
