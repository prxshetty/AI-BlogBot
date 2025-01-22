from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

class TaskStatus(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"

@dataclass
class Task:
    id: str
    dependencies: List[str]
    description: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None 