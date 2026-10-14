from app.repositories.face_repository import FaceRepository
from typing import List, Dict


class FaceService:
    """Service for processing facial component data."""
    
    def __init__(self):
        """Initialize the service with a face repository."""
        self.repository = FaceRepository()
    
    def get_initial_face_components(self) -> List[Dict[str, str]]:
        """
        Get the initial face components for the robot.
        
        Returns:
            List of dictionaries containing component data
            
        Raises:
            FileNotFoundError: If any component file is missing
            IOError: If there's an error reading any file
        """
        return self.repository.get_all_components()