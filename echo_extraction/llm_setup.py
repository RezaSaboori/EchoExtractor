# echo_extraction/llm_setup.py

import logging
import json
import os
from typing import Dict, Any, Type, Union
from dotenv import load_dotenv

# Attempt to import Langchain components and JsonOutputParser
try:
    # Use the updated import for Ollama from langchain_community
    from langchain_community.llms import Ollama
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser # Import JsonOutputParser
    from langchain_core.runnables import RunnableSequence # Explicitly import RunnableSequence
    from pydantic import BaseModel # Import BaseModel for type hinting

    LANGCHAIN_AVAILABLE = True
except ImportError:
    logging.warning("Langchain components or JsonOutputParser not found. LLM functionality will be disabled.")
    LANGCHAIN_AVAILABLE = False
    # Define dummy classes if Langchain is not available
    class Ollama:
        def __init__(self, *args, **kwargs):
            pass
        def invoke(self, *args, **kwargs):
            raise NotImplementedError("Langchain is not installed.")
    class PromptTemplate:
        def __init__(self, *args, **kwargs):
            pass
    class JsonOutputParser: # Dummy parser
        def parse(self, text: str) -> Dict[str, Any]:
            raise NotImplementedError("Langchain is not installed.")
    class RunnableSequence: # Dummy RunnableSequence
        def __init__(self, *args, **kwargs):
            pass
        def invoke(self, *args, **kwargs):
            raise NotImplementedError("Langchain is not installed.")
    class BaseModel: # Dummy BaseModel
        pass

# Load environment variables from .env file
load_dotenv()

# Define directories and paths
LOG_FILE_DIR = os.getenv("LOG_FILE_DIR", "/your/actual/path/to/logs")
FINAL_REPORTS_DIR = os.getenv("FINAL_REPORTS_DIR", "/your/actual/path/to/final_reports")
ABBREVIATION_CSV_PATH = os.getenv("ABBREVIATION_CSV_PATH", "/your/actual/path/to/echo_abb_merged_csv.csv")
REPORTS_JSON_PATH = os.getenv("REPORTS_JSON_PATH", "/your/actual/path/to/CTICI_NCIBB_Echo_Sample.json")
ABBREVIATIONS_OUTPUT_JSON_PATH = os.getenv("ABBREVIATIONS_OUTPUT_JSON_PATH", "/your/actual/path/to/abbreviations.json")

# ── LLM Initialization ───────────────────────────────────────────────────────
# Initialize the main extraction LLM
# Using cogito:70b as specified, ensure it's pulled and running
try:
    ollama_model_name = os.getenv("OLLAMA_MODEL_NAME", "your_ollama_model")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL") 

    if ollama_base_url:
        main_extraction_llm = Ollama(model=ollama_model_name, temperature=0.0, base_url=ollama_base_url) if LANGCHAIN_AVAILABLE else None
        feedback_llm = Ollama(model=ollama_model_name, temperature=0.0, base_url=ollama_base_url) if LANGCHAIN_AVAILABLE else None
    else:
        main_extraction_llm = Ollama(model=ollama_model_name, temperature=0.0) if LANGCHAIN_AVAILABLE else None
        feedback_llm = Ollama(model=ollama_model_name, temperature=0.0) if LANGCHAIN_AVAILABLE else None
except Exception as e:
    logging.error(f"Failed to initialize Ollama models: {e}")
    main_extraction_llm = None
    feedback_llm = None
    LANGCHAIN_AVAILABLE = False # Disable if LLM initialization fails

# Initialize the JsonOutputParser
json_parser = JsonOutputParser() if LANGCHAIN_AVAILABLE else JsonOutputParser() # Use dummy if not available

# ── Prompt Templates ─────────────────────────────────────────────────────────

# Prompt for the main extraction LLM - expects report, feedback, schema, AND schema_name
# Modified to accept a specific component schema and its name
main_extraction_prompt = PromptTemplate(
    input_variables=["report", "feedback", "schema", "schema_name"],
    template="""
You are an AI with comprehend knowledge of Cardiology and Echocardiography that extracts *just* the information relevant to the specific component described by the provided JSON schema from an echo-report into a JSON object.
You are currently extracting data for the {schema_name} component.
The output must be a valid JSON object that strictly conforms to the expected structure defined by the provided JSON schema.
Do NOT include any other text before or after the JSON.
DO NOT infer any information from the report that is not explicitly stated in the schema (for example, if the report says "EF:50%" for a field, do not infer systolic function is normal).
PAY ATTENTION TO THE UNITS OF THE REPORT AND THE SCHEMA. IF THE UNITS ARE NOT THE SAME, CONVERT THE UNITS TO THE UNITS EXPECTED BY THE SCHEMA.

**Here is the Echo Report Text:
```
{report}
```

---
Expected JSON Schema for the {schema_name} component (the descriptions and max/min are for your hint only):
```json
{schema}
```
---
Previous Attempt Feedback (if any):
{feedback}
---

Based on the Echo Report text, the Expected JSON Schema for the specific component, and any feedback provided, generate the JSON output conforming to the expected structure.
If there was previous feedback, carefully review it and correct your output.
Output JSON:
```json
{{
""".strip() # Keep the start of the JSON structure in the prompt
)

# Prompt for the Feedback Agent LLM
feedback_agent_prompt = PromptTemplate(
    # Added 'report' to input_variables
    input_variables=["report", "raw_llm_output", "error_details"],
    template="""
You are a feedback agent for another Agent that extracts structured data from echo reports into JSON.
Your task is to analyze the original echo report text, the previous attempt's output, and the errors,
and generate clear, actionable feedback to help the Agent correct its next attempt.

Original Echo Report Text:
```
{report}
```

Here is the raw output from the Agents previous attempt:
```
{raw_llm_output}
```

Here are the details about the error(s) encountered, including relevant schema snippets for each error:
```
{error_details}
```

Analyze the original report text, the previous output, the error details, and the provided schema snippets.
For each error listed in the details:
- Identify the specific issue (e.g., incorrect value type, missing field, extra text, wrong enum value) by looking at the error message, path, and the corresponding schema snippet.
- Pay close attention to the 'description', 'enum' (possible values), and 'default' attributes in the schema snippet.
- Generate concise and highly specific feedback for the main AI.
- Focus on telling the AI *what* was wrong, *where* it was wrong (using the path), and *how* to fix it based on the schema and report text.
- Hint the agent about the description, possible values, default values, and value types mentioned in the schema snippet for the problematic field.
- For the range errors, Help the model to CHANGE and CONVERT the Units if needed for example if the unit in the Report is in cm but the schema expects mm, then convert it to mm by multiplying it by 10.
- Remember that the default value for many fields is often 'Not Measured' or 'Not Assessed' unless specified differently in the schema.
- **CONSIDER TO GENERATE THE FEEDBACK IN LIST FORMAT, AND COVER ALL ERRORS MENTIONED IN THE ERROR DETAILS.**

Example Feedback Points (Adapt to specific errors and schema):
- "Error at path 'measurements.pericardial_thickness': The value 'Thick' is invalid. According to the schema, 'Pericardial Thickness' expects a number or 'Not Measured', and values should be between 0.5 and 10.0 mm. Check the schema snippet provided for this error."
- "Error at path 'assessment.effusion.size': The value 'Mild' is not a valid enum value for 'Effusion Size'. Refer to the schema snippet for valid options ('Small', 'Small to Moderate', 'Moderate', 'Moderate to Large', 'Large', 'Not Assessed')."
- "Error at path 'assessment.effusion.hemodynamic_impact': This field is missing, but required by the schema. Add the 'Hemodynamic Impact' field to the 'Effusion' object, using one of the valid enum values from the schema snippet."
- "JSON Parsing Error: Your output contained text before or after the JSON object, or had invalid syntax."
""".strip()
)

# ── Runnable Chains ────────────────────────────────────────────────────────
# Chain for the main extraction LLM (Prompt -> LLM)
main_extraction_chain = main_extraction_prompt | main_extraction_llm if LANGCHAIN_AVAILABLE else None

# Chain for the Feedback Agent LLM (Prompt -> LLM)
feedback_agent_chain = feedback_agent_prompt | feedback_llm if LANGCHAIN_AVAILABLE else None

# ── Helper Function to get chains ──────────────────────────────────────────
def get_extraction_chain() -> Union[RunnableSequence, None]:
    """Returns the main extraction Langchain runnable chain."""
    if not LANGCHAIN_AVAILABLE:
        logging.error("Langchain is not available. Extraction chain cannot be provided.")
        return None
    return main_extraction_chain

def get_feedback_chain() -> Union[RunnableSequence, None]:
    """Returns the feedback agent Langchain runnable chain."""
    if not LANGCHAIN_AVAILABLE:
        logging.error("Langchain is not available. Feedback chain cannot be provided.")
        return None
    return feedback_agent_chain

def get_json_parser() -> Union[JsonOutputParser, None]:
    """Returns the JsonOutputParser instance."""
    if not LANGCHAIN_AVAILABLE:
          # Return the dummy parser if Langchain is not available
          return JsonOutputParser()
    return json_parser

def is_langchain_available() -> bool:
    """Checks if Langchain components are available."""
    return LANGCHAIN_AVAILABLE

