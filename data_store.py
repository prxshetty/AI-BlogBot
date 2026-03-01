import sqlite3
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Optional
from data_models import TopicCollection, SourceContent

class DataStore:
    def __init__(self, db_path: str = "blogbot.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            topic TEXT NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data JSON NOT NULL)
            """)
        
    def save_topic(self, collection: TopicCollection) -> int:
        #Convert dataclass to dict for JSON storage
        data = {
            "topic": collection.topic,
            "keywords": collection.keywords,
            "sources": [
                {
                    "source_type": s.source_type,
                    "source_url": s.source_url,
                    "title": s.title,
                    "content": s.content,
                    "author": s.author,
                    "timestamp": s.timestamp.isoformat() if s.timestamp else None,
                    "metadata": s.metadata
                } for s in collection.sources
            ]
        }
    
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO topics (topic, data) VALUES (?, ?)",
                (collection.topic, json.dumps(data))
            )
            return cursor.lastrowid
        
    def list_topics(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, topic, created_at FROM topics ORDER BY created_at DESC")
            return [{"id": row[0], "topic": row[1], "created_at": row[2]} for row in cursor]

    def get_topic(self, topic_id: int) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT data FROM topics WHERE id = ?", (topic_id,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
