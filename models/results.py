from pydantic import BaseModel

from models.presidents import President


class Result(BaseModel):
    """Log the result of a question"""

    president: President
    is_correct: bool
    selected_year: int

    @property
    def correct_year(self) -> str:
        return f"{self.president.start} - {self.president.end}"
