from pathlib import Path
from typing import Dict, Any, Optional


class ResourceRepository:
    """Repository for accessing visual resources."""
    
    def __init__(self, base_path: str = "app/assets"):
        """
        Initialize the repository with the base path to assets.
        
        Args:
            base_path: Relative path to the assets directory
        """
        self.base_path = Path(base_path)
        # Define available resources
        self.available_resources = {
            "blink": {
                "type": "animation",
                "variants": ["variant_01", "variant_02", "variant_03"],
                "frames": ["frame_01", "frame_02", "frame_03"]
            }
            # More resources can be added here as needed
        }
    
    def resource_exists(self, resource_name: str, resource_type: str = None) -> bool:
        """
        Check if a resource exists in the catalog.
        
        Args:
            resource_name: Name of the resource to check
            resource_type: Type of resource (animation, image, etc.) - optional
            
        Returns:
            Boolean indicating if the resource exists
        """
        if resource_name not in self.available_resources:
            return False
            
        if resource_type is None:
            return True
            
        return self.available_resources[resource_name]["type"] == resource_type
    
    def get_resource_info(self, resource_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific resource.
        
        Args:
            resource_name: Name of the resource
            
        Returns:
            Dictionary with resource information or None if not found
        """
        return self.available_resources.get(resource_name)
    
    def get_animation_frames(self, animation_name: str, variant: str = None) -> Optional[list]:
        """
        Get the frames for an animation.
        
        Args:
            animation_name: Name of the animation
            variant: Specific variant to get frames for (optional)
            
        Returns:
            List of frame names or None if not found
        """
        if not self.resource_exists(animation_name, "animation"):
            return None
            
        animation_info = self.get_resource_info(animation_name)
        if variant is None:
            # Return frames for the first variant if none specified
            return animation_info["frames"]
        else:
            # In a more complex implementation, we would return frames for a specific variant
            # For now, we'll just return the general frames
            return animation_info["frames"]

    def read_blink_frame_bytes(self) -> list[tuple[str, bytes]]:
        """Read the ordered PNG frames used by the blink animation."""
        frames_path = Path(__file__).resolve().parents[1] / "assets" / "ojos"
        frame_names = ("1.png", "2.png", "3.png")

        return [
            (name, (frames_path / name).read_bytes())
            for name in frame_names
        ]