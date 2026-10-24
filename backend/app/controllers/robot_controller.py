from fastapi import APIRouter, HTTPException, status
from app.services.groq_service import GroqService
from app.views.robot_view import create_robot_response
from app.models.robot_request import RobotRequest
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/robot", tags=["robot"])

# Initialize services
groq_service = GroqService()


@router.post("/interpret", status_code=status.HTTP_200_OK)
async def interpret_robot_command(request: RobotRequest):
    """
    Interpret a text command using Groq API.
    
    Args:
        request: RobotRequest containing the text to interpret
        
    Returns:
        JSON response with the Groq response
    """
    try:
        logger.info(f"Received interpretation request: {request.text}")
        
        response_text = groq_service.interpret_text(request)
        logger.info(f"Groq response: {response_text}")
        
        return create_robot_response(success=True, response_text=response_text)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error processing interpretation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing the request with the AI service"
        )