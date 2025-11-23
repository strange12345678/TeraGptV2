# plugins/premium.py
from Theinertbotz.database import db
from script import Script
from config import Config
from pyrogram import enums

class PremiumManager:
    """Manage premium features and limits."""
    
    DAILY_LIMIT_FREE = Config.DAILY_LIMIT
    DAILY_LIMIT_PREMIUM = float('inf')
    
    @staticmethod
    def check_download_limit(user_id) -> tuple[bool, str]:
        """
        Check if user can download.
        Returns: (can_download: bool, message: str)
        """
        tier = db.get_user_tier(user_id)
        
        if tier == "premium":
            return True, "✅ Premium access"
        
        remaining = db.get_remaining_downloads(user_id)
        if remaining > 0:
            return True, f"📊 Downloads today: {db.get_daily_downloads(user_id)}/{Config.DAILY_LIMIT}"
        
        return False, Script.LIMIT_REACHED.format(daily_limit=Config.DAILY_LIMIT)
    
    @staticmethod
    def get_user_status(user_id) -> str:
        """Get formatted user status message."""
        tier = db.get_user_tier(user_id)
        
        if tier == "premium" and db.is_premium_valid(user_id):
            expiry = db.get_premium_expiry(user_id)
            if expiry:
                return f"👑 <b>Premium Member</b>\n\n✨ Unlimited downloads\n🎯 No restrictions\n⏰ Expires: {expiry[:10]}"
            else:
                return "👑 <b>Premium Member</b>\n\n✨ Unlimited downloads\n🎯 No restrictions\n♾️ Permanent"
        
        daily_downloads = db.get_daily_downloads(user_id)
        remaining = db.get_remaining_downloads(user_id)
        
        return f"""🎯 <b>Free Member</b>

📊 <b>Daily Limit:</b>
{daily_downloads}/{Config.DAILY_LIMIT} downloads used
{remaining} remaining

💎 <b>Upgrade to Premium:</b>
• Unlimited downloads
• Unlimited video storage
• Priority support
• No daily limits

<code>/premium</code> - Learn more"""

__all__ = ["PremiumManager"]
