from fastapi.responses import JSONResponse
from typing import List
from app.models.face_component import FaceInitialResponse


def create_face_initial_response(success: bool, components: List[dict]) -> JSONResponse:
    """
    Create a JSON response for the initial face endpoint.
    
    Args:
        success: Boolean indicating if the operation was successful
        components: List of facial components with their data
        
    Returns:
        JSONResponse with the formatted data
    """
    response_data = FaceInitialResponse(
        success=success,
        components=components
    )
    
    return JSONResponse(content=response_data.model_dump())