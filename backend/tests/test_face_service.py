import base64

import pytest

from app.services.face_detection_service import (
    FaceDetectionService,
    InvalidImageError,
    UnsupportedImageFormatError,
)


PNG_IMAGE = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1Pe"
    "AAAACklEQVQIHWMAAgAABAABDTukuQAAAABJRU5ErkJggg=="
)


class FakeClassifier:
    def __init__(self, detections):
        self.detections = detections
        self.arguments = None

    def detectMultiScale(self, image, **kwargs):
        self.arguments = kwargs
        return self.detections


def make_service(detections):
    service = FaceDetectionService.__new__(FaceDetectionService)
    service.classifier = FakeClassifier(detections)
    return service


def test_detect_reports_one_face():
    service = make_service([(0, 0, 40, 40)])

    result = service.detect(PNG_IMAGE)

    assert result.is_face is True
    assert result.faces_count == 1
    assert result.message == "Se detectó al menos un rostro."
    assert service.classifier.arguments == {
        "scaleFactor": 1.1,
        "minNeighbors": 5,
        "minSize": (40, 40),
    }


def test_detect_reports_multiple_faces():
    service = make_service([(0, 0, 40, 40), (40, 0, 40, 40)])

    result = service.detect(PNG_IMAGE)

    assert result.is_face is True
    assert result.faces_count == 2


def test_detect_reports_no_faces():
    service = make_service(())

    result = service.detect(PNG_IMAGE)

    assert result.is_face is False
    assert result.faces_count == 0
    assert result.message == "No se detectaron rostros."


@pytest.mark.parametrize("image_bytes", [b"", b"not an image"])
def test_detect_rejects_invalid_image_bytes(image_bytes):
    service = make_service(())

    with pytest.raises((InvalidImageError, UnsupportedImageFormatError)):
        service.detect(image_bytes)


def test_classifier_initialization_fails_when_cascade_is_unavailable(
    monkeypatch,
):
    class EmptyClassifier:
        @staticmethod
        def empty():
            return True

    monkeypatch.setattr(
        "app.services.face_detection_service.cv2.CascadeClassifier",
        lambda _: EmptyClassifier(),
    )

    with pytest.raises(RuntimeError, match="Unable to load the Haar Cascade"):
        FaceDetectionService()
