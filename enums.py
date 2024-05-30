from enum import Enum
from typing import Any

class BaseEnum(Enum):
    @classmethod
    def list(cls):
        return [t for t in cls]

class ModelType(BaseEnum):
    GPT4o = "gpt-4o"
    GPT35 = "gpt-3.5-turbo"
    
class TurnLimit(BaseEnum):
    TWENTY = 20
    FIVE = 5
    ONE = 1

class GameType(BaseEnum):
    NORMAL = "normal"
    # HEEJIN = "heejin"