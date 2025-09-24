import time
import random
from utils.config import CAR_PARTS

class MockPartIdentificationAgent:
    """
    A mock agent that simulates identifying which car parts are damaged.

    This agent takes damage bounding boxes as input and maps them to a predefined
    taxonomy of car parts, estimating the percentage of damage for each part.
    """

    def __init__(self):
        """Initializes the agent."""
        print("Initializing MockPartIdentificationAgent...")
        # Simulate model loading time
        time.sleep(0.15)

    def process(self, image_path: str, damage_detections: list):
        """
        Simulates mapping damage detections to car parts.

        Args:
            image_path (str): The path to the image file (for context).
            damage_detections (list): A list of damage detection dictionaries from
                                      the DamageDetectionAgent.

        Returns:
            dict: A dictionary containing the identified damaged parts.
        """
        print(f"--- Running Part Identification on: {image_path} ---")
        start_time = time.time()

        # Simulate processing delay
        time.sleep(random.uniform(0.5, 0.9))

        if not damage_detections:
            return {
                "damaged_parts": [],
                "processing_time_ms": (time.time() - start_time) * 1000
            }

        # --- Mock Logic ---
        # For each detected damage, we'll randomly assign it to a car part.
        # In a real system, this would involve spatial analysis, possibly using
        # a segmentation model or comparing bounding box overlaps.
        damaged_parts = []
        
        # Get a flat list of all possible exterior parts
        available_parts = CAR_PARTS["exterior"]
        
        # Ensure we don't assign more parts than are available
        num_parts_to_assign = min(len(damage_detections), len(available_parts))
        
        # Randomly select parts to be "damaged"
        assigned_parts = random.sample(available_parts, num_parts_to_assign)

        for i, detection in enumerate(damage_detections):
            if i < len(assigned_parts):
                part_name = assigned_parts[i]
                
                # Associate the original damage bbox with this part
                part_bbox = detection["bbox"] 
                
                part_data = {
                    "part_name": part_name,
                    "part_id": f"{part_name.upper()[:4]}-001", # Generate a mock ID
                    "damage_percentage": random.randint(15, 60),
                    "bbox": part_bbox,
                    # Carry over the damage type for the final report
                    "damage_type": detection.get("damage_type", "unknown")
                }
                damaged_parts.append(part_data)

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        print(f"--- Part Identification complete in {processing_time_ms:.0f}ms ---")

        return {
            "damaged_parts": damaged_parts,
            "processing_time_ms": processing_time_ms
        }

# Example usage (for testing the agent in isolation)
if __name__ == '__main__':
    agent = MockPartIdentificationAgent()
    
    # Create some mock damage detections to pass to the agent
    mock_detections = [
        {"bbox": [120, 340, 450, 520], "confidence": 0.92, "damage_type": "dent"},
        {"bbox": [600, 150, 750, 250], "confidence": 0.88, "damage_type": "scratch"}
    ]
    
    result = agent.process("path/to/image.jpg", mock_detections)
    print("\nPart Identification Result:")
    print(result)
    
    assert "damaged_parts" in result
    assert len(result["damaged_parts"]) <= len(mock_detections)
    if result["damaged_parts"]:
        assert "part_name" in result["damaged_parts"][0]
        assert "damage_percentage" in result["damaged_parts"][0]
        assert "bbox" in result["damaged_parts"][0]