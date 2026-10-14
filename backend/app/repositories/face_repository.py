import os
import base64
from typing import List, Dict
from pathlib import Path


class FaceRepository:
    """Repository for accessing facial component files."""
    
    def __init__(self, base_path: str = "app/assets/emociones"):
        """
        Initialize the repository with the base path to emociones assets.
        
        Args:
            base_path: Relative path to the emociones directory
        """
        self.base_path = Path(base_path)
        self.components = [
            {"name": "boca", "subdir": "boca", "filename": "boca.png"},
            {"name": "nariz", "subdir": "nariz", "filename": "nariz.png"},
            {"name": "ojo-derecho", "subdir": "ojo-derecho", "filename": "ojo-derecho.png"},
            {"name": "ojo-izquierdo", "subdir": "ojo-izquierdo", "filename": "ojo-izquierdo.png"}
        ]
    
    def get_component_path(self, component_name: str) -> Path:
        """
        Get the full path to a component file.
        
        Args:
            component_name: Name of the component (boca, nariz, etc.)
            
        Returns:
            Path object pointing to the component file
        """
        component_info = next(
            (c for c in self.components if c["name"] == component_name), 
            None
        )
        
        if not component_info:
            raise ValueError(f"Unknown component: {component_name}")
            
        return self.base_path / component_info["subdir"] / component_info["filename"]
    
    def get_all_components(self) -> List[Dict[str, str]]:
        """
        Get all facial components with their Base64 encoded data.
        
        Returns:
            List of dictionaries containing component information
            
        Raises:
            FileNotFoundError: If any component file is missing
            IOError: If there's an error reading any file
        """
        components_data = []
        
        for component_info in self.components:
            file_path = self.base_path / component_info["subdir"] / component_info["filename"]
            
            # Check if file exists
            if not file_path.exists():
                raise FileNotFoundError(f"Component file not found: {file_path}")
            
            # Read and encode the file
            try:
                with open(file_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                
                components_data.append({
                    "name": component_info["name"],
                    "type": "image/png",
                    "data": encoded_string
                })
            except Exception as e:
                raise IOError(f"Error reading file {file_path}: {str(e)}")
        
        return components_data