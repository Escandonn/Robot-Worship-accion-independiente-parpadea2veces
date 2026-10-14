from pydantic import BaseModel
from typing import Optional, Dict, Any, Union


class RobotRequest(BaseModel):
    """Model representing the request for robot interpretation."""
    text: str


class RobotResponseData(BaseModel):
    """Model representing the response data for robot interpretation."""
    type: str  # text, image, or animation
    content: str
    resource: Optional[Dict[str, Any]] = None


class RobotResponse(BaseModel):
    """Model representing the response for the robot interpretation endpoint."""
    success: bool
    intent: str
    response: RobotResponseData