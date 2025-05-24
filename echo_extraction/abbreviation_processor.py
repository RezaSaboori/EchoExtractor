import pandas as pd
import re
import logging
from typing import Dict, Union # Import Union here

logger = logging.getLogger(__name__)

# --- Abbreviation Replacement Logic ---

# Load the abbreviation dictionary safely
def load_abbreviation_dictionary(csv_path: str) -> Dict[str, str]:
    """
    Loads the abbreviation dictionary from a CSV file.

    Args:
        csv_path: The path to the CSV file containing abbreviations and full forms.

    Returns:
        A dictionary mapping lowercase abbreviations to their full forms,
        or an empty dictionary if loading fails.
    """
    abbrev_dict: Dict[str, str] = {}
    try:
        df = pd.read_csv(csv_path, encoding="ISO-8859-1")
        abbrev_dict = {
            str(row['Abbreviation']).strip().lower(): str(row['FullForm']).strip()
            for _, row in df.iterrows()
        }
        logger.info(f"Abbreviation dictionary loaded successfully from {csv_path}.")
    except FileNotFoundError:
        logger.error(f"Abbreviation CSV file not found at {csv_path}. Abbreviation replacement will be skipped.")
    except Exception as e:
        logger.error(f"Error loading abbreviation dictionary from {csv_path}: {e}. Abbreviation replacement may be incomplete.")
    return abbrev_dict

# Step 1: Replace dash-connected abbreviations BEFORE punctuation spacing
def replace_dashed_abbreviations(text: str, abbrev_map: dict) -> str:
    """Replaces dash-connected abbreviations in text while preserving line breaks."""
    dashed_abbrevs = {k: v for k, v in abbrev_map.items() if '-' in k}
    
    
    # Split by newlines to preserve them
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Sort by length descending to handle longer abbreviations first
        for abbr in sorted(dashed_abbrevs.keys(), key=lambda x: -len(x)):
            # Use word boundaries to ensure whole word match
            pattern = re.compile(rf'\b{re.escape(abbr)}\b', re.IGNORECASE)
            line = pattern.sub(dashed_abbrevs[abbr], line)
        processed_lines.append(line)
    
    # Join the lines back with newlines
    return '\n'.join(processed_lines)

# Step 2: Normalize punctuation spacing (but keep internal dashes)
def normalize_text_spacing(text: str) -> str:
    """Adds spaces around punctuation and normalizes whitespace while preserving line breaks."""
    # Split the text by newlines to preserve them
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Add space before and after common punctuation marks, INCLUDING dots initially
        line = re.sub(r'([.,!?;:()=+&{}\[\]])', r' \1 ', line)
        # Add space around dashes that are not part of a word (e.g., "word - word")
        line = re.sub(r'(?<!\w)-(?!\w)', ' - ', line)
        # Replace multiple spaces with a single space and strip leading/trailing whitespace
        line = re.sub(r' +', ' ', line).strip()
        processed_lines.append(line)
    
    # Join the lines back with newlines
    return '\n'.join(processed_lines)

# Step 3: Remove space around dots that are between numbers (e.g., "2 . 5" -> "2.5")
def remove_space_around_numeric_dots(text: str) -> str:
    """Removes space around dots that appear between two digits while preserving line breaks."""
    # Split by newlines to preserve them
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Find patterns like "digit space dot space digit" and replace with "digit dot digit"
        # Use \s* to account for potential multiple spaces added in the previous step
        line = re.sub(r'(\d)\s*\.\s*(\d)', r'\1.\2', line)
        processed_lines.append(line)
    
    # Join the lines back with newlines
    return '\n'.join(processed_lines)

# Step 4: Add space between numbers and words that are immediately adjacent
def add_space_between_number_and_word(text: str) -> str:
    """Adds a space between a number and an adjacent word while preserving line breaks."""
    # Split by newlines to preserve them
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Add space between a number (possibly with a decimal) and a following letter
        line = re.sub(r'(\d+(\.\d+)?)([A-Za-z])', r'\1 \3', line)
        # Add space between a letter and a following number (possibly with a decimal)
        line = re.sub(r'([A-Za-z])(\d+(\.\d+)?)', r'\1 \2', line)
        processed_lines.append(line)
    
    # Join the lines back with newlines
    return '\n'.join(processed_lines)

# Step 5: Replace regular abbreviations after spacing
def replace_standard_abbreviations(text: str, abbrev_map: dict) -> str:
    """Replaces standard abbreviations in text while preserving line breaks."""
    regular_abbrevs = {k: v for k, v in abbrev_map.items() if '-' not in k}
    
    # Split by newlines to preserve them
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Sort by length descending to handle longer abbreviations first
        for abbr in sorted(regular_abbrevs.keys(), key=lambda x: -len(x)):
            # Use word boundaries to ensure whole word match
            pattern = re.compile(rf'\b{re.escape(abbr)}\b', re.IGNORECASE)
            line = pattern.sub(regular_abbrevs[abbr], line)
        processed_lines.append(line)
    
    # Join the lines back with newlines
    return '\n'.join(processed_lines)

def process_abbreviations(text: str, abbrev_map: Dict[str, str]) -> str:
    """
    Applies the full abbreviation replacement pipeline to the input text.

    Args:
        text: The input text with potential abbreviations.
        abbrev_map: The dictionary mapping abbreviations to full forms.

    Returns:
        The text with abbreviations replaced.
    """
    if not abbrev_map:
        logger.warning("Abbreviation map is empty. Skipping abbreviation processing.")
        return text # Return original text if map is empty

    # Convert literal '\n' to actual newlines if they exist in the text
    text = text.replace('\\n', '\n')

    logger.info("Applying abbreviation replacement pipeline...")
    
    # Process each line separately to preserve newlines
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            # Apply the pipeline to each line individually
            step1_processed = replace_dashed_abbreviations(line, abbrev_map)
            step2_processed = normalize_text_spacing(step1_processed)
            step3_processed = remove_space_around_numeric_dots(step2_processed)
            step4_processed = add_space_between_number_and_word(step3_processed)
            line_output = replace_standard_abbreviations(step4_processed, abbrev_map)
            
            # Normalize whitespace for this line
            processed_lines.append(re.sub(r' +', ' ', line_output).strip())
        else:
            processed_lines.append('')  # Keep empty lines
    
    # Join the processed lines with newlines
    final_output = '\n'.join(processed_lines)

    logger.info("Abbreviation replacement complete.")
    return final_output

# Global variable to store the loaded dictionary
_abbrev_dictionary: Union[Dict[str, str], None] = None

def get_abbreviation_dictionary(csv_path: str) -> Dict[str, str]:
    """
    Gets the loaded abbreviation dictionary, loading it if necessary.
    Uses a global variable to avoid reloading the CSV multiple times.
    """
    global _abbrev_dictionary
    if _abbrev_dictionary is None:
        _abbrev_dictionary = load_abbreviation_dictionary(csv_path)
    return _abbrev_dictionary