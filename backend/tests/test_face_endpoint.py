import base64

from fastapi.testclient import TestClient

from app.main import app
from app.models.face_result import FaceResult
from app.controllers import face_controller


client = TestClient(app)
PNG_IMAGE = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/"
    "l9sAAAAASUVORK5CYII="
)


def test_validate_face_returns_success_contract(monkeypatch):
    monkeypatch.setattr(
        face_controller.face_detection_service,
        "detect",
        lambda _: FaceResult(True, 1, "Se detectó al menos un rostro."),
    )

    response = client.post(
        "/api/v1/face/validate",
        files={"file": ("test.png", PNG_IMAGE, "image/png")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "is_face": True,
        "faces_count": 1,
        "message": "Se detectó al menos un rostro.",
    }


def test_validate_face_returns_negative_detection(monkeypatch):
    monkeypatch.setattr(
        face_controller.face_detection_service,
        "detect",
        lambda _: FaceResult(False, 0, "No se detectaron rostros."),
    )

    response = client.post(
        "/api/v1/face/validate",
        files={"file": ("test.png", PNG_IMAGE, "image/png")},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["is_face"] is False
    assert response.json()["faces_count"] == 0


def test_validate_face_requires_file():
    response = client.post("/api/v1/face/validate")

    assert response.status_code == 400
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "FILE_REQUIRED"


def test_validate_face_rejects_empty_file():
    response = client.post(
        "/api/v1/face/validate",
        files={"file": ("empty.png", b"", "image/png")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "EMPTY_FILE"


def test_validate_face_rejects_corrupt_image():
    response = client.post(
        "/api/v1/face/validate",
        files={
            "file": (
                "corrupt.png",
                b"\x89PNG\r\n\x1a\ncorrupt image bytes",
                "image/png",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_IMAGE"


def test_validate_face_rejects_unsupported_media_type():
    response = client.post(
        "/api/v1/face/validate",
        files={"file": ("image.gif", b"GIF89a", "image/gif")},
    )

    assert response.status_code == 415
    assert response.json()["error"]["code"] == "UNSUPPORTED_MEDIA_TYPE"


def test_validate_face_rejects_declared_and_actual_type_mismatch():
    response = client.post(
        "/api/v1/face/validate",
        files={"file": ("image.jpg", PNG_IMAGE, "image/jpeg")},
    )

    assert response.status_code == 415
    assert response.json()["error"]["code"] == "MEDIA_TYPE_MISMATCH"


def test_validate_face_rejects_files_over_configured_limit(monkeypatch):
    monkeypatch.setattr(face_controller, "MAX_IMAGE_SIZE_BYTES", 8)

    response = client.post(
        "/api/v1/face/validate",
        files={"file": ("large.png", PNG_IMAGE, "image/png")},
    )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "FILE_TOO_LARGE"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
