from pydantic import BaseModel
from typing import Optional, Dict, Any


class GroqInterpretation(BaseModel):
    """Model representing the structured interpretation from Groq."""
    intent: str
    response_type: str  # text, image, or animation
    content: str
    resource: Optional[Dict[str, Any]] = None