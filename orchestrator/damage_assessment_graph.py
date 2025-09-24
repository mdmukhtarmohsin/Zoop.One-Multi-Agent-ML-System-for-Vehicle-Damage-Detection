import time
from langgraph.graph import StateGraph, END
from .graph_state import GraphState

# Import the mock agents
from agents.image_quality_agent import MockImageQualityAgent
from agents.damage_detection_agent import MockDamageDetectionAgent
from agents.part_identification_agent import MockPartIdentificationAgent
from agents.severity_assessment_agent import MockSeverityAssessmentAgent

# --- 1. Instantiate Agents ---
# Create a single instance of each agent to be used throughout the graph.
quality_agent = MockImageQualityAgent()
detection_agent = MockDamageDetectionAgent()
part_agent = MockPartIdentificationAgent()
severity_agent = MockSeverityAssessmentAgent()

# --- 2. Define Graph Nodes ---
# Each node in the graph is a function that takes the current state, performs an action,
# and returns a dictionary to update the state.

def run_quality_check(state: GraphState) -> GraphState:
    """Runs the Image Quality Agent and updates the state."""
    state['processing_log'].append("Step 1: Assessing Image Quality...")
    image_path = state['image_path']
    
    result = quality_agent.process(image_path)
    
    state['quality_check_result'] = result
    return state

def run_damage_detection(state: GraphState) -> GraphState:
    """Runs the Damage Detection Agent and updates the state."""
    state['processing_log'].append("Step 2: Detecting Damage...")
    image_path = state['image_path']
    
    result = detection_agent.process(image_path)
    
    state['damage_detection_result'] = result
    return state

def run_part_identification(state: GraphState) -> GraphState:
    """Runs the Part Identification Agent and updates the state."""
    state['processing_log'].append("Step 3: Identifying Damaged Parts...")
    image_path = state['image_path']
    damage_detections = state['damage_detection_result']['detections']
    
    result = part_agent.process(image_path, damage_detections)
    
    state['part_identification_result'] = result
    return state

def run_severity_assessment(state: GraphState) -> GraphState:
    """Runs the Severity Assessment Agent and updates the state."""
    state['processing_log'].append("Step 4: Assessing Severity...")
    damaged_parts = state['part_identification_result']['damaged_parts']
    
    result = severity_agent.process(damaged_parts)
    
    state['severity_assessment_result'] = result
    return state

def compile_final_report(state: GraphState) -> GraphState:
    """Compiles the final assessment report from all agent outputs."""
    state['processing_log'].append("Step 5: Compiling Final Report...")
    time.sleep(0.5) # Simulate report generation time
    
    # Handle the case where the image was rejected
    if not state['quality_check_result']['processable']:
        state['error_message'] = "Image quality is too low to process."
        state['final_report'] = {
            "claim_id": state['claim_id'],
            "assessment_result": {
                "quality_check": {
                    "passed": False,
                    "issues": state['quality_check_result']['issues']
                }
            }
        }
        state['processing_log'].append("Process Halted: Image Rejected.")
        return state

    # Compile the full success report
    quality_res = state['quality_check_result']
    damage_res = state['damage_detection_result']
    part_res = state['part_identification_result']
    severity_res = state['severity_assessment_result']

    # Create the final annotations by merging part and damage info
    annotations = []
    for part in part_res['damaged_parts']:
        annotations.append({
            "damage_type": part['damage_type'],
            "part": part['part_name'],
            "bbox": part['bbox'],
            "confidence": next((d['confidence'] for d in damage_res['detections'] if d['bbox'] == part['bbox']), 0.9),
            "severity": DAMAGE_TO_SEVERITY_MAPPING.get(part['damage_type'], "moderate")
        })

    report = {
        "claim_id": state['claim_id'],
        "assessment_result": {
            "quality_check": {
                "passed": True,
                "average_quality": quality_res['quality_score']
            },
            "damage_summary": {
                "total_damages_found": len(damage_res['detections']),
                "affected_parts": [p['part_name'] for p in part_res['damaged_parts']],
                "overall_severity": severity_res['overall_severity'],
                "confidence_score": round(sum(d['confidence'] for d in damage_res['detections']) / len(damage_res['detections']), 2) if damage_res['detections'] else 0
            },
            "annotations": [{"image_id": state['image_path'].split('/')[-1], "detections": annotations}],
            "repair_estimate": {
                "cost_range": severity_res['estimated_cost_range'],
                "repair_days": severity_res['repair_time_days'],
                "category": severity_res['repair_category']
            },
            "fraud_indicators": {
                "image_manipulation_detected": quality_res.get('manipulation_detected', False),
                "consistency_score": 0.95 # Mocked for now
            }
        },
        "agent_metrics": {
            "image_quality": int(quality_res['processing_time_ms']),
            "damage_detection": int(damage_res['processing_time_ms']),
            "part_identification": int(part_res['processing_time_ms']),
            "severity_assessment": int(severity_res['processing_time_ms'])
        }
    }
    
    state['final_report'] = report
    state['processing_log'].append("Process Complete.")
    return state

# --- 3. Define Conditional Edge ---
def should_continue(state: GraphState) -> str:
    """Determines the next step based on the image quality check."""
    if state['quality_check_result']['processable']:
        return "continue_processing"
    else:
        return "terminate_processing"

# --- 4. Build the Graph ---
def build_graph():
    """Builds and compiles the LangGraph for damage assessment."""
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("quality_check", run_quality_check)
    workflow.add_node("damage_detection", run_damage_detection)
    workflow.add_node("part_identification", run_part_identification)
    workflow.add_node("severity_assessment", run_severity_assessment)
    workflow.add_node("compile_report", compile_final_report)

    # Set the entry point
    workflow.set_entry_point("quality_check")

    # Add conditional edge from quality check
    workflow.add_conditional_edges(
        "quality_check",
        should_continue,
        {
            "continue_processing": "damage_detection",
            "terminate_processing": "compile_report"
        }
    )

    # Add sequential edges for the main workflow
    workflow.add_edge("damage_detection", "part_identification")
    workflow.add_edge("part_identification", "severity_assessment")
    workflow.add_edge("severity_assessment", "compile_report")

    # The final report node is the end of the graph
    workflow.add_edge("compile_report", END)

    # Compile the graph into a runnable app
    return workflow.compile()

# --- Helper for importing in other files ---
# This avoids running the build process every time the file is imported.
# We create a single, compiled instance of the graph.
damage_assessment_graph = build_graph()

# Dummy import to satisfy the final report compilation logic
from utils.config import DAMAGE_TO_SEVERITY_MAPPING