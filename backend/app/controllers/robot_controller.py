from fastapi import APIRouter, HTTPException, status
from app.services.groq_service import GroqService
from app.views.robot_view import create_robot_response
from app.models.robot_request import RobotRequest
from app.models.robot_response import RobotResponse, RobotResponseData
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
        
        interpretation = groq_service.interpret_text(request)

        if interpretation.intent == "blink":
            response = RobotResponse(
                success=True,
                intent="blink",
                response=RobotResponseData(
                    type="animation",
                    content="Parpadeo detectado",
                    frames=groq_service.get_blink_frames(),
                    count=interpretation.count,
                ),
            )
        else:
            response = RobotResponse(
                success=True,
                intent="text",
                response=RobotResponseData(
                    type="text",
                    content=interpretation.content,
                    frames=[],
                ),
            )

        return create_robot_response(response)
        
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