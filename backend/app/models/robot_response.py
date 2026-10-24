from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class RobotFrame(BaseModel):
    """Base64-encoded PNG frame for a robot animation."""

    name: str
    format: Literal["png"]
    data: str = Field(min_length=1)


class RobotResponseData(BaseModel):
    """Response content returned by the robot interpretation endpoint."""

    type: Literal["text", "animation"]
    content: str = Field(min_length=1)
    frames: list[RobotFrame] = Field(default_factory=list)
    count: Optional[int] = Field(default=None, ge=1, le=10)

    @model_validator(mode="after")
    def validate_response_shape(self):
        if self.type == "animation":
            if self.count is None:
                raise ValueError("Animation responses must include a cycle count")
            if [frame.name for frame in self.frames] != ["1.png", "2.png", "3.png"]:
                raise ValueError("Animation responses must include the three ordered PNG frames")
        elif self.frames or self.count is not None:
            raise ValueError("Text responses cannot include animation frames or a cycle count")
        return self


class RobotResponse(BaseModel):
    """Model representing the response for the robot interpretation endpoint."""
    success: bool
    intent: Literal["text", "blink"]
    response: RobotResponseData

    @model_validator(mode="after")
    def validate_intent_matches_response(self):
        expected_type = "animation" if self.intent == "blink" else "text"
        if self.response.type != expected_type:
            raise ValueError("Response type must match the interpreted intent")
        return self