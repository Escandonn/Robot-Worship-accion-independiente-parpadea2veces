from typing import Dict, Any, Optional
from app.models.groq_interpretation import GroqInterpretation
from app.models.robot_response import RobotResponseData
from app.repositories.resource_repository import ResourceRepository
import logging

# Set up logger
logger = logging.getLogger(__name__)


class ResponseService:
    """Service for validating interpretations and preparing responses."""
    
    def __init__(self):
        """Initialize the response service with a resource repository."""
        self.repository = ResourceRepository()
        # Define allowed intents
        self.allowed_intents = ["greeting", "blink", "show_image", "unknown"]
        # Define allowed response types
        self.allowed_response_types = ["text", "image", "animation"]
    
    def prepare_response(self, interpretation: GroqInterpretation) -> RobotResponseData:
        """
        Validate the interpretation and prepare the final response.
        
        Args:
            interpretation: GroqInterpretation object from Groq service
            
        Returns:
            RobotResponseData object ready to be sent to the frontend
            
        Raises:
            ValueError: If the interpretation is invalid or contains disallowed values
        """
        # Validate intent
        if interpretation.intent not in self.allowed_intents:
            logger.warning(f"Intent '{interpretation.intent}' not in allowed intents. Using 'unknown'.")
            interpretation.intent = "unknown"
        
        # Validate response type
        if interpretation.response_type not in self.allowed_response_types:
            logger.error(f"Response type '{interpretation.response_type}' not allowed.")
            raise ValueError(f"Invalid response type: {interpretation.response_type}")
        
        # Validate content
        if not interpretation.content or not interpretation.content.strip():
            logger.warning("Content is empty. Providing default content.")
            interpretation.content = "Procesando su solicitud..."
        
        # Validate resource if present
        if interpretation.resource is not None:
            self._validate_resource(interpretation.response_type, interpretation.resource)
        
        # Prepare the response data
        response_data = RobotResponseData(
            type=interpretation.response_type,
            content=interpretation.content,
            resource=interpretation.resource
        )
        
        return response_data
    
    def _validate_resource(self, response_type: str, resource: Dict[str, Any]) -> None:
        """
        Validate that a resource exists and is appropriate for the response type.
        
        Args:
            response_type: The type of response (text, image, animation)
            resource: The resource dictionary to validate
            
        Raises:
            ValueError: If the resource is invalid or doesn't exist
        """
        if response_type == "text":
            # For text responses, resource should be None
            if resource is not None:
                logger.warning("Resource provided for text response. Setting to None.")
                # We don't raise an error here, just ignore the resource
        
        elif response_type == "image":
            # For image responses, validate that it's an image resource
            if not isinstance(resource, dict) or "name" not in resource:
                raise ValueError("Image resource must be a dictionary with 'name' field")
            
            resource_name = resource.get("name")
            if not self.repository.resource_exists(resource_name, "image"):
                logger.warning(f"Image resource '{resource_name}' not found. Proceeding anyway.")
                # We don't raise an error here to allow for flexible resource naming
        
        elif response_type == "animation":
            # For animation responses, validate that it's an animation resource
            if not isinstance(resource, dict) or "name" not in resource:
                raise ValueError("Animation resource must be a dictionary with 'name' field")
            
            resource_name = resource.get("name")
            if not self.repository.resource_exists(resource_name, "animation"):
                logger.warning(f"Animation resource '{resource_name}' not found. Proceeding anyway.")
                # We don't raise an error here to allow for flexible resource naming
            
            # Validate parameters if present
            if "parameters" in resource and not isinstance(resource["parameters"], dict):
                logger.warning("Animation parameters should be a dictionary. Ignoring.")
                resource["parameters"] = {}