from app.services import groq_service


def test_groq_service_loads_backend_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "GROQ_API_KEY=test-api-key\nGROQ_MODEL=test-model\n",
        encoding="utf-8",
    )
    service_file = tmp_path / "app" / "services" / "groq_service.py"

    monkeypatch.setattr(groq_service, "__file__", str(service_file))
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_MODEL", raising=False)
    monkeypatch.setattr(groq_service, "Groq", lambda api_key: object())

    service = groq_service.GroqService()

    assert service.api_key == "test-api-key"
    assert service.model == "test-model"
    assert service.client is not None
