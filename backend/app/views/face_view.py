from fastapi.responses import JSONResponse
from typing import List
from app.models.face_component import FaceInitialResponse
from app.models.face_result import FaceResult


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


def create_face_validation_response(result: FaceResult) -> dict:
    return {
        "success": True,
        "is_face": result.is_face,
        "faces_count": result.faces_count,
        "message": result.message,
    }


def create_face_error_response(code: str, message: str) -> dict:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }