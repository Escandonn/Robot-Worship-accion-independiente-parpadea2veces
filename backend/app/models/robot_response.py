from pydantic import BaseModel


class RobotResponse(BaseModel):
    """Model representing the response for the robot interpretation endpoint."""
    success: bool
    response: str