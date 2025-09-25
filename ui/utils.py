import cv2
import numpy as np
from PIL import Image

# Define a color map for different severity levels to be used in annotations.
# Colors are in BGR format for OpenCV.
SEVERITY_COLOR_MAP = {
    "minor": (0, 255, 0),      # Green
    "moderate": (0, 255, 255), # Yellow
    "major": (0, 165, 255),    # Orange
    "severe": (0, 0, 255),     # Red
    "default": (255, 0, 0)     # Blue (for any unknown cases)
}

def draw_raw_detection_boxes(image_path: str, damage_detection_result: dict) -> np.ndarray:
    """
    Draws simple bounding boxes from the initial damage detection step.
    Uses a single color since severity and parts are not yet known.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        return np.zeros((400, 600, 3), dtype=np.uint8)

    detections = damage_detection_result.get("detections", [])
    
    raw_detection_color = (255, 0, 0) 

    for detection in detections:
        bbox = detection.get("bbox")
        if not bbox or len(bbox) != 4:
            continue

        x1, y1, x2, y2 = map(int, bbox)
        damage_type = detection.get("damage_type", "N/A")
        confidence = detection.get("confidence", 0)
        
        cv2.rectangle(image_cv, (x1, y1), (x2, y2), raw_detection_color, 2)
        
        label = f"{damage_type.capitalize()} ({confidence:.0%})"
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(image_cv, (x1, y1 - 20), (x1 + text_width, y1), raw_detection_color, -1)
        cv2.putText(image_cv, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)

import cv2
import numpy as np
from PIL import Image

# Define a color map for different severity levels to be used in annotations.
# Colors are in BGR format for OpenCV.
SEVERITY_COLOR_MAP = {
    "minor": (0, 255, 0),      # Green
    "moderate": (0, 255, 255), # Yellow
    "major": (0, 165, 255),    # Orange
    "severe": (0, 0, 255),     # Red
    "default": (255, 0, 0)     # Blue (for any unknown cases)
}

# --- EXISTING FUNCTION (NO CHANGES) ---
def draw_raw_detection_boxes(image_path: str, damage_detection_result: dict) -> np.ndarray:
    # ... (this function remains the same)
    try:
        image = Image.open(image_path).convert("RGB")
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        return np.zeros((400, 600, 3), dtype=np.uint8)
    detections = damage_detection_result.get("detections", [])
    raw_detection_color = (255, 0, 0) 
    for detection in detections:
        bbox = detection.get("bbox")
        if not bbox or len(bbox) != 4: continue
        x1, y1, x2, y2 = map(int, bbox)
        damage_type = detection.get("damage_type", "N/A")
        confidence = detection.get("confidence", 0)
        cv2.rectangle(image_cv, (x1, y1), (x2, y2), raw_detection_color, 2)
        label = f"{damage_type.capitalize()} ({confidence:.0%})"
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(image_cv, (x1, y1 - 20), (x1 + text_width, y1), raw_detection_color, -1)
        cv2.putText(image_cv, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)


# --- NEW FUNCTION ---
def draw_part_assignments(image_path: str, part_identification_result: dict) -> np.ndarray:
    """
    Draws bounding boxes of damages and labels them with the identified car part.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        return np.zeros((400, 600, 3), dtype=np.uint8)

    damaged_parts = part_identification_result.get("damaged_parts", [])
    
    # Use a distinct color for this step (e.g., orange)
    assignment_color = (0, 165, 255)

    for part in damaged_parts:
        bbox = part.get("bbox")
        if not bbox or len(bbox) != 4:
            continue

        x1, y1, x2, y2 = map(int, bbox)
        part_name = part.get("part_name", "N/A")
        damage_type = part.get("damage_type", "N/A")
        
        # Draw the bounding box
        cv2.rectangle(image_cv, (x1, y1), (x2, y2), assignment_color, 2)
        
        # Create and draw the label showing the assigned part
        label = f"{damage_type.capitalize()} -> {part_name}"
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(image_cv, (x1, y1 - 20), (x1 + text_width, y1), assignment_color, -1)
        cv2.putText(image_cv, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    return cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)


def draw_annotations(image_path: str, final_report: dict) -> np.ndarray:
    """
    Draws final, color-coded bounding boxes and labels on an image.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        image_np = np.array(image)
        # --- THE FIX IS ON THIS LINE ---
        # Changed cv2.COLOR_RGB_BGR to cv2.COLOR_RGB2BGR
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        return np.zeros((400, 600, 3), dtype=np.uint8)

    if not final_report or "assessment_result" not in final_report:
        return cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB) # Return original image in correct format

    annotations = final_report["assessment_result"].get("annotations", [])
    if not annotations:
        return cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB) # Return original image in correct format

    detections = annotations[0].get("detections", [])

    for detection in detections:
        bbox = detection.get("bbox")
        if not bbox or len(bbox) != 4:
            continue

        x1, y1, x2, y2 = map(int, bbox)
        damage_type = detection.get("damage_type", "N/A")
        part = detection.get("part", "N/A")
        confidence = detection.get("confidence", 0)
        severity = detection.get("severity", "default")
        color = SEVERITY_COLOR_MAP.get(severity, SEVERITY_COLOR_MAP["default"])

        cv2.rectangle(image_cv, (x1, y1), (x2, y2), color, 2)
        label = f"{damage_type.capitalize()} on {part} ({confidence:.0%})"
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        label_bg_y2 = y1 - 10
        label_bg_y1 = label_bg_y2 - text_height - 5
        
        if label_bg_y1 < 0:
            label_bg_y1 = y2 + 5
            label_bg_y2 = y2 + 10 + text_height

        cv2.rectangle(image_cv, (x1, label_bg_y1), (x1 + text_width, label_bg_y2), color, -1)
        cv2.putText(image_cv, label, (x1, y1 - 15 if label_bg_y1 < y1 else y2 + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    return cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)