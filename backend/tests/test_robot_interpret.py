import base64
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.controllers import robot_controller
from app.main import app
from app.models.groq_interpretation import GroqInterpretation
from app.models.robot_request import RobotRequest
from app.models.robot_response import RobotFrame, RobotResponseData
from app.repositories.resource_repository import ResourceRepository
from app.services.groq_service import GroqService, INTERPRETATION_SYSTEM_PROMPT


client = TestClient(app)


def test_interpret_robot_command_blink_returns_ordered_base64_frames(monkeypatch):
    def interpret_blink(request: RobotRequest) -> GroqInterpretation:
        assert request.text == "Parpadea dos veces"
        return GroqInterpretation(
            intent="blink",
            content="Parpadeo detectado",
            count=2,
        )

    monkeypatch.setattr(
        robot_controller.groq_service,
        "interpret_text",
        interpret_blink,
    )

    response = client.post(
        "/api/v1/robot/interpret",
        json={"text": "Parpadea dos veces"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["intent"] == "blink"
    assert data["response"]["type"] == "animation"
    assert data["response"]["content"] == "Parpadeo detectado"
    assert data["response"]["count"] == 2
    assert [frame["name"] for frame in data["response"]["frames"]] == [
        "1.png",
        "2.png",
        "3.png",
    ]
    assert all(frame["format"] == "png" for frame in data["response"]["frames"])


def test_interpret_robot_command_text_does_not_load_frames(monkeypatch):
    def interpret_text(request: RobotRequest) -> GroqInterpretation:
        assert request.text == "Hola Risp, ¿cómo estás?"
        return GroqInterpretation(
            intent="text",
            content="¡Hola! Estoy listo para ayudarte.",
        )

    monkeypatch.setattr(
        robot_controller.groq_service,
        "interpret_text",
        interpret_text,
    )

    def unexpected_frame_load():
        pytest.fail("Text responses must not load animation frames")

    monkeypatch.setattr(
        robot_controller.groq_service,
        "get_blink_frames",
        unexpected_frame_load,
    )

    response = client.post(
        "/api/v1/robot/interpret",
        json={"text": "Hola Risp, ¿cómo estás?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "text"
    assert data["response"] == {
        "type": "text",
        "content": "¡Hola! Estoy listo para ayudarte.",
        "frames": [],
    }


def test_interpret_robot_command_rejects_empty_text():
    response = client.post("/api/v1/robot/interpret", json={"text": ""})

    assert response.status_code == 400


def test_groq_interpretation_rejects_unsafe_cycle_counts():
    with pytest.raises(ValueError):
        GroqInterpretation(intent="blink", content="Parpadeo", count=11)

    with pytest.raises(ValueError):
        GroqInterpretation(intent="blink", content="Parpadeo", count=0)


def test_groq_service_requests_and_validates_json_interpretation():
    completion = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content='{"intent":"blink","content":"Parpadeo detectado","count":2}'
                )
            )
        ]
    )
    calls = {}

    class Completions:
        def create(self, **kwargs):
            calls.update(kwargs)
            return completion

    service = GroqService.__new__(GroqService)
    service.client = SimpleNamespace(
        chat=SimpleNamespace(completions=Completions())
    )
    service.model = "test-model"

    interpretation = service.interpret_text(RobotRequest(text="Haz dos parpadeos"))

    assert interpretation.intent == "blink"
    assert interpretation.count == 2
    assert calls["response_format"] == {"type": "json_object"}
    assert calls["messages"][0] == {
        "role": "system",
        "content": INTERPRETATION_SYSTEM_PROMPT,
    }
    assert calls["messages"][1]["content"] == "Haz dos parpadeos"
    assert calls["messages"][0]["role"] == "system"
    assert "WORSHIP" in calls["messages"][0]["content"]
    assert "hechicero creado por Alejandro Escando" in calls["messages"][0]["content"]
    assert "no te describas ni te presentes como un bot" in calls["messages"][0]["content"]
    assert "Cuando me pides que parpadee, tu vida no será la misma" in calls["messages"][0]["content"]
    assert "preguntas" in INTERPRETATION_SYSTEM_PROMPT
    assert "negaciones" in INTERPRETATION_SYSTEM_PROMPT


def test_blink_frames_are_base64_encoded_from_existing_ordered_files():
    service = GroqService.__new__(GroqService)
    service.resource_repository = ResourceRepository()

    frames = service.get_blink_frames()
    source_frames = service.resource_repository.read_blink_frame_bytes()
    assert [frame.name for frame in frames] == ["1.png", "2.png", "3.png"]
    for frame, (source_name, source_bytes) in zip(frames, source_frames):
        assert frame.format == "png"
        assert frame.name == source_name
        assert frame.data == base64.b64encode(source_bytes).decode("ascii")


def test_robot_frame_response_model_validates_cycle_count():
    with pytest.raises(ValueError):
        RobotResponseData(
            type="animation",
            content="Parpadeo detectado",
            frames=[RobotFrame(name="1.png", format="png", data="cG5n")],
            count=11,
        )
