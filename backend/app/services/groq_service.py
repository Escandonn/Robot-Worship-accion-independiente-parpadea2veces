import os
import json
from typing import Dict, Any
from groq import Groq
from app.models.groq_interpretation import GroqInterpretation
from app.models.robot_request import RobotRequest
import logging

# Set up logger
logger = logging.getLogger(__name__)


class GroqService:
    """Service for communicating with Groq API to interpret text."""
    
    def __init__(self):
        """Initialize the Groq service with API key from environment."""
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")  # Default model
        
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set in environment variables")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key) if self.api_key else None
    
    def interpret_text(self, request: RobotRequest) -> GroqInterpretation:
        """
        Interpret text using Groq API.
        
        Args:
            request: RobotRequest containing the text to interpret
            
        Returns:
            GroqInterpretation object with the results
            
        Raises:
            Exception: If there's an error communicating with Groq or processing the response
        """
        if not self.client:
            raise Exception("Groq client not initialized. Check GROQ_API_KEY environment variable.")
        
        # Validate input
        if not request.text or not request.text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            # Construct the prompt for Groq to get structured output
            prompt = self._create_interpretation_prompt(request.text)
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.1,  # Low temperature for more consistent outputs
                max_tokens=1024,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"}  # Request JSON output
            )
            
            # Extract the response
            response_text = chat_completion.choices[0].message.content
            
            # Parse the JSON response
            try:
                response_data = json.loads(response_text)
                interpretation = GroqInterpretation(**response_data)
                return interpretation
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Groq response as JSON: {response_text}")
                raise Exception(f"Invalid response from Groq: {str(e)}")
            except Exception as e:
                logger.error(f"Failed to validate Groq response: {str(e)}")
                raise Exception(f"Groq response validation failed: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error communicating with Groq: {str(e)}")
            raise Exception(f"Groq service error: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for guiding Groq's interpretation."""
        return """
        Eres un asistente que interpreta instrucciones en lenguaje natural para un robot llamado WORSHIP.
        Tu tarea es analizar el texto del usuario y determinar qué tipo de respuesta debe generar el robot.
        
        Debes devolver un objeto JSON con la siguiente estructura:
        {
          "intent": "string que identifica la intención principal del usuario",
          "response_type": "tipo de respuesta (text, image, o animation)",
          "content": "texto descriptivo de la respuesta que el frontend debe mostrar o comunicar",
          "resource": {
            // Información sobre el recurso necesario (opcional)
            // Para animations: {"name": "blink", "parameters": {"count": 2}}
            // Para images: {"name": "resource-name", "path": "ruta/al/recurso.png"}
            // Para text: null
          }
        }
        
        Intenciones posibles:
        - "greeting": El usuario está saludando o iniciando una conversación
        - "blink": El usuario quiere que el robot parpadee (una o más veces)
        - "show_image": El usuario quiere ver una imagen específica
        - "unknown": La intención no es clara o no pertenece a las categorías anteriores
        
        Ejemplos:
        - Entrada: "Hola Risp, ¿cómo estás?"
          Salida: {
            "intent": "greeting",
            "response_type": "text",
            "content": "¡Hola! Estoy listo para ayudarte.",
            "resource": null
          }
          
        - Entrada: "Parpadea dos veces"
          Salida: {
            "intent": "blink",
            "response_type": "animation",
            "content": "Voy a parpadear dos veces.",
            "resource": {"name": "blink", "parameters": {"count": 2}}
          }
          
        - Entrada: "Muestra una imagen de un corazón"
          Salida: {
            "intent": "show_image",
            "response_type": "image",
            "content": "Aquí tienes la imagen solicitada.",
            "resource": {"name": "corazon", "path": "emociones/corazon.png"}
          }
        
        Asegúrate de que tu respuesta sea válida JSON y siga exactamente esta estructura.
        No incluyas texto adicional fuera del JSON.
        """
    
    def _create_interpretation_prompt(self, text: str) -> str:
        """Create the prompt for Groq based on the user's text."""
        return f"""
        Analiza el siguiente texto del usuario y proporciona una interpretación estructurada:
        
        Texto del usuario: "{text}"
        
        Recuerda devolver únicamente un objeto JSON con la estructura especificada en el prompt del sistema.
        """