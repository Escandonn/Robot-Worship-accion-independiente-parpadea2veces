import cv2
import numpy as np

from app.models.face_result import FaceResult


class InvalidImageError(ValueError):
    """Raised when the provided bytes cannot be decoded as an image."""


class UnsupportedImageFormatError(ValueError):
    """Raised when the image bytes are not JPEG, PNG, or WebP."""


def get_image_media_type(image_bytes: bytes) -> str:
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        return "image/webp"
    raise UnsupportedImageFormatError("The image format is not supported.")


class FaceDetectionService:
    def __init__(self) -> None:
        cascade_path = (
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.classifier = cv2.CascadeClassifier(cascade_path)
        if self.classifier.empty():
            raise RuntimeError(
                f"Unable to load the Haar Cascade classifier: {cascade_path}"
            )

    def detect(self, image_bytes: bytes) -> FaceResult:
        if not image_bytes:
            raise InvalidImageError("The image file is empty.")

        get_image_media_type(image_bytes)
        encoded_image = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)
        if image is None:
            raise InvalidImageError("The image could not be decoded.")

        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.classifier.detectMultiScale(
            grayscale_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40),
        )
        faces_count = len(faces)
        is_face = faces_count > 0
        message = (
            "Se detectó al menos un rostro."
            if is_face
            else "No se detectaron rostros."
        )
        return FaceResult(
            is_face=is_face,
            faces_count=faces_count,
            message=message,
        )
