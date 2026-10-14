from pydantic import BaseModel
from typing import List, Optional


class FaceComponent(BaseModel):
    """Model representing a facial component."""
    name: str
    type: str
    data: str  # Base64 encoded image data


class FaceInitialResponse(BaseModel):
    """Model representing the response for the initial face endpoint."""
    success: bool
    components: List[FaceComponent]