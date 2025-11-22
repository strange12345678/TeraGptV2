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
        """Set user's auto-rename pattern. pattern: 'timestamp', 'datetime', or '' (disabled)."""
        self.users.update_one({"_id": user_id}, {"$set": {"auto_rename": pattern}}, upsert=True)
        return True

db = Database()
