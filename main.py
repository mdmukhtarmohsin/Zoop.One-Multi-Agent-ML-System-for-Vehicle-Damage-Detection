from ui.app import demo
import os

def main():
    """
    Launches the Gradio web server for the Vehicle Damage Assessment application.
    """
    # Create a dummy directory for uploads if it doesn't exist, as Gradio might need it.
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        
    print("Launching Vehicle Damage Assessment Dashboard...")
    # The launch() method starts the web server.
    # share=True creates a public link, useful for sharing or Colab.
    # Set debug=True for hot-reloading during development.
    demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)

if __name__ == "__main__":
    main()