import os
from groq import Groq
from app.models.robot_request import RobotRequest
import logging

# Set up logger
logger = logging.getLogger(__name__)


class GroqService:
    """Service for communicating with Groq API."""
    
    def __init__(self):
        """Initialize the Groq service with API key from environment."""
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set in environment variables")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key) if self.api_key else None
    
    def interpret_text(self, request: RobotRequest) -> str:
        """
        Send text to Groq API and get response.
        
        Args:
            request: RobotRequest containing the text to interpret
            
        Returns:
            Response text from Groq
            
        Raises:
            Exception: If there's an error communicating with Groq
        """
        if not self.client:
            raise Exception("Groq client not initialized. Check GROQ_API_KEY environment variable.")
        
        if not request.text or not request.text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": request.text
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
                stream=False
            )
            
            response_text = chat_completion.choices[0].message.content
            return response_text
            
        except Exception as e:
            logger.error(f"Error communicating with Groq: {str(e)}")
            raise Exception(f"Groq service error: {str(e)}")