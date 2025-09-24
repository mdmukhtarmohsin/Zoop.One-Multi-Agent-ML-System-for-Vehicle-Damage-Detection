import time
import random
from utils.config import SEVERITY_RULES, DAMAGE_TO_SEVERITY_MAPPING

class MockSeverityAssessmentAgent:
    """
    A mock agent that simulates assessing the overall severity of the damage.

    This agent aggregates all damage and part data to classify the overall
    severity, estimate repair costs, and recommend a repair approach.
    """

    def __init__(self):
        """Initializes the agent."""
        print("Initializing MockSeverityAssessmentAgent...")
        # Simulate model loading time
        time.sleep(0.1)

    def process(self, damaged_parts_data: list):
        """
        Simulates the final assessment of damage severity and cost.

        Args:
            damaged_parts_data (list): A list of dictionaries, where each dict
                                       describes a damaged part and the type of damage.

        Returns:
            dict: A dictionary containing the comprehensive severity assessment.
        """
        print("--- Running Severity Assessment ---")
        start_time = time.time()

        # Simulate processing delay
        time.sleep(random.uniform(0.4, 0.7))

        if not damaged_parts_data:
            return {
                "overall_severity": "no_damage_detected",
                "severity_score": 0.0,
                "repair_category": "none",
                "estimated_cost_range": [0, 0],
                "repair_time_days": 0,
                "processing_time_ms": (time.time() - start_time) * 1000
            }

        # --- Mock Logic ---
        # Determine overall severity based on the most severe damage type found.
        # In a real system, this would be a more complex rule engine or a predictive model.
        
        severity_levels = {"minor": 1, "moderate": 2, "major": 3, "severe": 4}
        max_severity_level = 0
        
        for part in damaged_parts_data:
            damage_type = part.get("damage_type", "dent")
            severity_str = DAMAGE_TO_SEVERITY_MAPPING.get(damage_type, "moderate")
            level = severity_levels.get(severity_str, 2)
            if level > max_severity_level:
                max_severity_level = level

        # Map the highest detected level back to a string
        overall_severity = next(
            (k for k, v in severity_levels.items() if v == max_severity_level), "moderate"
        )

        # Use the severity rules from our config to get cost and time
        assessment_rules = SEVERITY_RULES.get(overall_severity, SEVERITY_RULES["moderate"])
        cost_range = assessment_rules["cost_range"]
        repair_days = assessment_rules["repair_days"]

        # Add some random jitter to the cost estimate
        cost_range[0] = int(cost_range[0] * random.uniform(0.9, 1.1))
        cost_range[1] = int(cost_range[1] * random.uniform(1.0, 1.2))

        # Generate a final severity score out of 10
        severity_score = round(max_severity_level * 2.5 - random.uniform(0, 1), 1)

        repair_category_map = {
            "minor": "minor_cosmetic_repair",
            "moderate": "body_shop_required",
            "major": "significant_body_work",
            "severe": "potential_total_loss"
        }
        repair_category = repair_category_map.get(overall_severity)

        end_time = time.time()
        processing_time_ms = (end_time - start_time) * 1000
        print(f"--- Severity Assessment complete in {processing_time_ms:.0f}ms ---")

        return {
            "overall_severity": overall_severity,
            "severity_score": severity_score,
            "repair_category": repair_category,
            "estimated_cost_range": cost_range,
            "repair_time_days": repair_days,
            "processing_time_ms": processing_time_ms
        }

# Example usage (for testing the agent in isolation)
if __name__ == '__main__':
    agent = MockSeverityAssessmentAgent()
    
    # Create mock data from the previous agent
    mock_damaged_parts = [
        {"part_name": "front_bumper", "damage_type": "dent"},
        {"part_name": "left_headlight", "damage_type": "crack"} # This should drive the severity
    ]
    
    result = agent.process(mock_damaged_parts)
    print("\nSeverity Assessment Result:")
    print(result)
    
    assert "overall_severity" in result
    # "crack" is "major", so the overall severity should be "major"
    assert result["overall_severity"] == "major"
    assert result["estimated_cost_range"][0] >= SEVERITY_RULES["major"]["cost_range"][0]
    assert result["repair_time_days"] == SEVERITY_RULES["major"]["repair_days"]