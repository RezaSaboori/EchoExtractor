import os
import json
import time
from typing import Dict, Any, Type, List
import logging
import textwrap
from dotenv import load_dotenv

from echo_extraction import abbreviation_processor
from echo_extraction.extraction_logic import extract_component_data
from echo_extraction.utils import setup_logging, set_log_file
from echo_extraction.models import (
    EchoReport, CardiacChambers, ValvularApparatus,
    GreatVesselsAndVenousReturn, CongenitalAndStructuralDefects,
    MitralValve, AorticValve, PulmonaryValve, TricuspidValve,
    Pericardium, LeftVentricle, RightVentricle, LeftAtrium, RightAtrium,
    VSD, ASD, PFO,
    Aorta, PulmonicVein, IVC,
    LVAssessment, LVMeasurements,
    RVAssessment, RVMeasurements,
    LAAssessment, LAMeasurements,
    RAAssessment, RAMeasurements,
    MitralValveAssessment, MitralValveMeasurements,
    AorticValveAssessment, AorticValveMeasurements,
    PulmonaryValveAssessment, PulmonaryValveMeasurements,
    TricuspidValveAssessment, TricuspidValveMeasurements,
    AortaAssessment, AortaMeasurements,
    PulmonicVeinAssessment, PulmonicVeinMeasurements,
    IVCAssessment, IVCMeasurements,
    VSDAssessment, VSDMeasurements,
    ASDAssessment, ASDMeasurements,
    PFOAssessment, PFOMeasurements,
    PericardiumAssessment, PericardiumMeasurements
)

# Load environment variables
load_dotenv()

# Define directories and paths
LOG_FILE_DIR = os.getenv("LOG_FILE_DIR", "/storage03/Saboori/Echo/Extractor/main_app/logs")
FINAL_REPORTS_DIR = os.getenv("FINAL_REPORTS_DIR", "/storage03/Saboori/Echo/Extractor/main_app/final_reports")
ABBREVIATION_CSV_PATH = os.getenv("ABBREVIATION_CSV_PATH", "/storage03/Saboori/Echo/Extractor/main_app/echo_extraction/echo_abb_merged_csv.csv")
REPORTS_JSON_PATH = os.getenv("REPORTS_JSON_PATH", "/storage03/Saboori/Echo/Extractor/main_app/CTICI_NCIBB_Echo_Sample.json")

logger = logging.getLogger(__name__)

def process_report(report_text: str, abbrev_dict: Dict[str, str]) -> EchoReport:
    """Process a single echo report and return the final structured report."""
    start_time = time.perf_counter()

    # Process abbreviations
    if abbrev_dict:
        processed_report = abbreviation_processor.process_abbreviations(report_text, abbrev_dict)
        logger.debug(f"Processed Report:\n{textwrap.indent(processed_report, '    ')}")
    else:
        processed_report = report_text
        logger.warning("Skipping abbreviation processing.")

    # Log the input section
    logger.info("Input Section", extra={
        'log_type': 'INPUT_SECTION',
        'raw_input': report_text,
        'processed_input': processed_report
    })

    component_models_to_extract: List[Type[BaseModel]] = [
        MitralValve, AorticValve, PulmonaryValve, TricuspidValve,
        Pericardium,
        LeftVentricle, RightVentricle, LeftAtrium, RightAtrium,
        VSD, ASD, PFO,
        Aorta, PulmonicVein, IVC
    ]

    extracted_components: Dict[str, BaseModel] = {}
    extraction_errors: Dict[str, str] = {}

    logger.info("Starting modular extraction process...")

    for component_model in component_models_to_extract:
        component_name = component_model.__name__
        logger.info(f"\n--- Extracting data for {component_name} ---")
        try:
            validated_data = extract_component_data(processed_report, component_model, max_attempts=5)
            extracted_components[component_name] = validated_data
            logger.info(f"Successfully extracted data for {component_name}")
        except RuntimeError as e:
            logger.error(f"Failed to extract data for {component_name}: {e}")
            extraction_errors[component_name] = str(e)
        except Exception as e:
            logger.error(f"An unexpected error occurred during extraction for {component_name}: {e}")
            extraction_errors[component_name] = str(e)

    logger.info("\n--- Modular extraction complete ---")

    try:
        cardiac_chambers_data = CardiacChambers(
            Left_Ventricle=extracted_components.get(LeftVentricle.__name__, LeftVentricle(assessment=LVAssessment(), measurements=LVMeasurements())),
            Right_Ventricle=extracted_components.get(RightVentricle.__name__, RightVentricle(assessment=RVAssessment(), measurements=RVMeasurements())),
            Left_Atrium=extracted_components.get(LeftAtrium.__name__, LeftAtrium(assessment=LAAssessment(), measurements=LAMeasurements())),
            Right_Atrium=extracted_components.get(RightAtrium.__name__, RightAtrium(assessment=RAAssessment(), measurements=RAMeasurements()))
        )

        valvular_apparatus_data = ValvularApparatus(
            Mitral_Valve=extracted_components.get(MitralValve.__name__, MitralValve(assessment=MitralValveAssessment(), measurements=MitralValveMeasurements())),
            Aortic_Valve=extracted_components.get(AorticValve.__name__, AorticValve(assessment=AorticValveAssessment(), measurements=AorticValveMeasurements())),
            Pulmonary_Valve=extracted_components.get(PulmonaryValve.__name__, PulmonaryValve(assessment=PulmonaryValveAssessment(), measurements=PulmonaryValveMeasurements())),
            Tricuspid_Valve=extracted_components.get(TricuspidValve.__name__, TricuspidValve(assessment=TricuspidValveAssessment(), measurements=TricuspidValveMeasurements()))
        )

        great_vessels_data = GreatVesselsAndVenousReturn(
            aorta=extracted_components.get(Aorta.__name__, Aorta(assessment=AortaAssessment(), measurements=AortaMeasurements())),
            pulmonic_vein=extracted_components.get(PulmonicVein.__name__, PulmonicVein(assessment=PulmonicVeinAssessment(), measurements=PulmonicVeinMeasurements())),
            ivc=extracted_components.get(IVC.__name__, IVC(assessment=IVCAssessment(), measurements=IVCMeasurements()))
        )

        congenital_defects_data = CongenitalAndStructuralDefects(
            vsd=extracted_components.get(VSD.__name__, VSD(assessment=VSDAssessment(), measurements=VSDMeasurements())),
            asd=extracted_components.get(ASD.__name__, ASD(assessment=ASDAssessment(), measurements=ASDMeasurements())),
            pfo=extracted_components.get(PFO.__name__, PFO(assessment=PFOAssessment(), measurements=PFOMeasurements()))
        )

        pericardium_data = extracted_components.get(Pericardium.__name__, Pericardium(assessment=PericardiumAssessment(), measurements=PericardiumMeasurements()))

        final_echo_report = EchoReport(
            Cardiac_Chambers=cardiac_chambers_data,
            Valvular_Apparatus=valvular_apparatus_data,
            GreatVessels_and_VenousReturn=great_vessels_data,
            Congenital_and_Structural_Defects=congenital_defects_data,
            pericardium=pericardium_data
        )

        logger.info("\n--- Final EchoReport object created successfully ---")
        final_report_json_string = final_echo_report.model_dump_json(indent=2)

        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info("Final Report Section", extra={
            'log_type': 'FINAL_REPORT_SECTION',
            'successful_extractions': len(extracted_components),
            'total_components': len(component_models_to_extract),
            'total_time': total_time,
            'final_report_json': final_report_json_string
        })

        return final_echo_report

    except Exception as e:
        logger.error(f"\n--- Failed to create final EchoReport object ---")
        logger.error(f"Error: {e}")
        logger.error("Extracted components available:")
        for name, data in extracted_components.items():
            try:
                logger.error(f"    {name}: {data.model_dump_json(indent=2)}")
            except AttributeError:
                logger.error(f"    {name}: {data}")
        if extraction_errors:
            logger.error("Errors encountered during component extraction:")
            for name, error in extraction_errors.items():
                logger.error(f"    {name}: {error}")
        return None

if __name__ == "__main__":
    from echo_extraction.llm_setup import is_langchain_available
    if not is_langchain_available():
        print("\nLangchain components not available. Please install langchain-community and langchain-core (`pip install langchain-community langchain-core`) and ensure Ollama is running with the 'cogito:70b' model.")
    else:
        # Load abbreviation dictionary once
        abbrev_dict = abbreviation_processor.get_abbreviation_dictionary(ABBREVIATION_CSV_PATH)

        # Load reports from JSON
        try:
            with open(REPORTS_JSON_PATH, 'r') as f:
                reports = json.load(f)
        except Exception as e:
            print(f"Failed to load reports from {REPORTS_JSON_PATH}: {e}")
            exit(1)

        # Ensure output directories exist
        os.makedirs(LOG_FILE_DIR, exist_ok=True)
        os.makedirs(FINAL_REPORTS_DIR, exist_ok=True)

        # Set up initial logging (console only)
        setup_logging()

        # Process each report
        for i, report in enumerate(reports, start=1):
            try:
                _id = report['_id']
                report_text = report['data']
                log_file_path = os.path.join(LOG_FILE_DIR, f"{_id}.md")
                final_report_path = os.path.join(FINAL_REPORTS_DIR, f"{_id}.json")
                
                print(f"Processing report {i}/{len(reports)}: {_id}")

                # Set log file for this report
                set_log_file(log_file_path)

                # Process the report
                final_echo_report = process_report(report_text, abbrev_dict)

                if final_echo_report:
                    with open(final_report_path, 'w') as f:
                        f.write(final_echo_report.model_dump_json(indent=2))
                    print(f"Successfully processed report {_id}")
                else:
                    print(f"Failed to process report {_id}")
            except Exception as e:
                print(f"Error processing report {_id}: {e}")