import time
import random
from utils.config import DAMAGE_TYPES

class MockDamageDetectionAgent:
    """
    A mock agent that simulates detecting and classifying vehicle damage.

    This agent mimics the output of an object detection model, returning bounding
    boxes for damaged areas, classifying the type of damage, and providing a
    confidence score.
    """

    def __init__(self):
        """Initializes the agent."""
        print("Initializing MockDamageDetectionAgent...")
        # Simulate model loading time
        time.sleep(0.2)

    def process(self, image_path: str):
        """
        Simulates processing an image to detect damage.

        Args:
            image_path (str): The path to the image file.

        Returns:
            dict: A dictionary containing the damage detection results.
        """
        print(f"--- Running Damage Detection on: {image_path} ---")
        start_time = time.time()

        # Simulate processing delay, as this is typically the slowest step
        time.sleep(random.uniform(0.8, 1.5))

        # --- Mock Logic ---
        # We'll generate a few random bounding boxes to simulate detections.
        # In a real scenario, these would come from a model like YOLO.
        detections = []
        num_detections = random.randint(1, 3) # Simulate finding 1 to 3 damaged areas

        for _ in range(num_detections):
            # Generate random bounding box coordinates [x1, y1, x2, y2]
            x1 = random.randint(50, 200)
            y1 = random.randint(100, 300)
            width = random.randint(100, 250)
            height = random.randint(80, 200)
            x2 = x1 + width
            y2 = y1 + height

            detection = {
                "bbox": [x1, y1, x2, y2],
                "confidence": round(random.uniform(0.88, 0.99), 2),
                "damage_type": random.choice(DAMAGE_TYPES)
            }
            detections.append(detection)

        # Simulate a total damage area calculation (as a percentage)
        total_damage_area = round(random.uniform(5.0, 25.0), 2)

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        print(f"--- Damage Detection complete in {processing_time_ms:.0f}ms ---")

        return {
            "detections": detections,
            "total_damage_area": total_damage_area,
            "processing_time_ms": processing_time_ms
        }

# Example usage (for testing the agent in isolation)
if __name__ == '__main__':
    agent = MockDamageDetectionAgent()
    
    result = agent.process("path/to/some_image.jpg")
    print("\nDamage Detection Result:")
    print(result)
    
    assert "detections" in result
    assert "total_damage_area" in result
    assert len(result["detections"]) > 0
    assert "bbox" in result["detections"][0]
    assert "confidence" in result["detections"][0]
    assert "damage_type" in result["detections"][0]