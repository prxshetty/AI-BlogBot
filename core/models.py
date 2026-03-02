from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict

@dataclass
class SourceContent:
    source_type: str
    source_url: str
    title: str
    content: str
    author: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class TopicCollection:
    topic: str
    keywords: List[str]
    sources: List[SourceContent] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)