from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class GraphState(TypedDict):
    """
    Defines the state that is passed between nodes in the LangGraph.

    This state object accumulates the data as a claim is processed through
    the multi-agent pipeline. It uses proper Python type annotations.
    """
    
    # --- Initial Inputs ---
    claim_id: str
    image_path: str
    
    # --- State Tracking ---
    processing_log: List[str]
    error_message: Optional[str]

    # --- Agent Outputs ---
    # These fields will be populated by the respective agents.
    quality_check_result: Optional[Dict[str, Any]]
    damage_detection_result: Optional[Dict[str, Any]]
    part_identification_result: Optional[Dict[str, Any]]
    severity_assessment_result: Optional[Dict[str, Any]]

    # --- Final Compiled Output ---
    # This will hold the final, formatted report.
    final_report: Optional[Dict[str, Any]]