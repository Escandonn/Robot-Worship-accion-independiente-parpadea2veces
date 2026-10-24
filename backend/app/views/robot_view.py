from fastapi.responses import JSONResponse
from app.models.robot_response import RobotResponse


def create_robot_response(response: RobotResponse) -> JSONResponse:
    """
    Create a JSON response for the robot interpretation endpoint.
    
    Args:
        response: Validated robot response data
        
    Returns:
        JSONResponse with the formatted data
    """
    return JSONResponse(content=response.model_dump(exclude_none=True))