# Multi-Agent System for Vehicle Damage Assessment

This project implements a sophisticated multi-agent machine learning system designed to automate the process of vehicle damage assessment for insurance claims. It leverages a series of specialized AI agents, orchestrated by LangGraph, to analyze images of damaged vehicles, identify the type and location of damage, map it to specific car parts, and provide a final assessment report.

The system is powered by fine-tuned YOLOv8 models for high-accuracy damage and part detection, and features a step-by-step interactive web dashboard built with Gradio for transparent and intuitive analysis.

## ✨ Core Features

*   **Automated Assessment Pipeline**: An end-to-end workflow that takes an image and produces a detailed damage report.
*   **Multi-Agent Orchestration**: Utilizes four distinct agents (Quality, Damage, Parts, Severity) coordinated by LangGraph for a modular and robust workflow.
*   **Real-Time YOLO Integration**: Integrates two custom-trained YOLOv8 models for:
    1.  **Damage Detection**: Identifying various types of damage (cracks, scratches, dents).
    2.  **Part Segmentation**: Locating specific vehicle parts (bumpers, doors, lights).
*   **Intelligent Damage Mapping**: Automatically associates detected damages with vehicle parts using Intersection over Union (IoU) calculations.
*   **Step-by-Step Visualization**: The Gradio dashboard provides a linear, real-time view of the pipeline, showing the visual output of each agent as it completes its task.
*   **Modular and Scalable**: The agent-based architecture makes it easy to update, replace, or add new models and capabilities without rewriting the core logic.

## 🏗️ System Architecture

The system is designed as a stateful graph where each node represents an agent performing a specific task. The state (data) flows through the graph, being enriched at each step.

**Workflow:**
`Image Upload` -> **Image Quality Agent** -> `(Proceed/Reject)` -> **Damage Detection Agent (YOLO)** -> **Part Identification Agent (YOLO + IoU)** -> **Severity Assessment Agent** -> `Final Report`

*   **Orchestrator (LangGraph)**: The central "brain" that manages the workflow, directs data between agents, and handles conditional logic (e.g., rejecting a low-quality image).
*   **Agents**: Self-contained Python classes responsible for a single task. Currently, the Damage and Part agents use real ML models, while Quality and Severity are mock implementations.
*   **User Interface (Gradio)**: A web-based dashboard that allows for image uploads and visualizes the entire process in real-time.

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` and `virtualenv` (recommended)
*   PyTorch with CUDA support (recommended for GPU acceleration)

### 1. Installation

First, clone the repository and set up the environment.

```bash
# Clone the repository
git clone <your-repo-url>
cd vehicle-damage-assessment

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the required Python packages
pip install -r requirements.txt
```

### 2. Model Setup

This system requires two pre-trained YOLO model files (`.pt`).

**Place your trained models in the project's root directory** with the following exact filenames:

*   `damage_detection_yolo.pt`: Your model trained to detect different types of damage.
*   `part_detection_yolo.pt`: Your model trained to detect vehicle parts.

### 3. Configure Class Maps

Your models have specific class names and indices. You **must** update the Python dictionaries in the agent files to match your models for the system to work correctly.

*   **For Damage Detection**: Open `agents/damage_detection_agent.py` and update the `MODEL_DAMAGE_CLASS_MAP` dictionary.
*   **For Part Identification**: Open `agents/part_identification_agent.py` and update the `PART_CLASS_MAP` dictionary.

### 4. Running the Application

Once the installation and model setup are complete, you can launch the Gradio web application.

```bash
python main.py
```

The application will start, and you will see a URL in your terminal, typically `http://127.0.0.1:7860`. Open this URL in your web browser.

## 💻 How to Use the Dashboard

1.  **Upload Image**: Drag and drop an image of a damaged vehicle into the upload box on the left. The original image will appear on the right.
2.  **Assess Damage**: Click the "Assess Damage" button to start the pipeline.
3.  **Observe Real-Time Progress**: Watch as the collapsible sections below appear one by one:
    *   **Step 1: Image Quality Check**: Shows the results of the initial quality scan.
    *   **Step 2: Damage Detection**: Displays the image with all detected damages highlighted in blue.
    *   **Step 3: Damaged Part Identification**: Shows the result of the mapping logic. Successfully mapped damages are shown in **orange**, while unmapped damages are highlighted in **red**.
    *   **Step 4: Final Report**: Presents the final annotated image with color-coded severity and the complete JSON assessment report.

## 📂 Project Structure

```
vehicle-damage-assessment/
├── agents/
│   ├── damage_detection_agent.py     # Agent with real YOLO model for damage
│   ├── part_identification_agent.py  # Agent with real YOLO model for parts
│   ├── image_quality_agent.py      # Mock agent for quality checks
│   └── severity_assessment_agent.py    # Mock agent for final severity scoring
│
├── orchestrator/
│   ├── graph_state.py                # Defines the data structure for the workflow
│   └── damage_assessment_graph.py      # Builds and compiles the LangGraph orchestrator
|
├── models /
│   ├── damage.pt                # Damage Detection Model Fine Tuned YOlOv8n
│   └── part.pt                  # Part Detection odel Fine Tuned YOlOv8n
|
├── ui/
│   ├── app.py                        # The main Gradio application file
│   └── utils.py                      # Helper functions for drawing annotations on images
│
├── utils/
│   ├── config.py                     # Stores shared constants (damage types, etc.)
│   └── geometry.py                   # Contains geometry functions like calculate_iou
│
├── main.py                           # Entry point to launch the Gradio app
├── requirements.txt                  # Project dependencies
└── README.md                         # This file
```