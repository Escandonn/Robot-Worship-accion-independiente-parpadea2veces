from fastapi import APIRouter, HTTPException, status
from app.services.groq_service import GroqService
from app.services.response_service import ResponseService
from app.views.robot_view import create_robot_response
from app.models.robot_request import RobotRequest
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/robot", tags=["robot"])

# Initialize services
groq_service = GroqService()
response_service = ResponseService()


@router.post("/interpret", status_code=status.HTTP_200_OK)
async def interpret_robot_command(request: RobotRequest):
    """
    Interpret a text command for the WORSHIP Mascot Robot.
    
    Args:
        request: RobotRequest containing the text to interpret
        
    Returns:
        JSON response with the interpretation structured for the frontend
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Received interpretation request: {request.text}")
        
        # Step 1: Get interpretation from Groq
        groq_interpretation = groq_service.interpret_text(request)
        logger.info(f"Groq interpretation: {groq_interpretation}")
        
        # Step 2: Validate and prepare the response
        response_data = response_service.prepare_response(groq_interpretation)
        logger.info(f"Prepared response data: {response_data}")
        
        # Step 3: Create and return the final response
        return create_robot_response(
            success=True,
            intent=groq_interpretation.intent,
            response_data=response_data.model_dump()
        )
        
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