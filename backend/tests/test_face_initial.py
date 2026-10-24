import base64
import os
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

def test_get_initial_face_success():
    """Test that the endpoint returns successfully with all components."""
    response = client.get("/api/v1/face/initial")
    
    # Check that the request was successful
    assert response.status_code == 200
    
    # Parse JSON response
    data = response.json()
    
    # Check response structure
    assert data["success"] == True
    assert "components" in data
    assert isinstance(data["components"], list)
    assert len(data["components"]) == 4  # We have 4 components
    
    # Check each component has required fields
    expected_components = ["boca", "nariz", "ojo-derecho", "ojo-izquierdo"]
    found_components = []
    
    for component in data["components"]:
        assert "name" in component
        assert "type" in component
        assert "data" in component
        
        assert component["type"] == "image/png"
        found_components.append(component["name"])
        
        # Verify that data is valid Base64
        try:
            base64.b64decode(component["data"])
        except Exception:
            assert False, f"Component {component['name']} data is not valid Base64"
    
    # Check that we got all expected components
    assert set(found_components) == set(expected_components)

def test_get_initial_face_component_data_not_empty():
    """Test that each component has non-empty data."""
    response = client.get("/api/v1/face/initial")
    assert response.status_code == 200
    
    data = response.json()
    
    for component in data["components"]:
        assert len(component["data"]) > 0, f"Component {component['name']} has empty data"

def test_get_initial_face_response_structure():
    """Test that the response matches the expected structure."""
    response = client.get("/api/v1/face/initial")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check top-level keys
    assert set(data.keys()) == {"success", "components"}
    
    # Check success is boolean
    assert isinstance(data["success"], bool)
    
    # Check components is a list
    assert isinstance(data["components"], list)
    
    # Check each component structure
    for component in data["components"]:
        assert set(component.keys()) == {"name", "type", "data"}
        assert isinstance(component["name"], str)
        assert isinstance(component["type"], str)
        assert isinstance(component["data"], str)


def test_deployed_frontend_can_access_face_and_interpret_endpoints():
    origin = "https://robot-worship-accion-independiente-sepia.vercel.app"

    face_response = client.get(
        "/api/v1/face/initial",
        headers={"Origin": origin},
    )
    assert face_response.status_code == 200
    assert face_response.headers["access-control-allow-origin"] == origin

    preflight_response = client.options(
        "/api/v1/robot/interpret",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert preflight_response.status_code == 200
    assert preflight_response.headers["access-control-allow-origin"] == origin
    assert "POST" in preflight_response.headers["access-control-allow-methods"]
    assert "content-type" in preflight_response.headers["access-control-allow-headers"]