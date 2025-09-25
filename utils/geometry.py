# utils/geometry.py

def calculate_iou(boxA, boxB):
    """
    Calculates the Intersection over Union (IoU) of two bounding boxes.

    Args:
        boxA (list): The first bounding box in [x1, y1, x2, y2] format.
        boxB (list): The second bounding box in [x1, y1, x2, y2] format.

    Returns:
        float: The IoU value, which is between 0.0 and 1.0.
    """
    # Determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # Compute the area of the intersection rectangle
    # The intersection area is 0 if the boxes don't overlap
    interArea = max(0, xB - xA) * max(0, yB - yA)

    # Compute the area of both the prediction and ground-truth rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # Compute the union area by taking the sum of the two areas
    # and subtracting the intersection area.
    unionArea = float(boxAArea + boxBArea - interArea)

    # Compute the intersection over union
    iou = interArea / unionArea if unionArea > 0 else 0

    return iou