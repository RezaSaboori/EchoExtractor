import re
import argparse

def clean_markdown_file(filepath):
    """
    Reads a markdown file, corrects problematic consecutive backtick sequences,
    and overwrites the file with the cleaned content.

    Specifically, it addresses:
    1. Sequences of 4 or more backticks (e.g., ````, `````) are replaced with ```.
    2. Redundant ``` blocks, such as:
       ```
       ```json
       { ... }
       ```
       which becomes:
       ```json
       { ... }
       ```
    3. Or:
       ```json
       ```
       { ... }
       ```
       which also becomes:
       ```json
       { ... }
       ```
    4. Consecutive lines each containing only ```:
       ```
       ```
       which becomes:
       ```
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        original_content = content

        # Step 1: Normalize overly long backtick sequences to ```
        # e.g., ```` -> ```,  ````` -> ```
        content = re.sub(r'`{4,}', '```', content)

        # Step 2: Handle redundant ``` lines around a language-specified block
        # Case A: A line with only ``` followed by a line starting with ```lang
        content = re.sub(r'(^[ \t]*```[ \t]*\n)([ \t]*```[a-zA-Z0-9]+.*\n)', r'\2', content, flags=re.MULTILINE)

        # Case B: A line with ```lang followed by a line with only ```
        content = re.sub(r'(^[ \t]*```[a-zA-Z0-9]+.*\n)([ \t]*```[ \t]*\n)', r'\1', content, flags=re.MULTILINE)

        # Step 3: Handle consecutive lines of triple backticks
        # e.g., ```\n``` -> ```
        # This regex looks for a line that IS "```" (with optional surrounding whitespace)
        # followed by another line that IS "```" (with optional surrounding whitespace)
        # and replaces it with a single "```" line.
        # We loop this replacement because ```\n```\n``` would become ```\n``` in one pass, requiring another pass.
        new_content = content
        while True:
            # Replace two consecutive standalone ``` lines with one
            # Handles ```\n``` and keeps the first one. Also handles if the second ``` is at the EOF.
            # The (?=\n|\Z) is a positive lookahead asserting that the second ``` is followed by a newline or end of string,
            # without consuming it, which helps in cases of more than two ``` lines.
            processed_content = re.sub(r'(^[ \t]*```[ \t]*\n)[ \t]*```[ \t]*(?=\n|\Z)', r'\1', new_content, flags=re.MULTILINE)
            if processed_content == new_content:
                break
            new_content = processed_content
        content = new_content

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Cleaned file: {filepath}")
        else:
            print(f"No changes needed for file: {filepath}")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred while processing {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Clean markdown files by correcting problematic backtick sequences.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("filepath", help="Path to the markdown file to clean.")
    args = parser.parse_args()
    clean_markdown_file(args.filepath)

if __name__ == "__main__":
    main()