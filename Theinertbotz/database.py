# Theinertbotz/database.py
import logging
from pymongo import MongoClient
from config import Config

log = logging.getLogger("TeraBoxBot")

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB]
        self.users = self.db["users"]
        self.logs = self.db["logs"]
        self.settings = self.db["settings"]
        log.info("Connected to MongoDB")

    def add_user(self, user_id):
        if not self.users.find_one({"_id": user_id}):
            self.users.insert_one({"_id": user_id})
            return True
        return False

    def is_user(self, user_id):
        return self.users.find_one({"_id": user_id}) is not None

    def add_log(self, user_id, file_name, meta=None):
        doc = {"user_id": user_id, "file": file_name}
        if meta:
            doc.update(meta)
        self.logs.insert_one(doc)
    
    def get_user_rename_setting(self, user_id):
        """Get user's auto-rename setting. Returns pattern or None if not set."""
        user = self.users.find_one({"_id": user_id})
        if user:
            return user.get("auto_rename", "timestamp")  # Default to timestamp
        return "timestamp"
    
    def set_user_rename_setting(self, user_id, pattern):
        """Set user's auto-rename pattern. pattern: 'timestamp', 'datetime', custom, or '' (disabled)."""
        self.users.update_one({"_id": user_id}, {"$set": {"auto_rename": pattern}}, upsert=True)
        return True
    
    def get_custom_rename_pattern(self, user_id):
        """Get user's custom rename pattern if set."""
        user = self.users.find_one({"_id": user_id})
        if user:
            return user.get("custom_rename_pattern", None)
        return None
    
    def set_custom_rename_pattern(self, user_id, pattern):
        """Set custom rename pattern with variables."""
        self.users.update_one({"_id": user_id}, {"$set": {"custom_rename_pattern": pattern, "auto_rename": pattern}}, upsert=True)
        return True
    
    # ===== Premium System Methods =====
    def get_user_tier(self, user_id):
        """Get user's tier: 'free' or 'premium'. Defaults to 'free'."""
        user = self.users.find_one({"_id": user_id})
        if user:
            return user.get("tier", "free")
        return "free"
    
    def set_user_tier(self, user_id, tier):
        """Set user's tier to 'free' or 'premium'."""
        self.users.update_one({"_id": user_id}, {"$set": {"tier": tier}}, upsert=True)
        return True
    
    def increment_daily_downloads(self, user_id):
        """Increment user's daily download count."""
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"downloads_{today}"
        self.users.update_one({"_id": user_id}, {"$inc": {key: 1}}, upsert=True)
        return True
    
    def get_daily_downloads(self, user_id):
        """Get user's download count for today."""
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"downloads_{today}"
        user = self.users.find_one({"_id": user_id})
        if user:
            return user.get(key, 0)
        return 0
    
    def get_remaining_downloads(self, user_id):
        """Get remaining downloads for today (for free users)."""
        tier = self.get_user_tier(user_id)
        if tier == "premium":
            return float('inf')  # Unlimited
        daily_limit = 5
        used = self.get_daily_downloads(user_id)
        remaining = max(0, daily_limit - used)
        return remaining
    
    def can_download(self, user_id):
        """Check if user can download (respects daily limits)."""
        tier = self.get_user_tier(user_id)
        if tier == "premium" and self.is_premium_valid(user_id):
            return True
        remaining = self.get_remaining_downloads(user_id)
        return remaining > 0
    
    def set_premium_expiry(self, user_id, days):
        """Set premium expiry date. Days from now."""
        from datetime import datetime, timedelta
        if days is None or days == 0:
            # Permanent premium
            expiry = None
        else:
            expiry = (datetime.now() + timedelta(days=days)).isoformat()
        self.users.update_one({"_id": user_id}, {"$set": {"tier": "premium", "premium_expiry": expiry}}, upsert=True)
        return True
    
    def is_premium_valid(self, user_id):
        """Check if user's premium is still valid (not expired)."""
        from datetime import datetime
        user = self.users.find_one({"_id": user_id})
        if not user or user.get("tier") != "premium":
            return False
        
        expiry = user.get("premium_expiry")
        if expiry is None:
            return True  # Permanent premium
        
        expiry_dt = datetime.fromisoformat(expiry)
        if datetime.now() > expiry_dt:
            # Premium has expired, downgrade to free
            self.set_user_tier(user_id, "free")
            return False
        
        return True
    
    def get_premium_expiry(self, user_id):
        """Get premium expiry date for user."""
        user = self.users.find_one({"_id": user_id})
        if user:
            return user.get("premium_expiry")
        return None
    
    def set_premium_upload_channel(self, channel_id):
        """Set the premium upload channel ID. Use None to remove."""
        if channel_id is None:
            self.settings.update_one({"_id": "premium_upload_channel"}, {"$set": {"channel_id": None}}, upsert=True)
        else:
            self.settings.update_one({"_id": "premium_upload_channel"}, {"$set": {"channel_id": channel_id}}, upsert=True)
        return True
    
    def get_premium_upload_channel(self):
        """Get the premium upload channel ID."""
        doc = self.settings.find_one({"_id": "premium_upload_channel"})
        if doc:
            return doc.get("channel_id")
        return None
    
    def set_auto_delete(self, enabled):
        """Set auto-delete status."""
        self.settings.update_one({"_id": "auto_delete"}, {"$set": {"enabled": enabled}}, upsert=True)
        return True
    
    def is_auto_delete_enabled(self):
        """Get auto-delete status."""
        doc = self.settings.find_one({"_id": "auto_delete"})
        if doc:
            return doc.get("enabled", True)  # Default to True
        return True
    
    def get_total_downloads(self, user_id):
        """Get total number of files downloaded by user (all time)."""
        total = self.logs.count_documents({"user_id": user_id})
        return total
    
    def get_success_rate(self):
        """Get overall success rate (percentage of successful operations)."""
        total_logs = self.logs.count_documents({})
        if total_logs == 0:
            return 100
        success_logs = self.logs.count_documents({"status": "success"})
        return int((success_logs / total_logs) * 100)

db = Database()
