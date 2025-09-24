import gradio as gr
import time
import uuid
import json
from PIL import Image

# Import the compiled LangGraph orchestrator and the state definition
from orchestrator.damage_assessment_graph import damage_assessment_graph, GraphState
from ui.utils import draw_annotations

def process_damage_claim(image_upload):
    """
    The main function that processes the user's request. It streams the
    pipeline's progress back to the Gradio UI.
    """
    if image_upload is None:
        yield {
            status_textbox: gr.update(value="Please upload an image first.", visible=True),
        }
        return

    claim_id = f"CLM-{str(uuid.uuid4())[:8].upper()}"

    # --- Initial State for the Graph ---
    initial_state = GraphState(
        claim_id=claim_id,
        image_path=image_upload,
        processing_log=[],
        error_message=None,
        quality_check_result=None,
        damage_detection_result=None,
        part_identification_result=None,
        severity_assessment_result=None,
        final_report=None
    )

    # --- Stream the Graph Execution ---
    # This allows us to get real-time updates from the orchestrator.
    final_state = None
    for state_update in damage_assessment_graph.stream(initial_state):
        # The key of the dictionary is the name of the node that just ran
        node_name = list(state_update.keys())[0]
        node_output = state_update[node_name]
        
        # Update the UI with the latest processing log
        log_message = "\n".join(node_output['processing_log'])
        yield {
            status_textbox: gr.update(value=log_message, visible=True),
            # Clear previous results while processing
            annotated_image: gr.update(value=None),
            report_json: gr.update(value=None)
        }
        final_state = node_output # Keep track of the latest full state
        time.sleep(0.5) # Add a small delay for better UX

    # --- Final Update after Processing is Complete ---
    final_report = final_state.get('final_report', {})
    
    # Draw annotations on the image
    annotated_img_array = draw_annotations(image_upload, final_report)
    
    # Convert the final report dictionary to a formatted JSON string for display
    report_str = json.dumps(final_report, indent=2)

    yield {
        status_textbox: gr.update(value=final_state['processing_log'][-1]), # Show final status
        annotated_image: gr.update(value=annotated_img_array, visible=True),
        report_json: gr.update(value=report_str, visible=True)
    }


# --- Build the Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(), title="Vehicle Damage Assessment") as demo:
    gr.Markdown("# Multi-Agent ML System for Vehicle Damage Detection")
    gr.Markdown("Upload an image of a damaged vehicle to see the automated assessment pipeline in action.")

    with gr.Row():
        with gr.Column(scale=1):
            # Input components
            input_image = gr.Image(type="filepath", label="Upload Vehicle Image")
            submit_button = gr.Button("Assess Damage", variant="primary")
            
            gr.Markdown("---")
            status_textbox = gr.Textbox(
                label="Processing Status", 
                lines=6, 
                interactive=False, 
                visible=True,
                placeholder="Pipeline progress will be shown here..."
            )

        with gr.Column(scale=2):
            # Output components
            with gr.Row():
                original_image_display = gr.Image(label="Original Image", interactive=False)
                annotated_image = gr.Image(label="Annotated Damage", interactive=False)
            
            report_json = gr.JSON(label="Assessment Report", visible=True)

    # --- Event Handling ---
    # When the button is clicked, run the processing function
    submit_button.click(
        fn=process_damage_claim,
        inputs=[input_image],
        outputs=[status_textbox, annotated_image, report_json]
    )

    # Also display the original image in the output panel upon upload
    input_image.change(
        fn=lambda x: x, 
        inputs=input_image, 
        outputs=original_image_display
    )

if __name__ == "__main__":
    demo.launch()