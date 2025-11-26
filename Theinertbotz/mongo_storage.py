"""
MongoDB-backed storage for Pyrogram sessions.
Replaces SQLite storage for ephemeral container deployments.
"""

import logging
from pyrogram.storage import Storage
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

log = logging.getLogger("TeraBoxBot")

class MongoStorage(Storage):
    """Custom MongoDB storage backend for Pyrogram sessions."""
    
    def __init__(self, mongo_uri: str, db_name: str = "teraboxbot", session_name: str = "TeraBoxBot"):
        self.session_name = session_name
        self.db_name = db_name
        self.mongo_uri = mongo_uri
        self.client = None
        self.db = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.collection = self.db['pyrogram_sessions']
            self.collection.create_index("session_name")
            log.info(f"✅ Connected to MongoDB for session storage")
        except ServerSelectionTimeoutError:
            log.error("❌ Failed to connect to MongoDB")
            raise
    
    async def open(self):
        """Open storage connection."""
        pass
    
    async def close(self):
        """Close storage connection."""
        if self.client:
            self.client.close()
    
    async def exists(self) -> bool:
        """Check if session exists."""
        if not self.collection:
            return False
        doc = self.collection.find_one({"session_name": self.session_name})
        return doc is not None
    
    async def save(self, name: str, key: str, value: bytes, file_reference: bytes = None):
        """Save session data to MongoDB."""
        if not self.collection:
            return
        
        self.collection.update_one(
            {"session_name": self.session_name},
            {
                "$set": {
                    "session_name": self.session_name,
                    name: {
                        "key": key,
                        "value": value.hex() if isinstance(value, bytes) else value,
                        "file_reference": file_reference.hex() if file_reference else None
                    }
                }
            },
            upsert=True
        )
    
    async def load(self, name: str, key: str, file_reference: bytes = None) -> bytes:
        """Load session data from MongoDB."""
        if not self.collection:
            return None
        
        doc = self.collection.find_one({"session_name": self.session_name})
        if not doc or name not in doc:
            return None
        
        data = doc[name]
        if data.get("key") == key:
            value = data.get("value")
            if isinstance(value, str):
                try:
                    return bytes.fromhex(value)
                except:
                    return value.encode() if isinstance(value, str) else value
            return value
        
        return None
    
    async def delete(self):
        """Delete session from MongoDB."""
        if self.collection:
            self.collection.delete_one({"session_name": self.session_name})
    
    async def update_peers(self, peers: dict):
        """Update peers cache in MongoDB."""
        if not self.collection:
            return
        
        self.collection.update_one(
            {"session_name": self.session_name},
            {"$set": {"peers_cache": peers}},
            upsert=True
        )
    
    async def get_peers(self, *args, **kwargs) -> dict:
        """Get peers cache from MongoDB."""
        if not self.collection:
            return {}
        
        doc = self.collection.find_one({"session_name": self.session_name})
        return doc.get("peers_cache", {}) if doc else {}
