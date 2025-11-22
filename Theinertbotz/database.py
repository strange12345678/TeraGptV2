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
        if tier == "premium":
            return True
        remaining = self.get_remaining_downloads(user_id)
        return remaining > 0

db = Database()
