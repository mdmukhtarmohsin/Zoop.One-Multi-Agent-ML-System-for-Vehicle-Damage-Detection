# Car parts taxonomy based on the problem description
CAR_PARTS = {
    "exterior": [
        "front_bumper", "rear_bumper", "hood", "trunk",
        "left_door", "right_door", "left_fender", "right_fender",
        "windshield", "rear_window", "side_windows",
        "left_headlight", "right_headlight", "tail_lights"
    ],
    "wheels": ["front_left_wheel", "front_right_wheel", "rear_left_wheel", "rear_right_wheel"]
}

# Damage categories based on the problem description
DAMAGE_TYPES = ["scratch", "dent", "crack", "shatter", "missing", "bent", "paint_damage"]

# Severity mapping rules based on the problem description
SEVERITY_RULES = {
    "minor": {"cost_range": [100, 500], "repair_days": 1},
    "moderate": {"cost_range": [500, 3000], "repair_days": 3},
    "major": {"cost_range": [3000, 10000], "repair_days": 7},
    "severe": {"cost_range": [10000, 30000], "repair_days": 14}
}

# Evaluation metrics for documentation purposes
EVALUATION_METRICS = {
    "detection_accuracy": "Percentage of damages correctly identified",
    "localization_iou": "Intersection over Union for bounding boxes",
    "part_classification": "Accuracy of part identification",
    "severity_accuracy": "Correct severity classification rate",
    "processing_speed": "Average time per image",
    "multi_image_consistency": "Consistency across multiple angles"
}

# A simple mapping to associate damage types with potential severity levels
# This will be used by the mock severity agent.
DAMAGE_TO_SEVERITY_MAPPING = {
    "scratch": "minor",
    "paint_damage": "minor",
    "dent": "moderate",
    "bent": "moderate",
    "crack": "major",
    "shatter": "major",
    "missing": "severe"
}