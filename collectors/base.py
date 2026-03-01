from abc import ABC, abstractmethod
from typing import List
from data_models import SourceContent

class BaseCollector(ABC):
    @abstractmethod
    async def collect(self, query: str, **kwargs) -> List[SourceContent]:
        pass
    