import json
import copy
import textwrap
from typing import Dict, Any, List, Union


def resolve_ref(schema: Dict[str, Any], ref: str) -> Dict[str, Any]:
    """Resolves a JSON schema $ref pointer within the same schema document."""
    if not ref.startswith('#/'):
        return {"error": f"Cannot resolve external reference: {ref}"}
    parts = ref.split('/')[1:]
    current = schema
    try:
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return {"error": f"Failed to resolve reference part '{part}' at path {ref}"}
        return current
    except (KeyError, TypeError):
        return {"error": f"Failed to resolve reference: {ref}"}


def recursively_resolve_refs(snippet: Any, full_schema: Dict[str, Any], depth: int, max_depth: int = 5) -> Any:
    """
    Recursively resolves $ref pointers within a schema snippet up to a max depth.
    Returns a deep copy of the snippet with resolved references.
    """
    if depth >= max_depth or not isinstance(snippet, (dict, list)):
        return snippet
    resolved_snippet = copy.deepcopy(snippet)
    if isinstance(resolved_snippet, dict):
        if '$ref' in resolved_snippet and isinstance(resolved_snippet['$ref'], str):
            ref_val = resolved_snippet['$ref']
            resolved_target = resolve_ref(full_schema, ref_val)
            if 'error' not in resolved_target:
                return recursively_resolve_refs(resolved_target, full_schema, depth + 1, max_depth)
            else:
                resolved_snippet['$ref_error'] = resolved_target['error']
                return resolved_snippet
        else:
            for key, value in resolved_snippet.items():
                 if value is full_schema: # Avoid infinite recursion
                     continue
                 resolved_snippet[key] = recursively_resolve_refs(value, full_schema, depth + 1, max_depth)
    elif isinstance(resolved_snippet, list):
        for i, item in enumerate(resolved_snippet):
            if item is full_schema: # Avoid infinite recursion
                continue
            resolved_snippet[i] = recursively_resolve_refs(item, full_schema, depth + 1, max_depth)
    return resolved_snippet


def get_schema_snippet(schema: Dict[str, Any], loc: tuple, max_resolve_depth: int = 5) -> Dict[str, Any]:
    """
    Navigates the JSON schema based on the Pydantic error location tuple
    and returns the relevant sub-schema snippet, resolving references recursively.
    """
    current_schema = schema
    original_schema = schema 

    if isinstance(current_schema, dict) and 'properties' in current_schema:
        pass

    for i, part in enumerate(loc):
        resolved_current_schema = current_schema # Keep current_schema if no $ref
        if isinstance(current_schema, dict) and '$ref' in current_schema and isinstance(current_schema['$ref'], str):
             resolved = resolve_ref(original_schema, current_schema['$ref'])
             if 'error' in resolved:
                 return resolved 
             resolved_current_schema = resolved
        
        current_schema = resolved_current_schema # Update current_schema after potential resolution

        # Navigate based on the current part of the location (loc)
        if isinstance(part, str):
            if isinstance(current_schema, dict) and part in current_schema:
                 current_schema = current_schema[part]
            elif isinstance(current_schema, dict) and 'properties' in current_schema and part in current_schema['properties']:
                 current_schema = current_schema['properties'][part]
            else: # Try matching against aliases if 'properties' exists
                found_key = None
                if isinstance(current_schema, dict) and 'properties' in current_schema:
                    expected_alias = part.replace("_", " ").title()
                    for key_in_schema in current_schema['properties']:
                        if key_in_schema == expected_alias:
                            found_key = key_in_schema
                            break
                if found_key:
                    current_schema = current_schema['properties'][found_key]
                else:
                    expected_alias_msg = part.replace("_", " ").title()
                    return {"error": f"Could not find schema property for field '{part}' (tried alias '{expected_alias_msg}') at path {'.'.join(map(str, loc[:i+1]))}. Current schema keys: {list(current_schema.keys()) if isinstance(current_schema, dict) else 'Not a dict'}"}
        
        elif isinstance(part, int):
            if isinstance(current_schema, dict) and 'items' in current_schema:
                current_schema = current_schema['items']
            elif isinstance(current_schema, list): # If schema itself is a list (e.g. for tuple types)
                if part < len(current_schema):
                    current_schema = current_schema[part]
                else:
                    return {"error": f"Index {part} out of bounds for schema list at path {'.'.join(map(str, loc[:i+1]))}"}
            else:
                return {"error": f"Schema is not an array/list type with 'items', cannot navigate by index {part} at path {'.'.join(map(str, loc[:i+1]))}"}
        else:
            return {"error": f"Unexpected part type '{type(part)}' in loc at path {'.'.join(map(str, loc[:i+1]))}"}

    return recursively_resolve_refs(current_schema, original_schema, 0, max_resolve_depth)


# ── Error Formatting for LLM Feedback Agent ───────────────────────────────────
def format_validation_errors_for_agent(errors: List[Dict[str, Any]], schema: Dict[str, Any]) -> str:
    """
    Formats Pydantic validation errors into a string for the feedback agent LLM,
    including relevant schema snippets inline with each error.
    (This function remains as it serves a different purpose - for LLM feedback)
    """
    formatted_parts = []
    total_errors = len(errors)

    formatted_parts.append(f"Pydantic Validation Errors ({total_errors} found):")
    formatted_parts.append("-" * 20)

    for i, error in enumerate(errors):
        loc_tuple = tuple(error.get('loc', ('Unknown Location',))) # Ensure loc is a tuple
        msg = error.get('msg', 'No message')
        error_type = error.get('type', 'unknown')

        formatted_parts.append(f"--- Error {i + 1}/{total_errors} ---")
        formatted_parts.append(f"Path: {'.'.join(map(str, loc_tuple))}")
        formatted_parts.append(f"Message: {msg} (Type: {error_type})")

        schema_snippet = get_schema_snippet(schema, loc_tuple, max_resolve_depth=3) # Use max_resolve_depth 3

        formatted_parts.append("Relevant Schema Snippet for this Error:")
        formatted_parts.append("```json")
        try:
            snippet_json = json.dumps(schema_snippet, indent=2)
            formatted_parts.extend(textwrap.indent(snippet_json, "  ").splitlines())
        except TypeError: # Handle cases where snippet might not be directly serializable (e.g. error dict from get_schema_snippet)
            formatted_parts.append(textwrap.indent(str(schema_snippet), "  "))
        formatted_parts.append("```")

        if i < total_errors - 1:
             formatted_parts.append("-" * 10) 

    formatted_parts.append("-" * 20)
    return "\n".join(formatted_parts)


# ── NEW: Error Formatting for Markdown Book Log ───────────────────────────────
def format_pydantic_errors_for_book(
    pydantic_errors: List[Dict[str, Any]], 

    relevant_schema: Dict[str, Any], 
    component_name: str #
) -> List[Dict[str, Any]]:
    """
    Formats Pydantic validation errors into a list of dictionaries suitable for
    the Markdown book log. Each dictionary contains an ID, message, and schema snippet.
    """
    formatted_errors_for_book = []
    for i, error in enumerate(pydantic_errors):
        loc_tuple = tuple(error.get('loc', ('Unknown Location',))) # Ensure loc is a tuple
        msg = error.get('msg', 'No message')
        error_type = error.get('type', 'N/A')
        
        # Get the schema snippet relevant to the error's location within the passed relevant_schema
        # (which could be a component schema or the full EchoReport schema)
        schema_snippet_dict = get_schema_snippet(relevant_schema, loc_tuple, max_resolve_depth=2) # Keep snippet concise

        full_error_message = f"Path: {component_name}.{'.'.join(map(str, loc_tuple))} - Message: {msg} (Type: {error_type})"
        
        formatted_errors_for_book.append({
            'id': f'V{i+1}', # Validation Error ID
            'message': full_error_message,
            'schema_snippet': schema_snippet_dict 
        })
    return formatted_errors_for_book

