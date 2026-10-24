from fastapi.responses import JSONResponse
from app.models.robot_response import RobotResponse


def create_robot_response(success: bool, response_text: str) -> JSONResponse:
    """
    Create a JSON response for the robot interpretation endpoint.
    
    Args:
        success: Boolean indicating if the operation was successful
        response_text: The response text from Groq
        
    Returns:
        JSONResponse with the formatted data
    """
    response_obj = RobotResponse(
        success=success,
        response=response_text
    )
    
    return JSONResponse(content=response_obj.model_dump())