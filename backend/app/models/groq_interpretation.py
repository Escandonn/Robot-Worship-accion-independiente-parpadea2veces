from typing import Literal, Optional

from pydantic import BaseModel, Field


class GroqInterpretation(BaseModel):
    """Validated intent and content returned by Groq."""

    intent: Literal["blink", "text"]
    content: str = Field(min_length=1)
    count: Optional[int] = Field(default=None, ge=1, le=10)
