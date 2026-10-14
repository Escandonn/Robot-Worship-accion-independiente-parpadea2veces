from fastapi import APIRouter, HTTPException, status
from app.services.face_service import FaceService
from app.views.face_view import create_face_initial_response
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/face", tags=["face"])

# Initialize service
face_service = FaceService()


@router.get("/initial", status_code=status.HTTP_200_OK)
async def get_initial_face():
    """
    Get the initial face components for the WORSHIP Mascot Robot.
    
    Returns:
        JSON response with facial components encoded in Base64
        
    Raises:
        HTTPException: If there's an error accessing or processing the files
    """
    try:
        # Get components from service
        components_data = face_service.get_initial_face_components()
        
        # Create and return response
        return create_face_initial_response(
            success=True,
            components=components_data
        )
        
    except FileNotFoundError as e:
        logger.error(f"File not found error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more facial component files are missing"
        )
    except IOError as e:
        logger.error(f"IO error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error reading facial component files"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing facial components"
        )