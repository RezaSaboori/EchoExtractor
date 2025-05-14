import logging
import json
import textwrap
import os

LOG_FILE_DIR = "/storage03/Saboori/Echo/Extractor/main_app/logs"

logger = logging.getLogger(__name__)

class BookLogFilter(logging.Filter):
    """Filter log records intended for the Markdown book format."""
    def filter(self, record):
        return hasattr(record, 'log_type')

class MarkdownBookFormatter(logging.Formatter):
    """Format log records into a structured Markdown document."""
    def format(self, record):
        log_type = getattr(record, 'log_type', None)
        if not log_type:
            return ""

        parts = []

        if log_type == 'INPUT_SECTION':
            raw_input = getattr(record, 'raw_input', 'No raw input provided.')
            processed_input = getattr(record, 'processed_input', 'No processed input provided.')
            parts.append("# 📥 Input\n")
            parts.append("## 🧾 Raw Input\n")
            parts.append("```\n")
            parts.append(raw_input + "\n")
            parts.append("```\n")
            parts.append("## 🛠️ Processed Input\n")
            parts.append("```\n")
            parts.append(processed_input + "\n")
            parts.append("```\n")
        elif log_type == 'COMPONENT_START':
            component_name = getattr(record, 'component_name', 'Unknown Component')
            parts.append(f"\n\n# 📖 {component_name}\n")
        elif log_type == 'ATTEMPT_PROCESSED':
            component_name = getattr(record, 'component_name', 'Unknown Component')
            attempt_num = getattr(record, 'attempt_num', 'N/A')
            max_attempts = getattr(record, 'max_attempts', 'N/A')
            status = getattr(record, 'status', 'Unknown')

            status_emoji = "✅" if status == "Successful" else "❌"
            parts.append(f"\n## 🔄 Attempt {attempt_num}/{max_attempts} ({status_emoji} {status})\n")

            extractor_input = getattr(record, 'extractor_input', {})
            extractor_raw_output = getattr(record, 'extractor_raw_output', 'No raw output logged.')

            parts.append("\n### 🔍 Extractor\n")
            parts.append("\n#### 📥 Input\n")
            parts.append("```json\n")
            try:
                input_json_str = json.dumps(extractor_input, indent=2, ensure_ascii=False)
                parts.append(input_json_str + "\n")
            except Exception as e:
                logger.error(f"Error formatting Input JSON for log: {e}")
                parts.append("Error formatting Input JSON.\n")
            parts.append("```\n")

            parts.append("\n#### 📤 Raw Output\n")
            parts.append("```text\n")
            try:
                if extractor_raw_output:
                    parts.append(str(extractor_raw_output) + "\n")
                else:
                    parts.append("No raw output.\n")
            except Exception as e:
                logger.error(f"Error formatting Raw Output for log: {e}")
                parts.append("Error formatting Raw Output.\n")
            parts.append("```\n")

            errors = getattr(record, 'errors', [])
            if errors:
                parts.append("\n### 🚨 Errors\n")
                for i, err_detail in enumerate(errors):
                    error_id_display = f"Error {i+1}"
                    error_message = err_detail.get('message', 'No message provided.')
                    schema_snippet = err_detail.get('schema_snippet', {})

                    parts.append(f"\n#### {error_id_display}\n")
                    clean_error_message = str(error_message).strip().replace('`', "'")
                    parts.append("**Details:** `" + clean_error_message + "`\n")

                    if schema_snippet:
                        parts.append("\n**Related Schema:**\n")
                        parts.append("```json\n")
                        try:
                            schema_json_str = json.dumps(schema_snippet, indent=2, ensure_ascii=False)
                            parts.append(schema_json_str + "\n")
                        except Exception as e:
                            logger.error(f"Error formatting Schema JSON for log: {e}")
                            parts.append("Error formatting Schema JSON.\n")
                        parts.append("```\n")

            feedback_output = getattr(record, 'feedback_output', None)
            clean_feedback = str(feedback_output).strip() if feedback_output is not None else ""
            is_default_feedback = (clean_feedback == "No feedback provided (first attempt or previous success).")

            if clean_feedback and not is_default_feedback:
                parts.append("\n### 💡 Feedback Generator\n")
                parts.append("```text\n")
                parts.append(clean_feedback + "\n")
                parts.append("```\n")
        elif log_type == 'FINAL_REPORT_SECTION':
            successful_extractions = getattr(record, 'successful_extractions', 0)
            total_components = getattr(record, 'total_components', 0)
            total_time = getattr(record, 'total_time', 0.0)
            final_report_json = getattr(record, 'final_report_json', 'No final report generated.')
            ratio = successful_extractions / total_components if total_components > 0 else 0
            parts.append("# Final Report\n")
            parts.append("## 📊 Performance Summary\n")
            parts.append(f"🎯 Successful Extractions: {successful_extractions}/{total_components} ({ratio:.2%})\n")
            parts.append(f"⏱️ Total Time: {total_time:.2f} seconds\n")
            parts.append("## 📝 Final Echo Report\n")
            parts.append("```json\n")
            parts.append(final_report_json + "\n")
            parts.append("```\n")

        return "".join(parts)

def setup_logging():
    """Set up logging with console output only."""
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    logger.info("Console logging setup (INFO+).")

def set_log_file(log_file_path: str):
    """Dynamically set the file handler for logging to a specific Markdown file."""
    root_logger = logging.getLogger()
    # Remove existing file handlers
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            root_logger.removeHandler(handler)
            handler.close()
    
    # Add new file handler
    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    book_formatter = MarkdownBookFormatter()
    file_handler.setFormatter(book_formatter)
    file_handler.addFilter(BookLogFilter())
    root_logger.addHandler(file_handler)
    logger.info(f"Set log file to '{log_file_path}'")