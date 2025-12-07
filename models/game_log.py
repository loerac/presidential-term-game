from datetime import datetime
from typing import List

from pydantic import BaseModel

from models.results import Result


class GameLog(BaseModel):
    """Log the result of a quiz game"""

    date: datetime
    score: int
    total_questions: int
    duration: int
    results: List[Result]
