import re
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get file paths from environment variables with defaults
input_json_path = os.getenv("REPORTS_JSON_PATH", "/storage03/Saboori/Echo/Extractor/CTICI_NCIBB_Echo_Sample.json")
output_json_path = os.getenv("ABBREVIATIONS_OUTPUT_JSON_PATH", "/storage03/Saboori/Echo/Extractor/abbreviations.json")

# Load the data from input JSON file
with open(input_json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Regex pattern: at least two consecutive uppercase letters, optionally with dash
abbreviation_pattern = re.compile(r'\b[A-Z]{2,}(?:-[A-Z]+)?\b')

# Set to store unique abbreviations
abbreviations = set()

# Extract abbreviations from each report
for entry in data:
    text = entry.get("data", "")
    matches = abbreviation_pattern.findall(text)
    abbreviations.update(matches)

# Sort and prepare for export
sorted_abbreviations = sorted(abbreviations)

# Save to abbreviations.json
with open(output_json_path, "w", encoding="utf-8") as outfile:
    json.dump(sorted_abbreviations, outfile, indent=2)

print(f"Extracted {len(sorted_abbreviations)} unique abbreviations and saved to {output_json_path}.")
