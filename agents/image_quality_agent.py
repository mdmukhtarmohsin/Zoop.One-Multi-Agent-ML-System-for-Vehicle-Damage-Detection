import time
import random
import numpy as np

class MockImageQualityAgent:
    """
    A mock agent that simulates assessing image quality.

    This agent checks for simulated issues like blur, low light, or potential
    manipulation. It decides whether an image is processable and can suggest
    enhancements.
    """

    def __init__(self):
        """Initializes the agent."""
        print("Initializing MockImageQualityAgent...")
        # Simulate model loading time
        time.sleep(0.1)

    def process(self, image_path: str):
        """
        Simulates the processing of a single image to check its quality.

        Args:
            image_path (str): The path to the image file.

        Returns:
            dict: A dictionary containing the quality assessment results.
        """
        print(f"--- Running Image Quality Check on: {image_path} ---")
        start_time = time.time()

        # Simulate processing delay
        time.sleep(random.uniform(0.2, 0.5))

        # --- Mock Logic ---
        # We'll use the filename to simulate different quality scenarios.
        # This allows us to easily test different paths in our orchestrator.
        issues = []
        quality_score = random.uniform(0.85, 0.99)
        processable = True
        manipulation_detected = False

        if "blurry" in image_path.lower():
            issues.append("blur")
            quality_score = random.uniform(0.4, 0.6)
            processable = False
        
        if "dark" in image_path.lower():
            issues.append("low_light")
            quality_score = random.uniform(0.5, 0.7)
            # Let's say low_light is correctable, so processable remains True
        
        if "manipulated" in image_path.lower():
            manipulation_detected = True
            # Even if manipulated, we might still process it but flag it.
        
        # Simulate a placeholder for an enhanced image (e.g., a blank array)
        enhanced_image_placeholder = np.zeros((100, 100, 3), dtype=np.uint8)

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        print(f"--- Quality Check complete in {processing_time_ms:.0f}ms ---")

        return {
            "quality_score": round(quality_score, 2),
            "issues": issues,
            "enhanced_image": enhanced_image_placeholder,
            "processable": processable,
            "manipulation_detected": manipulation_detected,
            "processing_time_ms": processing_time_ms
        }

# Example usage (for testing the agent in isolation)
if __name__ == '__main__':
    agent = MockImageQualityAgent()
    
    # Test case 1: Good quality image
    good_image_result = agent.process("path/to/good_image.jpg")
    print("\nGood Image Result:")
    print(good_image_result)
    assert good_image_result["processable"] is True

    # Test case 2: Blurry image (should be rejected)
    blurry_image_result = agent.process("path/to/blurry_image.jpg")
    print("\nBlurry Image Result:")
    print(blurry_image_result)
    assert blurry_image_result["processable"] is False
    assert "blur" in blurry_image_result["issues"]

    # Test case 3: Dark image (should be processable)
    dark_image_result = agent.process("path/to/dark_image.jpg")
    print("\nDark Image Result:")
    print(dark_image_result)
    assert dark_image_result["processable"] is True
    assert "low_light" in dark_image_result["issues"]