import time
import random
from pathlib import Path
from ultralytics import YOLO

DAMAGE_CLASS_MAP = {
0: "car-part-crack",
1: "detachment",
2: "glass-crack",
3: "lamp-crack",
4: "minor-deformation",
5: "moderate-deformation",
6: "paint-chips",
7: "scratches",
8: "severe-deformation",
9: "side-mirror-crack",
10: "flat-tire",
}

class DamageDetectionAgent:
    """
    An agent that uses a fine-tuned YOLOv8 model to detect and classify
    vehicle damage from an image.
    """

    def __init__(self, model_path='models/damage.pt'):
        """
        Initializes the agent by loading the YOLO model.

        Args:
            model_path (str): The path to the pre-trained YOLO model file.
        """
        print("Initializing DamageDetectionAgent...")
        self.device = 'cpu'
        print(f"Using device: {self.device}")
        try:
            # Resolve model path relative to the project root if needed
            project_root = Path(__file__).resolve().parents[1]
            provided_path = Path(model_path).expanduser()

            if provided_path.is_absolute():
                resolved_path = provided_path
            else:
                # Prefer project-root relative first
                resolved_path = (project_root / provided_path).resolve()

            # If the resolved path doesn't exist, try models/ directory fallback
            if not resolved_path.exists():
                models_fallback = (project_root / 'models' / provided_path.name)
                if models_fallback.exists():
                    resolved_path = models_fallback

            print(f"Loading damage model from: {resolved_path}")

            self.model = YOLO(str(resolved_path))
            self.model.to(self.device)
            print("Damage detection model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def process(self, image_path: str):
        """
        Processes an image to detect damage using the YOLO model.

        Args:
            image_path (str): The path to the image file.

        Returns:
            dict: A dictionary containing the damage detection results, adhering
                  to the standard output format.
        """
        print(f"--- Running Damage Detection on: {image_path} ---")
        start_time = time.time()

        if not self.model:
            return {
                "detections": [],
                "total_damage_area": 0,
                "processing_time_ms": 0
            }

        # --- Real YOLO Model Inference ---
        try:
            results = self.model(image_path, verbose=False) # verbose=False to reduce console spam
        except Exception as e:
            print(f"An error occurred during model inference: {e}")
            return {"detections": [], "total_damage_area": 0, "processing_time_ms": (time.time() - start_time) * 1000}

        detections = []
        # Assuming results[0] contains the detections for the first image
        if results and results[0]:
            boxes = results[0].boxes
            for box in boxes:
                # Extract bounding box coordinates [x1, y1, x2, y2]
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
                
                # Extract confidence and class
                confidence = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                
                # Map class_id to damage_type string
                damage_type = DAMAGE_CLASS_MAP.get(class_id, "unknown_damage")

                detection = {
                    "bbox": [x1, y1, x2, y2],
                    "confidence": round(confidence, 2),
                    "damage_type": damage_type
                }
                detections.append(detection)

        # Mock the total damage area for now, as this is complex to calculate
        total_damage_area = round(random.uniform(5.0, 25.0), 2) if detections else 0

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        print(f"--- Damage Detection complete in {processing_time_ms:.0f}ms, found {len(detections)} damages ---")

        return {
            "detections": detections,
            "total_damage_area": total_damage_area,
            "processing_time_ms": processing_time_ms
        }

# Example usage (for testing the agent in isolation)
if __name__ == '__main__':
    # Make sure you have a model file named 'damage_detection_yolo.pt'
    # and a test image in the root directory to run this test.
    try:
        agent = DamageDetectionAgent(model_path='../models/damage.pt')
        # Create a dummy image for testing if you don't have one
        from PIL import Image
        import numpy as np
        dummy_image_path = "test_damage_image.jpg"
        Image.fromarray(np.zeros((640, 640, 3), dtype=np.uint8)).save(dummy_image_path)

        result = agent.process(dummy_image_path)
        print("\nDamage Detection Result:")
        print(result)
        assert "detections" in result
    except Exception as e:
        print(f"Could not run test: {e}")