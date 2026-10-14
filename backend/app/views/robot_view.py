from fastapi.responses import JSONResponse
from app.models.robot_response import RobotResponse


def create_robot_response(success: bool, intent: str, response_data: dict) -> JSONResponse:
    """
    Create a JSON response for the robot interpretation endpoint.
    
    Args:
        success: Boolean indicating if the operation was successful
        intent: The identified intent from the user's request
        response_data: Dictionary containing the response data (type, content, resource)
        
    Returns:
        JSONResponse with the formatted data
    """
    response_obj = RobotResponse(
        success=success,
        intent=intent,
        response=response_data
    )
    
    return JSONResponse(content=response_obj.model_dump())