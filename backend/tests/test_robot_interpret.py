from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

def test_interpret_robot_command_success():
    """Test that the endpoint returns successfully with a valid interpretation."""
    response = client.post(
        "/api/v1/robot/interpret",
        json={"text": "Hola Risp, ¿cómo estás?"}
    )
    
    # Check that the request was successful
    assert response.status_code == 200
    
    # Parse JSON response
    data = response.json()
    
    # Check response structure
    assert data["success"] == True
    assert "intent" in data
    assert "response" in data
    assert isinstance(data["response"], dict)
    
    # Check response has required fields
    assert "type" in data["response"]
    assert "content" in data["response"]
    assert "resource" in data["response"]  # Can be null
    
    # Check that response type is valid
    assert data["response"]["type"] in ["text", "image", "animation"]
    
    # Check that content is not empty
    assert len(data["response"]["content"].strip()) > 0

def test_interpret_robot_command_blink():
    """Test that the endpoint correctly interprets a blink command."""
    response = client.post(
        "/api/v1/robot/interpret",
        json={"text": "Parpadea dos veces"}
    )
    
    # Check that the request was successful
    assert response.status_code == 200
    
    # Parse JSON response
    data = response.json()
    
    # Check response structure
    assert data["success"] == True
    assert data["intent"] == "blink"
    assert data["response"]["type"] == "animation"
    assert "Voy a parpadear" in data["response"]["content"] or "parpadear" in data["response"]["content"]
    
    # Check that resource contains blink information
    assert data["response"]["resource"] is not None
    assert data["response"]["resource"]["name"] == "blink"
    assert "parameters" in data["response"]["resource"]
    assert "count" in data["response"]["resource"]["parameters"]

def test_interpret_robot_command_empty_text():
    """Test that the endpoint handles empty text appropriately."""
    response = client.post(
        "/api/v1/robot/interpret",
        json={"text": ""}
    )
    
    # Should return a validation error
    assert response.status_code == 400  # Bad Request

def test_interpret_robot_command_response_structure():
    """Test that the response matches the expected structure."""
    response = client.post(
        "/api/v1/robot/interpret",
        json={"text": "Cualquier texto para probar"}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Check top-level keys
    assert set(data.keys()) == {"success", "intent", "response"}
    
    # Check success is boolean
    assert isinstance(data["success"], bool)
    
    # Check intent is string
    assert isinstance(data["intent"], str)
    
    # Check response structure
    assert set(data["response"].keys()) == {"type", "content", "resource"}
    assert isinstance(data["response"]["type"], str)
    assert isinstance(data["response"]["content"], str)
    # resource can be null or a dict
    assert data["response"]["resource"] is None or isinstance(data["response"]["resource"], dict)