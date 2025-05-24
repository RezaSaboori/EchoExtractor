# Echo Report Extractor

## 1. Overview

The Echo Report Extractor is a Python application designed to process unstructured echocardiogram (echo) report texts, extract clinically relevant information, and structure it into a standardized JSON format. It leverages Large Language Models (LLMs) through the Langchain framework, specifically using an Ollama-hosted model, to interpret and parse the medical text. The system performs abbreviation expansion, modular data extraction for various cardiac components, and iterative feedback-driven refinement to ensure accuracy and completeness of the extracted data.

## 2. Features

-   **Abbreviation Expansion**: Automatically replaces common medical abbreviations in echo reports with their full forms using a customizable CSV dictionary.
-   **Modular LLM-based Extraction**: Extracts data for distinct cardiac components (e.g., Left Ventricle, Aortic Valve, Pericardium) independently using specific Pydantic schemas.
-   **Iterative Refinement with Feedback**: If initial LLM extraction fails validation against the schema, a feedback mechanism generates corrective prompts for subsequent attempts.
-   **Structured Output**: Produces a final JSON output conforming to a detailed Pydantic model (`EchoReport`), ensuring data consistency.
-   **Comprehensive Logging**: Generates detailed logs of the extraction process, including inputs, LLM outputs, feedback loops, and errors, suitable for review and debugging. Log files are saved in Markdown format.
-   **Environment Configuration**: Utilizes a `.env` file for easy configuration of model names, API endpoints, and file paths.
-   **Batch Processing**: Can process multiple echo reports from a single input JSON file.

## 3. Directory Structure

```
main_app/
├── .git/                       # Git repository files
├── .gitignore                  # Specifies intentionally untracked files that Git should ignore
├── echo_extraction/            # Core extraction logic and models
│   ├── __pycache__/            # Python bytecode cache
│   ├── llm_setup.py            # Configures Langchain, Ollama LLM, and prompt templates
│   ├── utils.py                # Utility functions (e.g., logging setup)
│   ├── abbreviation_processor.py # Handles abbreviation expansion
│   ├── models.py               # Defines Pydantic models for structured echo data
│   ├── extraction_logic.py     # Core logic for component-wise data extraction and feedback
│   ├── __init__.py             # Makes the directory a Python package
│   ├── schema_helpers.py       # Helper functions for schema and error formatting
│   └── echo_abb_merged_csv.csv # CSV file containing medical abbreviations and their full forms
├── final_reports/              # Output directory for successfully processed structured JSON reports
├── logs/                       # Output directory for detailed Markdown logs of each report processing
├── requirements.txt            # Python package dependencies
├── .env                        # Environment variable configuration (API keys, paths, model names)
├── main.py                     # Main script to run the echo report extraction process
└── CTICI_NCIBB_Echo_Sample.json # Sample input JSON file containing echo reports
```

## 4. Setup and Installation

### 4.1. Prerequisites

-   Python 3.8+
-   An Ollama instance running with a compatible model (e.g., `cogito:70b` or as specified in `.env`).
-   Git (for cloning the repository).

### 4.2. Cloning the Repository

```bash
git clone <repository_url>
cd main_app
```

### 4.3. Setting up the Environment

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 4.4. Installing Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4.5. Environment Variables

Create a `.env` file in the `main_app` root directory by copying the example or creating a new one. This file is used to configure paths, Ollama model details, and other settings.

Example `.env` content:

```env
# --- Ollama Configuration ---
OLLAMA_MODEL_NAME="your_ollama_model_name:tag"  # e.g., "mistral:latest", "cogito:70b"
# OLLAMA_BASE_URL="http://localhost:11434"    # Uncomment and set if Ollama runs on a different host/port

# --- File Paths (Defaults are usually fine if running from main_app directory) ---
LOG_FILE_DIR="./logs"
FINAL_REPORTS_DIR="./final_reports"
ABBREVIATION_CSV_PATH="./echo_extraction/echo_abb_merged_csv.csv"
REPORTS_JSON_PATH="./CTICI_NCIBB_Echo_Sample.json" # Path to the input JSON file with reports
# ABBREVIATIONS_OUTPUT_JSON_PATH="./abbreviations.json" # Optional: path for an output JSON of abbreviations (if functionality is added)
```

**Important**:
-   Ensure the `OLLAMA_MODEL_NAME` matches a model available in your Ollama instance.
-   The file paths (`LOG_FILE_DIR`, `FINAL_REPORTS_DIR`, etc.) can be absolute or relative to the `main_app` directory. The defaults are set to relative paths.

## 5. Usage

To run the echo report extraction process, execute the `main.py` script from the `main_app` directory:

```bash
python main.py
```

The script will:
1.  Load echo reports from the JSON file specified by `REPORTS_JSON_PATH` (default: `CTICI_NCIBB_Echo_Sample.json`).
2.  For each report:
    a.  Set up a dedicated Markdown log file in the `LOG_FILE_DIR` (default: `logs/`).
    b.  Process abbreviations using the `ABBREVIATION_CSV_PATH`.
    c.  Perform modular extraction of cardiac components.
    d.  If successful, save the structured JSON output to `FINAL_REPORTS_DIR` (default: `final_reports/`) with a filename corresponding to the report's `_id`.
    e.  Log the detailed process, including LLM interactions and any errors, to the Markdown log file.
3.  Print progress and status messages to the console.

## 6. Key Components

-   **`main.py`**: The entry point of the application. It orchestrates the loading of reports, processing each report through the extraction pipeline, and saving the results.
-   **`echo_extraction/`**: This package contains the core logic:
    -   **`llm_setup.py`**: Initializes and configures the Langchain LLM (Ollama), prompt templates for extraction and feedback generation, and the JSON output parser.
    -   **`models.py`**: Defines a comprehensive set of Pydantic models that dictate the structure of the extracted echo report data. This includes detailed schemas for cardiac chambers, valves, great vessels, congenital defects, and the pericardium.
    -   **`extraction_logic.py`**: Implements the iterative extraction process. It calls the LLM for each component, validates the output against the Pydantic models, and uses a feedback loop with another LLM chain to refine prompts if validation fails.
    -   **`abbreviation_processor.py`**: Handles the preprocessing of report text to expand abbreviations based on a provided CSV file.
    -   **`utils.py`**: Contains utility functions, primarily for setting up the detailed Markdown logging.
    -   **`schema_helpers.py`**: Provides functions to format Pydantic validation errors and schema information for logging and feedback generation.
-   **`CTICI_NCIBB_Echo_Sample.json`**: The input file containing an array of echo reports. Each report object in the JSON array should have an `_id` (for naming output files) and a `data` field containing the raw echo report text.
-   **`echo_extraction/echo_abb_merged_csv.csv`**: A CSV file mapping abbreviations (column `Abbreviation`) to their full forms (column `FullForm`).

## 7. Input Data Format

The application expects input echo reports to be provided in a JSON file (specified by `REPORTS_JSON_PATH` in `.env`). The JSON file should contain a list of objects, where each object represents a single echo report and has at least the following keys:
-   `_id`: A unique identifier for the report (string). This ID will be used for naming the output log and JSON files.
-   `data`: The raw text content of the echocardiogram report (string).

Example:
```json
[
  {
    "_id": "report_001",
    "data": "Patient Name: John Doe... LV Ejection Fraction: 55% (Normal)... The mitral valve shows mild regurgitation..."
  },
  {
    "_id": "report_002",
    "data": "Echo findings: RVSP estimated at 30 mmHg. Aortic valve is trileaflet..."
  }
]
```

## 8. Output

-   **Structured JSON Reports**: For each successfully processed input report, a JSON file is created in the `FINAL_REPORTS_DIR`. The filename will be `<_id>.json` (e.g., `report_001.json`). This file contains the structured data extracted from the echo report, conforming to the `EchoReport` Pydantic model.
-   **Detailed Logs**: For each input report, a Markdown log file is created in the `LOG_FILE_DIR`. The filename will be `<_id>.md` (e.g., `report_001.md`). These logs provide a comprehensive trace of the extraction process, including:
    -   The original and abbreviation-processed report text.
    -   Details of each extraction attempt for every cardiac component.
    -   The exact input (prompt, schema, feedback) provided to the LLM.
    -   The raw output from the LLM.
    -   Validation errors encountered.
    -   Feedback generated for the LLM.

## 9. Troubleshooting and Error Handling

-   **Langchain Not Available**: If Langchain components are not installed or an Ollama model cannot be initialized, the script will print an error message, and LLM-dependent functionalities will be disabled or raise errors. Ensure `langchain-community`, `langchain-core` are installed and Ollama is running and accessible.
-   **Model Not Found**: Ensure the `OLLAMA_MODEL_NAME` in your `.env` file corresponds to a model that has been pulled and is available in your Ollama instance (e.g., via `ollama list`).
-   **File Not Found Errors**: Check the paths specified in your `.env` file (`REPORTS_JSON_PATH`, `ABBREVIATION_CSV_PATH`) and ensure they point to the correct locations.
-   **Extraction Failures**: If a report consistently fails extraction for certain components even after multiple attempts, review the corresponding Markdown log file in the `logs/` directory. This log will show the LLM's attempts, the errors, and the feedback provided, which can help diagnose issues with the prompts, the schema, or the LLM's interpretation for complex or ambiguous report sections. The Pydantic models in `models.py` define the expected structure; if the LLM struggles to conform, prompt engineering or model adjustments might be needed.

## 10. Customization

-   **LLM Model**: Change the `OLLAMA_MODEL_NAME` and optionally `OLLAMA_BASE_URL` in the `.env` file to use different Ollama-hosted models or instances.
-   **Abbreviations**: Update `echo_extraction/echo_abb_merged_csv.csv` to add, remove, or modify abbreviation definitions.
-   **Extraction Schema**: Modify the Pydantic models in `echo_extraction/models.py` to change the structure or fields of the data to be extracted. This will also require updating the corresponding logic in `main.py` that assembles the final `EchoReport`.
-   **Prompts**: The LLM prompts for extraction and feedback generation are defined in `echo_extraction/llm_setup.py`. These can be adjusted for fine-tuning the LLM's behavior.
<<<<<<< HEAD
-   **Maximum Extraction Attempts**: The number of attempts the system makes to extract data for a component before giving up can be changed by modifying the `max_attempts` parameter in the `extract_component_data` function calls within `main.py` or `extraction_logic.py`. 
=======
-   **Maximum Extraction Attempts**: The number of attempts the system makes to extract data for a component before giving up can be changed by modifying the `max_attempts` parameter in the `extract_component_data` function calls within `main.py` or `extraction_logic.py`. 
>>>>>>> d4b2fbd1aadd6bca2499a4de7fae6cbe30e9451d
