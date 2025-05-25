import re
import logging
from typing import Any, Dict, List, Union, Optional

logger = logging.getLogger(__name__)

def normalize_key(key: str) -> str:
    """
    Normalize a key by:
    - Lowercasing
    - Removing spaces, dashes, and underscores
    """
    return re.sub(r'[\s_\-]', '', key).lower()

def remap_llm_keys(data: Union[Dict, List, Any],
                     current_model_fields: Optional[Dict[str, Any]]
                     ) -> Union[Dict, List, Any]:
    """
    Recursively remap keys in a dict to match model field names, correcting for spaces, underscores, dashes, and case.
    Only remaps keys that are a normalization match to a model field.
    Args:
        data: The LLM output dict, list, or primitive value.
        current_model_fields: The model's __fields__ dict (Dict[str, FieldInfo]) for the current data if it's a dict,
                              or for the items if data is a list of models. None otherwise.
    Returns:
        A new dict, list, or the original primitive with remapped keys where applicable.
    """
    logger.debug(f"remap_llm_keys CALLED. Data type: {type(data)}, Data (truncated): {str(data)[:200]}, Current model fields keys: {list(current_model_fields.keys()) if current_model_fields else 'None'}")

    if isinstance(data, list):
        # If data is a list, current_model_fields should pertain to the schema of the *items* in the list.
        # This means the logic that calls remap_llm_keys for a list value must have already determined
        # the item_schema_fields.
        logger.debug(f"  Data is a list. Remapping each item with fields: {list(current_model_fields.keys()) if current_model_fields else 'None'}")
        return [remap_llm_keys(item, current_model_fields) for item in data]

    if not isinstance(data, dict) or not current_model_fields:
        # Not a dictionary that needs key remapping against model_fields, or no fields provided.
        # Could be a primitive value, or a dict that's not part of a defined Pydantic model structure.
        logger.debug(f"  Data is not a dict OR no current_model_fields. Returning data as is. Data type: {type(data)}")
        return data

    # Build normalization map for the current dictionary level
    norm_map = {normalize_key(field_name): field_name for field_name in current_model_fields.keys()}
    logger.debug(f"  Normalized map for current dict level: {norm_map}")

    remapped_dict = {}
    for llm_key, llm_value in data.items():
        norm_llm_key = normalize_key(llm_key)
        
        # Determine the target model field name
        model_field_name = norm_map.get(norm_llm_key, llm_key) # Default to original llm_key if no normalized match
        
        if model_field_name != llm_key:
            logger.debug(f"    Key mapped: '{llm_key}' (norm: '{norm_llm_key}') -> '{model_field_name}'")
        else:
            logger.debug(f"    Key processing: '{llm_key}' (norm: '{norm_llm_key}') -> (no change, or no match in norm_map: '{model_field_name}')")

        # Determine model_fields for the next recursion level (for llm_value)
        subfields_for_next_recursion = None
        field_info = current_model_fields.get(model_field_name) # Get FieldInfo for the target model field

        if field_info:
            field_annotation = getattr(field_info, 'annotation', None)
            if field_annotation:
                if hasattr(field_annotation, '__fields__'): 
                    subfields_for_next_recursion = field_annotation.__fields__
                    logger.debug(f"      Subfields for '{model_field_name}' (type: Pydantic Model {field_annotation.__name__}): {list(subfields_for_next_recursion.keys())}")
                else: # Check if annotation is List[PydanticModel] or similar
                    origin = getattr(field_annotation, '__origin__', None)
                    args = getattr(field_annotation, '__args__', [])
                    if (origin is list or origin is List) and args and hasattr(args[0], '__fields__'):
                        # This is for items if llm_value is a list
                        subfields_for_next_recursion = args[0].__fields__
                        logger.debug(f"      Subfields for items in '{model_field_name}' (type: List[{args[0].__name__}]): {list(subfields_for_next_recursion.keys())}")
                    elif isinstance(llm_value, dict) or isinstance(llm_value, list):
                         logger.debug(f"      Value for '{model_field_name}' is dict/list, but its annotation '{field_annotation}' is not a recognized Pydantic model or List[PydanticModel]. No subfields for recursion.")
            elif isinstance(llm_value, dict) or isinstance(llm_value, list):
                 logger.debug(f"      Value for '{model_field_name}' is dict/list, but no annotation found on FieldInfo. No subfields for recursion.")
        elif (isinstance(llm_value, dict) or isinstance(llm_value, list)):
            logger.debug(f"    Field '{model_field_name}' (from llm_key '{llm_key}') not found in current_model_fields. Cannot determine subfields for recursion if value is dict/list.")

        remapped_dict[model_field_name] = remap_llm_keys(llm_value, subfields_for_next_recursion)
    
    logger.debug(f"  Remapped dictionary for current level: {remapped_dict}")
    return remapped_dict

