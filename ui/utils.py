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

def draw_annotations(image_path: str, final_report: dict) -> np.ndarray:
    """
    Draws bounding boxes and labels on an image based on the final report.

    Args:
        image_path (str): The path to the original image.
        final_report (dict): The final compiled report containing annotations.

    Returns:
        np.ndarray: The image with annotations drawn on it, as a NumPy array.
    """
    try:
        # Load the image using Pillow and convert to an OpenCV-compatible format (BGR)
        image = Image.open(image_path).convert("RGB")
        image_np = np.array(image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        # Return a blank image if the original file is not found
        return np.zeros((400, 600, 3), dtype=np.uint8)

    # Extract the list of detections for the specific image
    # The report structure has annotations nested under the image_id
    if not final_report or "assessment_result" not in final_report:
        return image_cv # Return original image if report is empty

    annotations = final_report["assessment_result"].get("annotations", [])
    if not annotations:
        return image_cv

    # The first item in the list corresponds to our single image
    detections = annotations[0].get("detections", [])

    for detection in detections:
        bbox = detection.get("bbox")
        if not bbox or len(bbox) != 4:
            continue

        # Get coordinates
        x1, y1, x2, y2 = map(int, bbox)

        # Get details for the label
        damage_type = detection.get("damage_type", "N/A")
        part = detection.get("part", "N/A")
        confidence = detection.get("confidence", 0)
        severity = detection.get("severity", "default")

        # Get color from the map
        color = SEVERITY_COLOR_MAP.get(severity, SEVERITY_COLOR_MAP["default"])

        # Draw the bounding box
        cv2.rectangle(image_cv, (x1, y1), (x2, y2), color, 2)

        # Create the label text
        label = f"{damage_type.capitalize()} on {part} ({confidence:.0%})"

        # Position the label text slightly above the bounding box
        # Add a filled rectangle as a background for the text for better readability
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        label_bg_y2 = y1 - 10
        label_bg_y1 = label_bg_y2 - text_height - 5
        
        # Adjust if the label goes off-screen
        if label_bg_y1 < 0:
            label_bg_y1 = y2 + 5
            label_bg_y2 = y2 + 10 + text_height

        cv2.rectangle(image_cv, (x1, label_bg_y1), (x1 + text_width, label_bg_y2), color, -1)
        cv2.putText(image_cv, label, (x1, y1 - 15 if label_bg_y1 < y1 else y2 + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Convert back to RGB for display in Gradio
    return cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)