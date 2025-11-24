# Theinertbotz/secondary_download.py
import subprocess
import os
import asyncio
import time
import logging
import re
from pyrogram import enums
from config import Config
from Theinertbotz.processing import ProgressManager
from Theinertbotz.rename import auto_rename_file
from Theinertbotz.database import db

log = logging.getLogger("TeraBoxBot")

os.makedirs(getattr(Config, "DOWNLOAD_DIR", "downloads"), exist_ok=True)


async def download_hls_video(client, message, m3u8_url: str, bot_username: str, filename: str = None):
    """
    Download HLS video (m3u8) using ffmpeg.
    Returns (filepath, safe_filename) on success.
    
    Args:
        client: pyrogram client
        message: incoming pyrogram Message
        m3u8_url: Direct m3u8 playlist URL
        bot_username: Bot username for display
        filename: Optional filename override
    """
    try:
        status_msg = await message.reply("⏳ sᴛᴀʀᴛɪɴɢ ʜʟs ᴅᴏᴡɴʟᴏᴀᴅ...", quote=True)
        await asyncio.sleep(2)
    except Exception:
        try:
            status_msg = await client.send_message(message.chat.id, "⏳ sᴛᴀʀᴛɪɴɢ ʜʟs ᴅᴏᴡɴʟᴏᴀᴅ...")
            await asyncio.sleep(2)
        except Exception:
            status_msg = None

    async def edit_coro(text, parse_mode=enums.ParseMode.HTML):
        if status_msg:
            try:
                await status_msg.edit_text(text, parse_mode=parse_mode)
            except Exception:
                pass

    pm = ProgressManager(edit_coro, bot_username=bot_username, kind="download")

    # Generate filename if not provided
    if not filename:
        timestamp = int(time.time())
        filename = f"video_{timestamp}.mp4"
    
    # Store original filename for rename
    original_filename = filename
    
    # Sanitize filename
    safe_fn = "".join(c for c in filename if c.isalnum() or c in " .-_()[]{}%").strip()
    if not safe_fn or safe_fn.lower().endswith(('.m3u8',)):
        safe_fn = f"video_{int(time.time())}.mp4"
    
    # Ensure .mp4 extension
    if not safe_fn.lower().endswith('.mp4'):
        safe_fn += ".mp4"
    
    filepath = os.path.join(getattr(Config, "DOWNLOAD_DIR", "downloads"), safe_fn)
    
    # Get user info for auto-rename
    user_id = getattr(message.from_user, "id", None) if hasattr(message, "from_user") else None
    username = getattr(message.from_user, "username", "unknown") if hasattr(message, "from_user") else "unknown"
    
    if user_id:
        rename_pattern = db.get_user_rename_setting(user_id)
    else:
        rename_pattern = getattr(Config, "AUTO_RENAME", "")

    try:
        await edit_coro("⏳ <b>ꜰᴇᴛᴄʜɪɴɢ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍ...</b>")
        
        # Get video duration using ffprobe for accurate progress
        total_duration = 0
        try:
            probe_cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                m3u8_url
            ]
            probe_result = await asyncio.create_subprocess_exec(
                *probe_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await asyncio.wait_for(probe_result.communicate(), timeout=15)
            if stdout:
                total_duration = float(stdout.decode().strip())
                log.info(f"Video duration: {total_duration:.1f} seconds")
        except Exception as e:
            log.warning(f"Could not get video duration: {e}")
        
        # Build ffmpeg command with progress output
        # -c copy = stream copy without re-encoding (fastest)
        # -bsf:a aac_adtstoasc = convert AAC if needed
        # -progress pipe:1 = output progress to stdout
        cmd = [
            "ffmpeg",
            "-i", m3u8_url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-y",  # Overwrite output file
            "-progress", "pipe:1",
            "-loglevel", "error",
            filepath
        ]
        
        log.info(f"Running ffmpeg command for m3u8: {' '.join(cmd)}")
        
        # Run ffmpeg with progress tracking
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Track progress by parsing ffmpeg output and monitoring file size
        start_time = time.time()
        last_update = start_time
        last_bytes = 0
        current_time_us = 0
        total_duration_us = int(total_duration * 1000000) if total_duration > 0 else 0
        progress_end_detected = False
        
        # Read ffmpeg progress output line by line
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            
            line_str = line.decode().strip()
            
            # Parse time position from ffmpeg
            if line_str.startswith("out_time_us="):
                try:
                    current_time_us = int(line_str.split("=")[1])
                except:
                    pass
            
            # Detect progress end marker and do final update immediately
            if line_str.startswith("progress=end"):
                progress_end_detected = True
                # Immediate final update on progress=end
                try:
                    if os.path.exists(filepath):
                        final_bytes = os.path.getsize(filepath)
                        elapsed_total = time.time() - start_time
                        avg_speed = final_bytes / elapsed_total if elapsed_total > 0 else 0
                        await pm.update(final_bytes, final_bytes, avg_speed)
                except Exception as e:
                    log.debug(f"Final progress update on end marker failed: {e}")
            
            # Update progress periodically
            now = time.time()
            if now - last_update >= 1.0:
                try:
                    # Get current file size
                    if os.path.exists(filepath):
                        current_bytes = os.path.getsize(filepath)
                    else:
                        current_bytes = 0
                    
                    # Calculate speed based on file size growth
                    elapsed = now - last_update
                    speed = (current_bytes - last_bytes) / elapsed if elapsed > 0 else 0
                    
                    # Choose progress mode based on available data
                    if total_duration_us > 0 and current_time_us > 0 and current_bytes > 0:
                        # Mode 1: Duration available - estimate total based on bitrate
                        time_ratio = min(current_time_us / total_duration_us, 1.0)  # Cap at 100%
                        if time_ratio > 0.05:  # Only after 5% to avoid early spikes
                            estimated_total = int(current_bytes / time_ratio)
                            # Smooth the estimate to avoid jumps
                            estimated_total = max(estimated_total, current_bytes)
                            processed = current_bytes
                            total = estimated_total
                        else:
                            # Too early for reliable estimate
                            processed = current_bytes
                            total = 0
                    else:
                        # Mode 2: No duration - show unknown total UI
                        processed = current_bytes
                        total = 0
                    
                    # Update ProgressManager
                    await pm.update(processed, total, speed)
                    
                    last_update = now
                    last_bytes = current_bytes
                except Exception as e:
                    log.debug(f"Progress update error: {e}")
        
        # Wait for process to complete
        await process.wait()
        
        if process.returncode != 0:
            stderr = await process.stderr.read()
            error_out = stderr.decode() if stderr else "Unknown error"
            log.error(f"ffmpeg failed: {error_out}")
            await edit_coro(f"❌ <b>ꜰꜰᴍᴘᴇɢ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ</b>\n\n{error_out[:200]}")
            return None, None
        
        if not os.path.exists(filepath):
            await edit_coro("❌ <b>ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ - ɴᴏ ꜰɪʟᴇ ᴄʀᴇᴀᴛᴇᴅ</b>")
            return None, None
        
        # Final progress update to show 100% completion (if not already done on progress=end)
        if not progress_end_detected:
            final_size = os.path.getsize(filepath)
            total_time = time.time() - start_time
            avg_speed = final_size / total_time if total_time > 0 else 0
            try:
                await pm.update(final_size, final_size, avg_speed)
            except Exception:
                log.debug("Final progress update failed")
        
        # Apply auto-rename if enabled
        if rename_pattern and os.path.exists(filepath):
            file_size_bytes = os.path.getsize(filepath)
            # Convert bytes to human readable format
            for unit in ['B', 'KB', 'MB', 'GB']:
                if file_size_bytes < 1024:
                    file_size_str = f"{file_size_bytes:.1f}{unit}"
                    break
                file_size_bytes /= 1024
            else:
                file_size_str = f"{file_size_bytes:.1f}TB"
            
            # Prepare variables with actual file size
            variables = {
                "file_size": file_size_str,
                "username": username or str(user_id),
                "user_id": str(user_id) if user_id else "unknown"
            }
            # Pass original_filename to preserve variable replacement
            new_fn = auto_rename_file(original_filename, rename_pattern, variables)
            if new_fn != safe_fn:
                new_filepath = os.path.join(getattr(Config, "DOWNLOAD_DIR", "downloads"), new_fn)
                try:
                    os.rename(filepath, new_filepath)
                    filepath = new_filepath
                    safe_fn = new_fn
                    log.info(f"Renamed file: {safe_fn}")
                except Exception as e:
                    log.warning(f"Failed to rename file: {e}")
        
        file_size = os.path.getsize(filepath)
        await edit_coro(f"✅ <b>ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ!</b>\n<code>{safe_fn}</code>\n🗂️ {file_size / (1024**2):.2f} MB")
        
        # Auto-delete status message after 5 seconds
        await asyncio.sleep(5)
        try:
            if status_msg:
                await status_msg.delete()
        except:
            pass
        
        log.info(f"HLS download complete: {filepath} ({file_size} bytes)")
        return filepath, safe_fn

    except asyncio.CancelledError:
        log.warning(f"Download cancelled: {filepath}")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        await edit_coro("❌ <b>ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ</b>")
        return None, None

    except Exception as e:
        log.error(f"HLS download error: {e}", exc_info=True)
        await edit_coro(f"❌ <b>ᴅᴏᴡɴʟᴏᴀᴅ ᴇʀʀᴏʀ:</b>\n<code>{str(e)[:100]}</code>")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        return None, None
