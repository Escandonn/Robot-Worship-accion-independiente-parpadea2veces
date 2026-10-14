"""
Basic import tests for the robot interpretation services.
These tests verify that the modules can be imported without errors.
They don't test actual functionality since that would require API keys and external services.
"""

def test_groq_service_import():
    """Test that GroqService can be imported."""
    try:
        from app.services.groq_service import GroqService
        assert True  # If we get here, the import succeeded
    except ImportError as e:
        assert False, f"Failed to import GroqService: {e}"

def test_response_service_import():
    """Test that ResponseService can be imported."""
    try:
        from app.services.response_service import ResponseService
        assert True  # If we get here, the import succeeded
    except ImportError as e:
        assert False, f"Failed to import ResponseService: {e}"

def test_resource_repository_import():
    """Test that ResourceRepository can be imported."""
    try:
        from app.repositories.resource_repository import ResourceRepository
        assert True  # If we get here, the import succeeded
    except ImportError as e:
        assert False, f"Failed to import ResourceRepository: {e}"

def test_robot_models_import():
    """Test that robot models can be imported."""
    try:
        from app.models.robot_request import RobotRequest
        from app.models.robot_response import RobotResponse
        from app.models.groq_interpretation import GroqInterpretation
        assert True  # If we get here, the imports succeeded
    except ImportError as e:
        assert False, f"Failed to import robot models: {e}"

def test_robot_controller_import():
    """Test that robot controller can be imported."""
    try:
        from app.controllers.robot_controller import router
        assert True  # If we get here, the import succeeded
    except ImportError as e:
        assert False, f"Failed to import robot controller: {e}"

def test_robot_view_import():
    """Test that robot view can be imported."""
    try:
        from app.views.robot_view import create_robot_response
        assert True  # If we get here, the import succeeded
    except ImportError as e:
        assert False, f"Failed to import robot view: {e}"