from pydantic import BaseModel


class RobotRequest(BaseModel):
    """Model representing the request for robot interpretation."""
    text: str