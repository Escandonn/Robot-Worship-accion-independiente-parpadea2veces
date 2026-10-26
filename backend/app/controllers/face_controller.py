import logging
import os
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from app.services.face_detection_service import (
    FaceDetectionService,
    InvalidImageError,
    UnsupportedImageFormatError,
    get_image_media_type,
)
from app.services.face_service import FaceService
from app.views.face_view import (
    create_face_error_response,
    create_face_initial_response,
    create_face_validation_response,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/face", tags=["face"])
face_service = FaceService()
face_detection_service = FaceDetectionService()

try:
    MAX_IMAGE_SIZE_BYTES = int(
        os.getenv("MAX_IMAGE_SIZE_BYTES", str(5 * 1024 * 1024))
    )
except ValueError as error:
    raise RuntimeError("MAX_IMAGE_SIZE_BYTES must be a positive integer.") from error
if MAX_IMAGE_SIZE_BYTES <= 0:
    raise RuntimeError("MAX_IMAGE_SIZE_BYTES must be a positive integer.")


UPLOAD_CHUNK_SIZE = 64 * 1024


def _error_response(
    status_code: int,
    code: str,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=create_face_error_response(code, message),
    )


async def _read_limited_upload(file: UploadFile) -> Optional[bytes]:
    chunks = []
    total_size = 0
    while True:
        chunk = await file.read(
            min(UPLOAD_CHUNK_SIZE, MAX_IMAGE_SIZE_BYTES + 1 - total_size)
        )
        if not chunk:
            break
        if len(chunk) > MAX_IMAGE_SIZE_BYTES - total_size:
            return None
        chunks.append(chunk)
        total_size += len(chunk)
    return b"".join(chunks)


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


@router.post("/validate", status_code=status.HTTP_200_OK)
async def validate_face(file: Optional[UploadFile] = File(default=None)):
    if file is None:
        return _error_response(
            status.HTTP_400_BAD_REQUEST,
            "FILE_REQUIRED",
            "Debe enviar una imagen en el campo 'file'.",
        )

    if not file.content_type:
        return _error_response(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "UNSUPPORTED_MEDIA_TYPE",
            "Solo se admiten imágenes JPEG, PNG y WebP.",
        )

    declared_media_type = file.content_type.split(";", 1)[0].strip().lower()
    allowed_media_types = {"image/jpeg", "image/png", "image/webp"}
    if declared_media_type not in allowed_media_types:
        return _error_response(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "UNSUPPORTED_MEDIA_TYPE",
            "Solo se admiten imágenes JPEG, PNG y WebP.",
        )

    image_bytes = await _read_limited_upload(file)
    if image_bytes is None:
        return _error_response(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            "FILE_TOO_LARGE",
            "El archivo supera el límite de tamaño permitido.",
        )
    if not image_bytes:
        return _error_response(
            status.HTTP_400_BAD_REQUEST,
            "EMPTY_FILE",
            "El archivo está vacío.",
        )

    try:
        actual_media_type = get_image_media_type(image_bytes)
        if actual_media_type != declared_media_type:
            return _error_response(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "MEDIA_TYPE_MISMATCH",
                "El contenido del archivo no coincide con el tipo declarado.",
            )
        result = face_detection_service.detect(image_bytes)
    except UnsupportedImageFormatError:
        return _error_response(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "UNSUPPORTED_MEDIA_TYPE",
            "El contenido no es una imagen JPEG, PNG o WebP.",
        )
    except InvalidImageError:
        return _error_response(
            status.HTTP_400_BAD_REQUEST,
            "INVALID_IMAGE",
            "El archivo no contiene una imagen válida.",
        )

    return create_face_validation_response(result)