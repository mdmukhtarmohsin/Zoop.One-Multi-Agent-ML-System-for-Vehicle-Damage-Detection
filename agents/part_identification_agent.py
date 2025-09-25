import time
import random
from pathlib import Path
from ultralytics import YOLO
from utils.geometry import calculate_iou

# IMPORTANT: You must update this map to match your part detection model's classes.
# The key is the class index (0, 1, 2, ...) and the value is the part name.
PART_CLASS_MAP = {
  0: "back_bumper",
  1: "back_door",
  2: "back_glass",
  3: "back_left_door",
  4: "back_left_light",
  5: "back_light",
  6: "back_right_door",
  7: "back_right_light",
  8: "front_bumper",
  9: "front_door",
  10: "front_glass",
  11: "front_left_door",    
  12: "front_left_light",
  13: "front_light",
  14: "front_right_door",
  15: "front_right_light",
  16: "hood",
  17: "left_mirror",
  18: "object", 
  19: "right_mirror",
  20: "tailgate",
  21: "trunk",
  22: "wheel",
}

class PartIdentificationAgent:
    """
    An agent that uses a YOLO model to identify car parts and then maps
    detected damages to those parts based on bounding box overlap (IoU).
    """
    IOU_THRESHOLD = 0.01 # If overlap is less than 10%, we don't associate them.

    def __init__(self, model_path='models/parts.pt'):
        """
        Initializes the agent by loading the part detection YOLO model.
        """
        print("Initializing PartIdentificationAgent...")
        self.device = 'cpu'
        print(f"Using device: {self.device}")
        try:
            # Resolve model path relative to the project root if needed
            project_root = Path(__file__).resolve().parents[1]
            provided_path = Path(model_path).expanduser()

            if provided_path.is_absolute():
                resolved_path = provided_path
            else:
                resolved_path = (project_root / provided_path).resolve()

            if not resolved_path.exists():
                models_fallback = (project_root / 'models' / provided_path.name)
                if models_fallback.exists():
                    resolved_path = models_fallback

            print(f"Loading parts model from: {resolved_path}")

            self.model = YOLO(str(resolved_path))
            self.model.to(self.device)
            print("Part detection model loaded successfully.")
        except Exception as e:
            print(f"Error loading part detection model: {e}")
            self.model = None

    def process(self, image_path: str, damage_detections: list):
        """
        Identifies car parts in the image and associates them with the provided
        damage detections.

        Args:
            image_path (str): The path to the image file.
            damage_detections (list): A list of damage detection dictionaries.

        Returns:
            dict: A dictionary containing the identified damaged parts.
        """
        print(f"--- Running Part Identification on: {image_path} ---")
        start_time = time.time()

        if not self.model or not damage_detections:
            return {
                "damaged_parts": [],
                "processing_time_ms": (time.time() - start_time) * 1000
            }

        # --- 1. Detect all car parts in the image ---
        try:
            part_results = self.model(image_path, verbose=False)
        except Exception as e:
            print(f"An error occurred during part detection inference: {e}")
            return {"damaged_parts": [], "processing_time_ms": (time.time() - start_time) * 1000}

        detected_parts = []
        if part_results and part_results[0]:
            for box in part_results[0].boxes:
                detected_parts.append({
                    "bbox": box.xyxy[0].cpu().numpy().tolist(),
                    "class_id": int(box.cls[0].cpu().numpy())
                })

        # --- 2. Find the best part match for each damage ---
        damaged_parts = []
        for damage in damage_detections:
            best_iou = 0
            best_part_match = None

            for part in detected_parts:
                iou = calculate_iou(damage['bbox'], part['bbox'])
                if iou > best_iou:
                    best_iou = iou
                    best_part_match = part
            
            # If a sufficiently overlapping part was found, create the record
            if best_part_match and best_iou > self.IOU_THRESHOLD:
                part_name = PART_CLASS_MAP.get(best_part_match['class_id'], "unknown_part")
                
                part_data = {
                    "part_name": part_name,
                    "part_id": f"{part_name.upper()[:4]}-001", # Mock ID
                    "damage_percentage": random.randint(15, 60), # Mocked for now
                    "bbox": damage['bbox'], # Use the damage bbox for annotation
                    "damage_type": damage.get("damage_type", "unknown")
                }
                damaged_parts.append(part_data)

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        print(f"--- Part Identification complete in {processing_time_ms:.0f}ms ---")

        return {
            "damaged_parts": damaged_parts,
            "processing_time_ms": processing_time_ms
        }

# Example usage
if __name__ == '__main__':
    # This test requires both a model and a test image.
    try:
        agent = PartIdentificationAgent(model_path='parts.pt')
        
        # Mock damage detections from the previous agent
        mock_detections = [
            {"bbox": [120, 340, 450, 520], "confidence": 0.92, "damage_type": "dent"},
            {"bbox": [600, 150, 750, 250], "confidence": 0.88, "damage_type": "scratch"}
        ]
        
        # Create a dummy image for testing
        from PIL import Image
        import numpy as np
        dummy_image_path = "test_parts_image.jpg"
        Image.fromarray(np.zeros((640, 640, 3), dtype=np.uint8)).save(dummy_image_path)

        result = agent.process(dummy_image_path, mock_detections)
        print("\nPart Identification Result:")
        print(result)
    except Exception as e:
        print(f"Could not run test: {e}")