from pymongo import MongoClient
from config import Config, logger

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.users = None
        self.downloads = None
        self.errors = None
        try:
            if Config.MONGO_URI:
                self.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
                self.db = self.client[Config.MONGO_DB]
                self.users = self.db["users"]
                self.downloads = self.db["downloads"]
                self.errors = self.db["errors"]
                logger.info("Connected to MongoDB")
        except Exception as e:
            logger.warning(f"MongoDB init failed: {e}")
            self.client = None

    def add_user(self, user_id: int, name: str = None):
        if not self.client:
            return
        if not self.users.find_one({"_id": user_id}):
            self.users.insert_one({"_id": user_id, "name": name})

    def log_download(self, user_id: int, file_name: str, size: str = None):
        if not self.client:
            return
        self.downloads.insert_one({"user_id": user_id, "file_name": file_name, "size": size})

    def log_error(self, user_id: int, error_text: str):
        if not self.client:
            return
        self.errors.insert_one({"user_id": user_id, "error": error_text})

db = Database()
