from pydantic import BaseModel
from typing import Optional, Dict, Any


class RobotRequest(BaseModel):
    """Model representing the request for robot interpretation."""
    text: str


class GroqInterpretation(BaseModel):
    """Model representing the interpretation from Groq."""
    intent: str
    should_blink: Optional[bool] = None
    count: Optional[int] = None
    response_type: Optional[str] = None  # text, image, or animation
    content: Optional[str] = None
    resource: Optional[Dict[str, Any]] = None


class RobotResponse(BaseModel):
    """Model representing the response for the robot interpretation endpoint."""
    success: bool
    intent: str
    response: Dict[str, Any]