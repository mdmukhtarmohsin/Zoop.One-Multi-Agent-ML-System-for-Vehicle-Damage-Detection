import gradio as gr
import time
import uuid
import json

from orchestrator.damage_assessment_graph import damage_assessment_graph, GraphState
# Import all three drawing utilities now
from ui.utils import draw_annotations, draw_raw_detection_boxes, draw_part_assignments

def process_damage_claim(image_path, progress=gr.Progress(track_tqdm=True)):
    """
    Main processing function that streams step-by-step updates to the UI.
    """
    if image_path is None:
        gr.Warning("Please upload an image first!")
        return {
            quality_output_group: gr.update(visible=False),
            damage_output_group: gr.update(visible=False),
            parts_output_group: gr.update(visible=False),
            final_report_group: gr.update(visible=False),
        }

    # --- 1. Reset UI for a new run ---
    yield {
        quality_output_group: gr.update(visible=False),
        damage_output_group: gr.update(visible=False),
        parts_output_group: gr.update(visible=False),
        final_report_group: gr.update(visible=False),
    }

    claim_id = f"CLM-{str(uuid.uuid4())[:8].upper()}"
    initial_state = GraphState(
        claim_id=claim_id, image_path=image_path, processing_log=[],
        error_message=None, quality_check_result=None, damage_detection_result=None,
        part_identification_result=None, severity_assessment_result=None, final_report=None
    )

    # --- 2. Stream the graph and update UI at each step ---
    final_state = None
    for state_update in damage_assessment_graph.stream(initial_state):
        node_name = list(state_update.keys())[0]
        node_output = state_update[node_name]
        final_state = node_output

        if node_name == 'quality_check':
            qc_result = node_output['quality_check_result']
            status_text = f"Quality Score: {qc_result['quality_score']}\nProcessable: {qc_result['processable']}\nIssues: {qc_result['issues'] or 'None'}"
            yield {quality_status: gr.update(value=status_text), quality_output_group: gr.update(visible=True)}
            if not qc_result['processable']:
                gr.Error("Image quality too low. Process halted.")
                break

        elif node_name == 'damage_detection':
            dd_result = node_output['damage_detection_result']
            annotated_img = draw_raw_detection_boxes(image_path, dd_result)
            yield {
                damage_annotated_image: gr.update(value=annotated_img),
                damage_raw_json: gr.update(value=dd_result),
                damage_output_group: gr.update(visible=True)
            }

        elif node_name == 'part_identification':
            pi_result = node_output['part_identification_result']
            # --- NEW: Call the new drawing function for this step ---
            part_assignment_img = draw_part_assignments(image_path, pi_result)
            yield {
                # --- NEW: Update the new image component ---
                parts_annotated_image: gr.update(value=part_assignment_img),
                parts_identified_json: gr.update(value=pi_result),
                parts_output_group: gr.update(visible=True)
            }
        
        elif node_name == 'compile_report':
            final_report = node_output.get('final_report', {})
            final_annotated_img = draw_annotations(image_path, final_report)
            yield {
                final_annotated_image: gr.update(value=final_annotated_img),
                final_report_json: gr.update(value=final_report),
                final_report_group: gr.update(visible=True)
            }
        
        time.sleep(0.5)

# --- Build the New Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(), title="Vehicle Damage Assessment") as demo:
    gr.Markdown("# Multi-Agent Vehicle Damage Assessment")
    gr.Markdown("Upload an image to see the step-by-step analysis pipeline.")

    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(type="filepath", label="Upload Vehicle Image")
            submit_button = gr.Button("Assess Damage", variant="primary")
        with gr.Column(scale=2):
            original_image_display = gr.Image(label="Original Image", interactive=False)
    
    input_image.change(fn=lambda x: x, inputs=input_image, outputs=original_image_display)

    with gr.Accordion("Step 1: Image Quality Check", open=False) as quality_output_group:
        quality_status = gr.Textbox(label="Quality Assessment", interactive=False)
    
    with gr.Accordion("Step 2: Damage Detection (YOLO)", open=False) as damage_output_group:
        with gr.Row():
            damage_annotated_image = gr.Image(label="Detected Damage Areas")
            damage_raw_json = gr.JSON(label="Raw Detection Output")

    # --- NEW: Add an Image component to the Step 3 Accordion ---
    with gr.Accordion("Step 3: Damaged Part Identification (YOLO + IoU)", open=False) as parts_output_group:
        with gr.Row():
            parts_annotated_image = gr.Image(label="Damage Mapped to Parts")
            parts_identified_json = gr.JSON(label="Mapping Output")

    with gr.Accordion("Step 4: Final Assessment & Report", open=False) as final_report_group:
        with gr.Row():
            final_annotated_image = gr.Image(label="Final Annotated Image")
            final_report_json = gr.JSON(label="Comprehensive Report")

    # --- NEW: Add the new component to the list of all outputs ---
    all_outputs = [
        quality_status, quality_output_group,
        damage_annotated_image, damage_raw_json, damage_output_group,
        parts_annotated_image, parts_identified_json, parts_output_group,
        final_annotated_image, final_report_json, final_report_group
    ]

    submit_button.click(
        fn=process_damage_claim,
        inputs=[input_image],
        outputs=all_outputs
    )

if __name__ == "__main__":
    demo.launch()