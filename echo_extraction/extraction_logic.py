# echo_extraction/extraction_logic.py

import logging
import json
import textwrap
import os
from typing import Dict, Any, Type, Union, List, Optional
from pydantic import BaseModel, ValidationError, Field
from .llm_setup import get_extraction_chain, get_feedback_chain, get_json_parser, is_langchain_available
from .schema_helpers import format_validation_errors_for_agent, format_pydantic_errors_for_book 
from .models import EchoReport
from .llm_mapping_utils import remap_llm_keys


# Get a logger specific to this module
logger = logging.getLogger(__name__)

def generate_feedback(
    report: str,
    raw_llm_output: str,
    error_details: Union[List[Dict[str, Any]], str],
    full_echo_schema: Dict[str, Any]
) -> str:
    """
    Uses the feedback agent LLM to generate constructive feedback based on errors.
    """
    feedback_agent_chain = get_feedback_chain()
    if not is_langchain_available() or feedback_agent_chain is None:
        logger.error("Langchain components or feedback agent chain not available. Cannot generate feedback.")
        return "Could not generate specific feedback due to missing components. Please ensure output is valid JSON and matches the schema."

    feedback_input_details = ""
    if isinstance(error_details, list): # Pydantic errors
        feedback_input_details = format_validation_errors_for_agent(error_details, full_echo_schema)
    elif isinstance(error_details, str): # JSON parsing or other string error
        feedback_input_details = f"Error Detail:\n{error_details}\n\n"
        try:
            full_schema_start = json.dumps(full_echo_schema, indent=2)[:500] + "..."
            feedback_input_details += f"Expected overall JSON structure starts like:\n```json\n{full_schema_start}\n```"
        except Exception as e:
            feedback_input_details += f"Could not generate full schema snippet for feedback: {e}"
    else:
        feedback_input_details = f"Unknown error type for feedback generation: {type(error_details)}"

    try:
        feedback_response = feedback_agent_chain.invoke({
            "report": report,
            "raw_llm_output": raw_llm_output,
            "error_details": feedback_input_details,
        })
        generated_feedback = feedback_response.strip()
        return generated_feedback
    except Exception as e:
        return f"An error occurred while generating specific feedback ({e}). Please ensure your output is ONLY valid JSON and strictly conforms to the schema."


def extract_component_data(
    report: str,
    component_model: Type[BaseModel],
    max_attempts: int = 5
) -> BaseModel:
    """
    Extracts data for a specific component, logging details for the Markdown book.
    """
    if not is_langchain_available():
        logger.error("LLM functionality is disabled. Cannot perform extraction.")
        raise RuntimeError("LLM functionality is disabled. Cannot perform extraction.")

    main_extraction_chain = get_extraction_chain()
    json_parser = get_json_parser()
    full_echo_schema = EchoReport.model_json_schema() 

    if main_extraction_chain is None or json_parser is None:
        logger.error("LLM chains or parser not initialized correctly.")
        raise RuntimeError("LLM chains or parser not initialized correctly.")

    component_name = component_model.__name__
    # Get the Pydantic schema for error reporting and validation
    pydantic_component_schema = component_model.model_json_schema()
    
    # Load schema from JSON file instead of Pydantic model for the extraction prompt
    schema_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'JSON_Schema')
    # Try both .json and .schema.json extensions
    possible_filenames = [f"{component_name}.json", f"{component_name}.schema.json"]
    schema_path = None
    for fname in possible_filenames:
        candidate = os.path.join(schema_dir, fname)
        if os.path.isfile(candidate):
            schema_path = candidate
            break
    if not schema_path:
        raise FileNotFoundError(f"Schema file for component '{component_name}' not found in {schema_dir}.")
    with open(schema_path, 'r') as f:
        json_component_schema = json.load(f)
    component_schema_str = json.dumps(json_component_schema, indent=2)
    
    # Log the start of processing for this component (for the book)
    logger.info(f"Starting component: {component_name}", extra={
        'log_type': 'COMPONENT_START',
        'component_name': component_name
    })

    feedback = ""  # Initial empty feedback
    last_error_for_runtime_exception = None # To store the very last error if all attempts fail

    for i in range(1, max_attempts + 1):
        # Prepare a dictionary to hold all data for the current attempt's log entry
        attempt_log_data = {
            'log_type': 'ATTEMPT_PROCESSED', # This will be recognized by MarkdownBookFormatter
            'component_name': component_name,
            'attempt_num': i,
            'max_attempts': max_attempts,
            'status': 'Processing', # Initial status
            'extractor_input': {},
            'extractor_raw_output': 'Not yet generated.',
            'feedback_output': feedback if feedback else "No feedback provided (first attempt or previous success).", # Log current feedback
            'errors': [] # List to store errors for this attempt
        }
        
        # Populate extractor_input for the log
        # This is the actual input to the main_extraction_chain.invoke
        current_llm_input = {
            "report": report, # Full report is part of the input
            "feedback": feedback,
            "schema": component_schema_str, # Component-specific JSON schema
            "schema_name": component_name # Add the component name
        }
        attempt_log_data['extractor_input'] = current_llm_input

        logger.info(f"Attempt {i}/{max_attempts} for {component_name}...")

        try:
            response = main_extraction_chain.invoke(current_llm_input)
            raw_output = response.strip()
            attempt_log_data['extractor_raw_output'] = raw_output

            parsed_data = json_parser.parse(raw_output)
            # Remap keys to match model fields before validation
            remapped_data = remap_llm_keys(parsed_data, component_model.__fields__)
            validated_component = component_model.model_validate(remapped_data)
            
            attempt_log_data['status'] = 'Successful'
            # Log successful attempt details to the book
            logger.info(f"Attempt {i} for {component_name} successful.", extra=attempt_log_data)
            return validated_component

        except json.JSONDecodeError as jde:
            last_error_for_runtime_exception = jde
            attempt_log_data['status'] = 'Failed'
            error_message = f"Failed to parse output as valid JSON: {jde}"
            
            attempt_log_data['errors'].append({
                'id': f'E{len(attempt_log_data["errors"]) + 1}', 
                'message': error_message,
                'schema_snippet': "N/A for JSON parsing error. Check raw LLM output for syntax issues."
            })
            
            # Generate feedback for the next attempt
            feedback = generate_feedback(report, raw_output, error_message, full_echo_schema)
            attempt_log_data['feedback_output'] = feedback
            # Log failed attempt details to the book
            logger.error(f"Attempt {i} for {component_name} failed: JSON Parse Error.", extra=attempt_log_data)

        except ValidationError as ve:
            last_error_for_runtime_exception = ve
            attempt_log_data['status'] = 'Failed'
            
            formatted_pyd_errors = format_pydantic_errors_for_book(ve.errors(), pydantic_component_schema, component_name)
            attempt_log_data['errors'].extend(formatted_pyd_errors)
            
            # Generate feedback for the next attempt
            feedback = generate_feedback(report, raw_output, ve.errors(), full_echo_schema)
            attempt_log_data['feedback_output'] = feedback
            logger.error(f"Attempt {i} for {component_name} failed: Validation Error.", extra=attempt_log_data)

        except Exception as e:
            last_error_for_runtime_exception = e
            attempt_log_data['status'] = 'Failed'
            error_message = f"An unexpected error occurred during attempt {i} for {component_name}: {e}"
            
            attempt_log_data['errors'].append({
                'id': f'E{len(attempt_log_data["errors"]) + 1}',
                'message': error_message,
                'schema_snippet': "N/A for unexpected error."
            })
            
            # Generate feedback for the next attempt
            feedback = generate_feedback(report, raw_output, error_message, full_echo_schema)
            attempt_log_data['feedback_output'] = feedback
            logger.error(f"Attempt {i} for {component_name} failed: Unexpected Error.", extra=attempt_log_data)

    # If loop finishes, all attempts failed. The last attempt's failure is already logged.
    logger.error(f"Extraction for {component_name} FAILED After {max_attempts} Attempts.")
    raise RuntimeError(f"Failed to extract and validate data for {component_name} after {max_attempts} attempts. Last error: {last_error_for_runtime_exception}")

