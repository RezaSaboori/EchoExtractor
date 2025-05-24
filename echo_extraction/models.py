from enum import Enum
from typing import List, Union, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict


# ── Shared Models ────────────────────────────────────────────────────────────
MeasurementValue = Union[float, int, Literal["Not Measured"]]

common_model_config = ConfigDict(
    populate_by_name=True,
    use_enum_values=True,
    alias_generator=lambda s: s.replace("_", " ").title()
)






# ── Left Ventricle ────────────────────────────────────────────────────────────
# ── Left Ventricle Enums ──────────────────────────────────────────────────────
class LVSizeEnum(str, Enum):
    """Enumeration for Left Ventricular size assessment."""
    NORMAL = "Normal"
    SMALL = "Small"
    ENLARGED = "Enlarged"
    MILD_ENLARGED = "Mild Enlarged"
    MILD_TO_MODERATE_ENLARGED = "Mild to Moderate Enlarged"
    MODERATE_ENLARGED = "Moderate Enlarged"
    MODERATE_TO_SEVERE_ENLARGED = "Moderate to Severe Enlarged"
    SEVERELY_ENLARGED = "Severe Enlarged"
    NOT_ASSESSED = "Not Assessed"

class LVSystolicFunctionEnum(str, Enum):
    """Enumeration for Left Ventricular systolic function assessment."""
    NORMAL = "Normal"
    REDUCED = "Reduced"
    MILDLY_REDUCED = "Mildly Reduced"
    MILD_TO_MODERATELY_REDUCED = "Mild to Moderately Reduced"
    MODERATELY_REDUCED = "Moderately Reduced"
    MODERATE_TO_SEVERELY_REDUCED = "Moderate to Severely Reduced"
    SEVERELY_REDUCED = "Severely Reduced"
    NOT_ASSESSED = "Not Assessed"

class LVDiastolicFunctionEnum(str, Enum):
    """Enumeration for Left Ventricular diastolic function grade."""
    NORMAL = "Normal"
    GRADE_I = "Grade I" # Impaired Relaxation
    GRADE_II = "Grade II" # Pseudonormal
    GRADE_III = "Grade III" # Restrictive - Reversible
    GRADE_IV = "Grade IV" # Restrictive - Irreversible
    NOT_ASSESSED = "Not Assessed"

class LVHypertrophyTypeEnum(str, Enum):
    """Enumeration for Left Ventricular hypertrophy type."""
    NO = "No"
    CONCENTRIC_REMODELING = "Concentric Remodeling"
    CONCENTRIC = "Concentric"
    ECCENTRIC = "Eccentric"
    NOT_ASSESSED = "Not Assessed"

class LVHypertrophySeverityEnum(str, Enum):
    """Enumeration for Left Ventricular hypertrophy severity."""
    MILD = "Mild"
    MILD_TO_MODERATE = "Mild to Moderate"
    MODERATE = "Moderate"
    MODERATE_TO_SEVERE = "Moderate to Severe"
    SEVERE = "Severe"
    NOT_ASSESSED = "Not Assessed"

class LVWallMotionAbnormalityTypeEnum(str, Enum):
    """Enumeration for Left Ventricular wall motion abnormality type."""
    NO = "No"
    GLOBAL_HYPOKINESIA = "Global Hypokinesia"
    RWMA = "RWMA" # Regional Wall Motion Abnormality
    NOT_ASSESSED = "Not Assessed"

class LVWallMotionAbnormalityRegionEnum(str, Enum):
    """Enumeration for Left Ventricular wall motion abnormality regions (AHA 17-segment model)."""
    INFEROSEPTUM_BASE = "Inferoseptum_Base"
    INFEROSEPTUM_MID = "Inferoseptum_Mid"
    INFEROSEPTUM_APEX = "Inferoseptum_Apex"
    ANTEROLATERAL_BASE = "Anterolateral_Base"
    ANTEROLATERAL_MID = "Anterolateral_Mid"
    ANTEROLATERAL_APEX = "Anterolateral_Apex"
    INFERIOR_BASE = "Inferior_Base"
    INFERIOR_MID = "Inferior_Mid"
    INFERIOR_APEX = "Inferior_Apex"
    ANTERIOR_BASE = "Anterior_Base"
    ANTERIOR_MID = "Anterior_Mid"
    ANTERIOR_APEX = "Anterior_Apex"
    ANTEROSEPTUM_BASE = "Anteroseptum_Base"
    ANTEROSEPTUM_MID = "Anteroseptum_Mid"
    INFEROLATERAL_BASE = "Inferolateral_Base"
    INFEROLATERAL_MID = "Inferolateral_Mid"
    POSTERIOR_CIRCULATION = "Posterior Circulation"
    INFERIOR_CIRCULATION = "Inferior Circulation" 
    NOT_ASSESSED = "Not Assessed" 

class LVClotPresenceEnum(str, Enum):
    """Enumeration for presence of thrombus in Left Ventricle."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class LVASHPresenceEnum(str, Enum):
    """Enumeration for presence of Asymmetric septal hypertrophy in Left Ventricle."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class LVEFMethodEnum(str, Enum):
    """Enumeration for method of EF measurement."""
    EYE_BALL = "Eye ball"
    SIMPSON = "Simpson"


# ── Left Ventricle Assessment Models ────────────────────────────────────────────
class LVHypertrophy(BaseModel):
    """Model for Left Ventricular hypertrophy assessment."""
    model_config = common_model_config

    type: LVHypertrophyTypeEnum = Field(
        default=LVHypertrophyTypeEnum.NOT_ASSESSED,
        description="Hypertrophy type assessment"
    )
    severity: LVHypertrophySeverityEnum = Field(
        default=LVHypertrophySeverityEnum.NOT_ASSESSED,
        description="Hypertrophy severity assessment"
    )

class LVWallMotionAbnormality(BaseModel):
    """Model for Left Ventricular wall motion abnormality assessment."""
    model_config = common_model_config

    type: LVWallMotionAbnormalityTypeEnum = Field(
        default=LVWallMotionAbnormalityTypeEnum.NOT_ASSESSED,
        description="Wall motion abnormality type"
    )
    regions: List[LVWallMotionAbnormalityRegionEnum] = Field(
        default_factory=lambda: [LVWallMotionAbnormalityRegionEnum.NOT_ASSESSED],
        description="Wall motion abnormality regions"
    )


class LVAssessment(BaseModel):
    """Overall assessment of the Left Ventricle."""
    model_config = common_model_config

    size: LVSizeEnum = Field(
        default=LVSizeEnum.NOT_ASSESSED,
        description="Left Ventricular size assessment"
    )
    systolic_function: LVSystolicFunctionEnum = Field(
        default=LVSystolicFunctionEnum.NOT_ASSESSED,
        description="Systolic function assessment"
    )
    diastolic_function: LVDiastolicFunctionEnum = Field(
        default=LVDiastolicFunctionEnum.NOT_ASSESSED,
        description="Diastolic function grade"
    )
    hypertrophy: LVHypertrophy = Field(
        default_factory=LVHypertrophy,
        description="Hypertrophy type and severity assessment"
    )
    wall_motion_abnormality: LVWallMotionAbnormality = Field(
        default_factory=LVWallMotionAbnormality,
        description="Wall motion abnormality assessment"
    )
    clot: LVClotPresenceEnum = Field(
        default=LVClotPresenceEnum.NOT_ASSESSED,
        description="Presence of thrombus in Left Ventricle"
    )
    ash: LVASHPresenceEnum = Field(
        default=LVASHPresenceEnum.NOT_ASSESSED,
        description="Presence of Asymmetric septal hypertrophy in Left Ventricle"
    )


# ── Left Ventricle Measurement Models ────────────────────────────────────────────

class LVEjectionFraction(BaseModel):
    """Quantitative measurements of Ejection Fraction."""
    model_config = common_model_config

    value: MeasurementValue = Field(
        default="Not Measured",
        description="Ejection Fraction (%)",
        unit="%"
    )
    method: LVEFMethodEnum = Field(
        default=LVEFMethodEnum.SIMPSON,
        description="Method of EF measurement"
    )

    # Field-level validator: If value is invalid, only default value, not the whole model
    @field_validator("value", mode="before")
    @classmethod
    def validate_ef_value(cls, v, info):
        """If EF value is invalid, return 'Not Measured' but keep other fields."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (5 <= val <= 90):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"

    # Field-level validator: If method is invalid, only default method
    @field_validator("method", mode="before")
    @classmethod
    def validate_ef_method(cls, v, info):
        """If method is invalid, return default method only for this field."""
        valid_methods = [e.value for e in LVEFMethodEnum]
        if v in valid_methods:
            return v
        return LVEFMethodEnum.SIMPSON

class LVDiameters(BaseModel):
    """Quantitative measurements of Left Ventricular diameters."""
    model_config = common_model_config

    lvedd: MeasurementValue = Field(
        default="Not Measured",
        description="LV End-Diastolic Diameter",
        unit="cm"
    )
    lvesd: MeasurementValue = Field(
        default="Not Measured",
        description="LV End-Systolic Diameter",
        unit="cm"
    )
    ivsd: MeasurementValue = Field(
        default="Not Measured",
        description="Interventricular Septum Diameter",
        unit="cm"
    )
    pwd: MeasurementValue = Field(
        default="Not Measured",
        description="Posterior Wall Diameter",
        unit="cm"
    )

    @field_validator("lvedd", "lvesd", "ivsd", "pwd", mode="before")
    @classmethod
    def validate_diameter_value(cls, v, info):
        """If LV diameter value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            # Specific range checks based on the JSON schema
            if info.field_name == 'lvedd' and not (2 <= val <= 9):
                return "Not Measured"
            if info.field_name == 'lvesd' and not (1 <= val <= 8):
                return "Not Measured"
            if info.field_name == 'ivsd' and not (0.5 <= val <= 3):
                return "Not Measured"
            if info.field_name == 'pwd' and not (0.5 <= val <= 3):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LVVolumes(BaseModel):
    """Quantitative measurements of Left Ventricular volumes."""
    model_config = common_model_config

    lvedv: MeasurementValue = Field(
        default="Not Measured",
        description="Left Ventricle End-Diastolic Volume",
        unit="cc"
    )
    lvesv: MeasurementValue = Field(
        default="Not Measured",
        description="Left Ventricle End-Systolic Volume",
        unit="cc"
    )
    lveddi: MeasurementValue = Field(
        default="Not Measured",
        description="Left Ventricle End-Diastolic Diameter Index",
        unit="cm/m\u00b2"
    )
    lvedvi: MeasurementValue = Field(
        default="Not Measured",
        description="Left Ventricle End-Diastolic Volume Index",
        unit="cc/m\u00b2"
    )

    @field_validator("lvedv", "lvesv", "lveddi", "lvedvi", mode="before")
    @classmethod
    def validate_volume_value(cls, v, info):
        """If LV volume value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == 'lvedv' and not (50 <= val <= 300):
                return "Not Measured"
            if info.field_name == 'lvesv' and not (10 <= val <= 200):
                return "Not Measured"
            if info.field_name == 'lveddi' and not (2.0 <= val <= 4.5):
                return "Not Measured"
            if info.field_name == 'lvedvi' and not (30 <= val <= 150):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LVFunctionIndices(BaseModel):
    """Quantitative measurements of Left Ventricular function indices."""
    model_config = common_model_config

    fs: MeasurementValue = Field(
        default="Not Measured",
        description="Fractional Shortening (%)",
        unit="%"
    )
    tei_index: MeasurementValue = Field(
        default="Not Measured",
        description="myocardial performance index"
    )
    dp_dt: MeasurementValue = Field(
        default="Not Measured",
        description="Rate of rise of LV pressure during isovolumetric contraction"
    )
    sphericity_index: MeasurementValue = Field(
        default="Not Measured",
        description="sphericity index (Ratio comparing the LV's long and short axis dimensions)"
    )

    @field_validator("fs", "tei_index", "dp_dt", "sphericity_index", mode="before")
    @classmethod
    def validate_function_index_value(cls, v, info):
        """If LV function index value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == 'fs' and not (10 <= val <= 50):
                return "Not Measured"
            if info.field_name == 'tei_index' and not (0 <= val <= 1):
                return "Not Measured"
            if info.field_name == 'dp_dt' and not (400 <= val <= 3000):
                return "Not Measured"
            if info.field_name == 'sphericity_index' and not (0 <= val <= 1):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LVStrainMeasures(BaseModel):
    """Quantitative measurements of Left Ventricular strain."""
    model_config = common_model_config

    global_longitudinal_strain: MeasurementValue = Field(
        default="Not Measured",
        description="Average percentage of myocardial shortening in the longitudinal plane",
        unit="%"
    )
    longitudinal_strain_4ch: MeasurementValue = Field(
        default="Not Measured",
        description="Strain measured in the apical four-chamber view",
        unit="%"
    )
    longitudinal_strain_2ch: MeasurementValue = Field(
        default="Not Measured",
        description="Strain from the apical two-chamber view",
        unit="%"
    )
    longitudinal_strain_apical_long_axis: MeasurementValue = Field(
        default="Not Measured",
        description="Strain from the apical long-axis (3-chamber) view",
        unit="%"
    )

    @field_validator("global_longitudinal_strain", "longitudinal_strain_4ch", "longitudinal_strain_2ch", "longitudinal_strain_apical_long_axis", mode="before")
    @classmethod
    def validate_strain_value(cls, v, info):
        """If LV strain value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name in ["global_longitudinal_strain", "longitudinal_strain_4ch", "longitudinal_strain_2ch", "longitudinal_strain_apical_long_axis"] and not (-30 <= val <= -5):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LVRegionalWallMotionScore(BaseModel):
    """Model for a single Regional Wall Motion Score."""
    model_config = common_model_config

    region: LVWallMotionAbnormalityRegionEnum = Field(
        default=LVWallMotionAbnormalityRegionEnum.NOT_ASSESSED,
        description="LV segment name (AHA 17-segment model)"
    )
    score: MeasurementValue = Field(
        default="Not Measured",
        description="Numeric score (1 = Normal, 2 = Hypokinetic, 3 = Severely Hypokinetic, 4 = Akinetic, 5 = Dyskinetic)"
    )

    @field_validator("score", mode="before")
    @classmethod
    def validate_score_value(cls, v, info):
        """If RWMS score value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (1 <= val <= 5):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"

class LVRegionalWallMotionScores(BaseModel):
    """Quantitative measurements of Regional Wall Motion Scores."""
    model_config = common_model_config

    rwmsi: MeasurementValue = Field(
        default="Not Measured",
        description="Regional Wall Motion Score Index"
    )
    rwms: List[LVRegionalWallMotionScore] = Field(
        default_factory=lambda: [LVRegionalWallMotionScore(region=LVWallMotionAbnormalityRegionEnum.NOT_ASSESSED, score="Not Measured")],
        description="Regional Wall Motion Scores"
    )

    @field_validator("rwmsi", mode="before")
    @classmethod
    def validate_rwmsi_value(cls, v, info):
        """If RWMSI value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (1 <= val <= 5):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LVMass(BaseModel):
    """Quantitative measurement of Left Ventricular Mass."""
    model_config = common_model_config

    value: MeasurementValue = Field(
        default="Not Measured",
        description="Left Ventricular Mass",
        unit="gr"
    )


class LVMeasurements(BaseModel):
    """Quantitative measurements related to the Left Ventricle."""
    model_config = common_model_config

    ef: LVEjectionFraction = Field(
        default_factory=LVEjectionFraction,
        description="Ejection Fraction details"
    )
    diameter: LVDiameters = Field(
        default_factory=LVDiameters,
        description="Left Ventricular diameter measurements"
    )
    volumes: LVVolumes = Field(
        default_factory=LVVolumes,
        description="Left Ventricular volume measurements"
    )
    function_indices: LVFunctionIndices = Field(
        default_factory=LVFunctionIndices,
        description="Left Ventricular function indices"
    )
    strain_measures: LVStrainMeasures = Field(
        default_factory=LVStrainMeasures,
        description="Left Ventricular strain measurements"
    )
    regional_wall_motion_scores: LVRegionalWallMotionScores = Field(
        default_factory=LVRegionalWallMotionScores,
        description="Regional Wall Motion Scores"
    )
    mass: LVMass = Field(
        default_factory=LVMass,
        description="Left Ventricular Mass"
    )

# ── Left Ventricle Root ────────────────────────────────────────────────────────────
class LeftVentricle(BaseModel):
    """Top-level model for the Left Ventricle section of the echo report."""
    model_config = common_model_config

    assessment: LVAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the Left Ventricle"
    )
    measurements: LVMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the Left Ventricle"
    )






# ── Right Ventricle ───────────────────────────────────────────────────────────
# ── Right Ventricle Enums ───────────────────────────────────────────────────────────
class RVSizeEnum(str, Enum):
    """Enumeration for Right Ventricular size assessment."""
    NORMAL = "Normal"
    TOP_NORMAL = "Top Normal"
    SMALL = "Small"
    ENLARGED = "Enlarged"
    MILD_ENLARGED = "Mild Enlarged"
    MILD_TO_MODERATE_ENLARGED = "Mild to Moderate Enlarged"
    MODERATE_ENLARGED = "Moderate Enlarged"
    MODERATE_TO_SEVERE_ENLARGED = "Moderate to Severe Enlarged"
    SEVERELY_ENLARGED = "Severe Enlarged"
    NOT_ASSESSED = "Not Assessed"

class RVSystolicFunctionEnum(str, Enum):
    """Enumeration for Right Ventricular systolic function assessment."""
    NORMAL = "Normal"
    PRESERVED = "Preserved"
    MILDLY_REDUCED = "Mildly Reduced"
    MILD_TO_MODERATELY_REDUCED = "Mild to Moderately Reduced"
    MODERATELY_REDUCED = "Moderately Reduced"
    MODERATE_TO_SEVERELY_REDUCED = "Moderate to Severely Reduced"
    SEVERELY_REDUCED = "Severely Reduced"
    NOT_ASSESSED = "Not Assessed"

class RVHypertrophyPresenceEnum(str, Enum):
    """Enumeration for presence of right ventricular hypertrophy."""
    NO = "No"
    YES = "Yes"
    NOT_ASSESSED = "Not Assessed"

class RVHypertrophySeverityEnum(str, Enum):
    """Enumeration for severity of right ventricular hypertrophy."""
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    NOT_ASSESSED = "Not Assessed"


# ── Right Ventricle Assessment Models ───────────────────────────────────────────
class RVHypertrophy(BaseModel):
    """Model for Right Ventricular hypertrophy assessment."""
    model_config = common_model_config

    presence: RVHypertrophyPresenceEnum = Field(
        default=RVHypertrophyPresenceEnum.NOT_ASSESSED,
        description="Presence of right ventricular hypertrophy"
    )
    severity: RVHypertrophySeverityEnum = Field(
        default=RVHypertrophySeverityEnum.NOT_ASSESSED,
        description="Severity of right ventricular hypertrophy"
    )


class RVAssessment(BaseModel):
    """Overall assessment of the Right Ventricle."""
    model_config = common_model_config

    size: RVSizeEnum = Field(
        default=RVSizeEnum.NOT_ASSESSED,
        description="Right Ventricular size assessment"
    )
    systolic_function: RVSystolicFunctionEnum = Field(
        default=RVSystolicFunctionEnum.NOT_ASSESSED,
        description="Right Ventricular systolic function assessment"
    )
    hypertrophy: RVHypertrophy = Field(
        default_factory=RVHypertrophy,
        description="Right Ventricular hypertrophy assessment"
    )


# ── Right Ventricle Measurement Models ───────────────────────────────────────────

class RVDimensions(BaseModel):
    """Quantitative measurements of Right Ventricular dimensions."""
    model_config = common_model_config

    mid_rv_diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Mid Right Ventricular Diameter",
        unit="cm"
    )
    longitudinal_rv_diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Longitudinal Right Ventricular Diameter",
        unit="cm"
    )
    rv_thickness: MeasurementValue = Field(
        default="Not Measured",
        description="Right Ventricular Free Wall Thickness",
        unit="mm"
    )
    rvot_diameter_sax: MeasurementValue = Field(
        default="Not Measured",
        alias="RVOT diameter (in SAX View)",
        description="RVOT diameter in Short Axis View",
        unit="mm"
    )
    rvot_diameter_plax: MeasurementValue = Field(
        default="Not Measured",
        alias="RVOT diameter (in PLAX View)",
        description="RVOT diameter in Parasternal Long Axis View",
        unit="mm"
    )

    @field_validator("mid_rv_diameter", "longitudinal_rv_diameter", "rv_thickness", "rvot_diameter_sax", "rvot_diameter_plax", mode="before")
    @classmethod
    def validate_dimension_value(cls, v, info):
        """If RV dimension value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == 'mid_rv_diameter' and not (1.0 <= val <= 5.0):
                return "Not Measured"
            if info.field_name == 'longitudinal_rv_diameter' and not (2.0 <= val <= 9.0):
                return "Not Measured"
            if info.field_name == 'rv_thickness' and not (1.0 <= val <= 15.0):
                return "Not Measured"
            if info.field_name == 'rvot_diameter_sax' and not (5.0 <= val <= 45.0):
                return "Not Measured"
            if info.field_name == 'rvot_diameter_plax' and not (5.0 <= val <= 45.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class RVAreas(BaseModel):
    """Quantitative measurements of Right Ventricular areas."""
    model_config = common_model_config

    rved_area: MeasurementValue = Field(
        default="Not Measured",
        alias="RVED Area",
        description="Right Ventricular End-Diastolic Area",
        unit="cm\u00b2"
    )
    rves_area: MeasurementValue = Field(
        default="Not Measured",
        alias="RVES Area",
        description="Right Ventricular End-Systolic Area",
        unit="cm\u00b2"
    )
    fac: MeasurementValue = Field(
        default="Not Measured",
        alias="FAC",
        description="Fractional Area Change",
        unit="%"
    )

    @field_validator("rved_area", "rves_area", "fac", mode="before")
    @classmethod
    def validate_area_value(cls, v, info):
        """If RV area value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == 'rved_area' and not (5.0 <= val <= 40.0):
                return "Not Measured"
            if info.field_name == 'rves_area' and not (2.0 <= val <= 30.0):
                return "Not Measured"
            if info.field_name == 'fac' and not (10 <= val <= 70):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class RVFunctionIndices(BaseModel):
    """Quantitative measurements of Right Ventricular function indices."""
    model_config = common_model_config

    rv_mpi: MeasurementValue = Field(
        default="Not Measured",
        alias="RV MPI",
        description="Myocardial Performance Index (Tei Index) of RV"
    )
    tapse: MeasurementValue = Field(
        default="Not Measured",
        alias="TAPSE",
        description="Tricuspid Annular Plane Systolic Excursion",
        unit="mm"
    )
    sm: MeasurementValue = Field(
        default="Not Measured",
        alias="Sm",
        description="Tricuspid annular systolic velocity",
        unit="cm/sec"
    )

    @field_validator("rv_mpi")
    @classmethod
    def validate_rv_mpi(cls, v, info):
        """If RV MPI value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            value = float(v)
            if not 0.0 <= value <= 1.5:
                return "Not Measured"
        except Exception:
            return "Not Measured"
        return v

    @field_validator("tapse")
    @classmethod
    def validate_tapse(cls, v, info):
        """If TAPSE value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            value = float(v)
            if not 5.0 <= value <= 40.0:
                return "Not Measured"
        except Exception:
            return "Not Measured"
        return v

    @field_validator("sm")
    @classmethod
    def validate_sm(cls, v, info):
        """If Sm value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            value = float(v)
            if not 0.0 <= value <= 20.0:
                return "Not Measured"
        except Exception:
            return "Not Measured"
        return v


class RVMeasurements(BaseModel):
    """Quantitative measurements related to the Right Ventricle."""
    model_config = common_model_config

    dimensions: RVDimensions = Field(
        default_factory=RVDimensions,
        description="Right Ventricular dimension measurements"
    )
    areas: RVAreas = Field(
        default_factory=RVAreas,
        description="Right Ventricular area measurements"
    )
    function_indices: RVFunctionIndices = Field(
        default_factory=RVFunctionIndices,
        description="Right Ventricular function indices"
    )

# ── Right Ventricle Root ───────────────────────────────────────────────────────────
class RightVentricle(BaseModel):
    """Top-level model for the Right Ventricle section of the echo report."""
    model_config = common_model_config

    assessment: RVAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the Right Ventricle"
    )
    measurements: RVMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the Right Ventricle"
    )





# ── Left Atrium ───────────────────────────────────────────────────────────────
# ── Left Atrium Enums ───────────────────────────────────────────────────────────────
class LASizeEnum(str, Enum):
    """Enumeration for Left Atrium size assessment."""
    NORMAL = "Normal"
    TOP_NORMAL = "Top Normal"
    ENLARGED = "Enlarged"
    MILD_ENLARGED = "Mild Enlarged"
    MODERATE_ENLARGED = "Moderate Enlarged"
    SEVERELY_ENLARGED = "Severe Enlarged"
    NOT_ASSESSED = "Not Assessed"

class LASpontaneousEchoContrastEnum(str, Enum):
    """Enumeration for presence and severity of spontaneous echo contrast (SEC or 'smoke') in LA."""
    NO = "No"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    NOT_ASSESSED = "Not Assessed"

class LAClotPresenceEnum(str, Enum):
    """Enumeration for presence of thrombus in Left Atrium."""
    NO = "No"
    SMALL = "Small"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class LAACSpontaneousEchoContrastEnum(str, Enum):
    """Enumeration for presence and severity of spontaneous echo contrast (SEC or 'smoke') in LAA."""
    NO = "No"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    NOT_ASSESSED = "Not Assessed"

class LAACClotPresenceEnum(str, Enum):
    """Enumeration for presence of clot in LAA."""
    NO = "No"
    SMALL = "Small"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class LAACClosedInPreviousSurgeryEnum(str, Enum):
    """Enumeration for previous surgical closure of LAA."""
    YES = "Yes"
    PARTIAL = "Partial"
    NO = "No"
    UNKNOWN = "Unknown"
    NOT_ASSESSED = "Not Assessed"


# ── Left Atrium Assessment Models ─────────────────────────────────────────────
class LAAppendageAssessment(BaseModel):
    """Model for Left Atrial Appendage assessment details."""
    model_config = common_model_config

    spontaneous_echo_contrast: LAACSpontaneousEchoContrastEnum = Field(
        default=LAACSpontaneousEchoContrastEnum.NOT_ASSESSED,
        alias="Spontaneous Echo Contrast",
        description="Presence and severity of spontaneous echo contrast (SEC or 'smoke') in LAA"
    )
    clot: LAACClotPresenceEnum = Field(
        default=LAACClotPresenceEnum.NOT_ASSESSED,
        description="Presence of clot in LAA"
    )
    closed_in_previous_surgery: LAACClosedInPreviousSurgeryEnum = Field(
        default=LAACClosedInPreviousSurgeryEnum.NOT_ASSESSED,
        alias="Closed in Previous Surgery",
        description="Previous surgical closure of LAA"
    )


class LAAssessment(BaseModel):
    """Overall assessment of the Left Atrium."""
    model_config = common_model_config

    size: LASizeEnum = Field(
        default=LASizeEnum.NOT_ASSESSED,
        description="Left Atrium size assessment"
    )
    spontaneous_echo_contrast: LASpontaneousEchoContrastEnum = Field(
        default=LASpontaneousEchoContrastEnum.NOT_ASSESSED,
        alias="Spontaneous Echo Contrast (Smoke)",
        description="Presence and severity of spontaneous echo contrast (SEC or 'smoke')"
    )
    clot: LAClotPresenceEnum = Field(
        default=LAClotPresenceEnum.NOT_ASSESSED,
        description="Presence of thrombus in Left Atrium"
    )
    appendage: LAAppendageAssessment = Field(
        default_factory=LAAppendageAssessment,
        alias="Appendage (LAA)",
        description="Left Atrial Appendage assessment details"
    )


# ── Left Atrium Measurement Models ─────────────────────────────────────────────

class LAVolumes(BaseModel):
    """Quantitative measurements of Left Atrial volumes."""
    model_config = common_model_config

    biplane_volume: MeasurementValue = Field(
        default="Not Measured",
        alias="Biplane Volume",
        description="Left Atrial Volume",
        unit="cc"
    )
    volume_4ch_view: MeasurementValue = Field(
        default="Not Measured",
        alias="Volume (4Ch View)",
        description="Left Atrial Volume from 4-Chamber View",
        unit="cc"
    )
    volume_2ch_view: MeasurementValue = Field(
        default="Not Measured",
        alias="Volume (2Ch View)",
        description="Left Atrial Volume from 2-Chamber View",
        unit="cc"
    )

    @field_validator("biplane_volume", "volume_4ch_view", "volume_2ch_view", mode="before")
    @classmethod
    def validate_volume_value(cls, v, info):
        """If LA volume value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name in ["biplane_volume", "volume_4ch_view", "volume_2ch_view"] and not (10 <= val <= 250):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LAFunctionIndices(BaseModel):
    """Quantitative measurements of Left Atrial function indices."""
    model_config = common_model_config

    la_ef: MeasurementValue = Field(
        default="Not Measured",
        alias="LA EF",
        description="Left Atrial Ejection Fraction",
        unit="%"
    )
    active_ef: MeasurementValue = Field(
        default="Not Measured",
        alias="Active EF",
        description="Active Ejection Fraction",
        unit="%"
    )
    passive_ef: MeasurementValue = Field(
        default="Not Measured",
        alias="Passive EF",
        description="Passive Ejection Fraction",
        unit="%"
    )

    @field_validator("la_ef", "active_ef", "passive_ef", mode="before")
    @classmethod
    def validate_function_index_value(cls, v, info):
        """If LA function index value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == 'la_ef' and not (10 <= val <= 90):
                return "Not Measured"
            if info.field_name == 'active_ef' and not (5 <= val <= 60):
                return "Not Measured"
            if info.field_name == 'passive_ef' and not (5 <= val <= 60):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LAStrainMeasures(BaseModel):
    """Quantitative measurements of Left Atrial strain."""
    model_config = common_model_config

    global_strain_2d_ste: MeasurementValue = Field(
        default="Not Measured",
        alias="Global Strain (2D-STE)",
        description="Global Strain by 2D Speckle Tracking Echocardiography",
        unit="%"
    )

    @field_validator("global_strain_2d_ste", mode="before")
    @classmethod
    def validate_strain_value(cls, v, info):
        """If LA strain value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (5 <= val <= 60):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LAAppendageMeasurements(BaseModel):
    """Quantitative measurements of Left Atrial Appendage."""
    model_config = common_model_config

    velocity: MeasurementValue = Field(
        default="Not Measured",
        alias="Velocity",
        description="Left Atrial Appendage velocity",
        unit="cm/sec"
    )

    @field_validator("velocity", mode="before")
    @classmethod
    def validate_velocity_value(cls, v, info):
        """Validator for LAA velocity value."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (10 <= val <= 100):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class LAMeasurements(BaseModel):
    """Quantitative measurements related to the Left Atrium."""
    model_config = common_model_config

    diameter: MeasurementValue = Field(
        default="Not Measured",
        alias="Diameter",
        description="Left Atrial Diameter",
        unit="cm"
    )
    area: MeasurementValue = Field(
        default="Not Measured",
        alias="Area",
        description="Left Atrial Area",
        unit="cm\u00b2"
    )
    volumes: LAVolumes = Field(
        default_factory=LAVolumes,
        alias="Volumes",
        description="Left Atrial volume measurements"
    )
    function_indices: LAFunctionIndices = Field(
        default_factory=LAFunctionIndices,
        alias="Function Indices",
        description="Left Atrial function indices"
    )
    strain_measures: LAStrainMeasures = Field(
        default_factory=LAStrainMeasures,
        alias="Strain Measures",
        description="Left Atrial strain measurements"
    )
    appendage: LAAppendageMeasurements = Field(
        default_factory=LAAppendageMeasurements,
        alias="Appendage (LAA)",
        description="Quantitative measurements for Left Atrial Appendage"
    )

    @field_validator("diameter", "area", mode="before")
    @classmethod
    def validate_simple_measurement_value(cls, v, info):
        """If LA measurement value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == 'diameter' and not (2.0 <= val <= 7.0):
                return "Not Measured"
            if info.field_name == 'area' and not (5.0 <= val <= 60.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── Left Atrium Root ───────────────────────────────────────────────────────────
class LeftAtrium(BaseModel):
    """Top-level model for the Left Atrium section of the echo report."""
    model_config = common_model_config

    assessment: LAAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the Left Atrium"
    )
    measurements: LAMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the Left Atrium"
    )






# ── Right Atrium ──────────────────────────────────────────────────────────────
# ── Right Atrium Enums ──────────────────────────────────────────────────────────────
class RASizeEnum(str, Enum):
    """Enumeration for Right Atrium size assessment."""
    NORMAL = "Normal"
    TOP_NORMAL = "Top Normal"
    ENLARGED = "Enlarged"
    MILD_ENLARGED = "Mild Enlarged"
    MODERATE_ENLARGED = "Moderate Enlarged"
    SEVERELY_ENLARGED = "Severe Enlarged"
    NOT_ASSESSED = "Not Assessed"

class RASpontaneousEchoContrastEnum(str, Enum):
    """Enumeration for presence and severity of spontaneous echo contrast (SEC or 'smoke') in RA."""
    NO = "No"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    NOT_ASSESSED = "Not Assessed"

class RAClotPresenceEnum(str, Enum):
    """Enumeration for presence of thrombus in Right Atrium."""
    NO = "No"
    SMALL = "Small"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class RAASpontaneousEchoContrastEnum(str, Enum):
    """Enumeration for presence and severity of spontaneous echo contrast (SEC or 'smoke') in RAA."""
    NO = "No"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    NOT_ASSESSED = "Not Assessed"

class RAACClotPresenceEnum(str, Enum):
    """Enumeration for presence of clot in RAA."""
    NO = "No"
    SMALL = "Small"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class RAACClosedInPreviousSurgeryEnum(str, Enum):
    """Enumeration for previous surgical closure of RAA."""
    YES = "Yes"
    PARTIAL = "Partial"
    NO = "No"
    UNKNOWN = "Unknown"
    NOT_ASSESSED = "Not Assessed"


# ── Right Atrium Assessment Models ─────────────────────────────────────────────
class RAAppendageAssessment(BaseModel):
    """Model for Right Atrial Appendage assessment details."""
    model_config = common_model_config

    spontaneous_echo_contrast: RAASpontaneousEchoContrastEnum = Field(
        default=RAASpontaneousEchoContrastEnum.NOT_ASSESSED,
        alias="Spontaneous Echo Contrast",
        description="Presence and severity of spontaneous echo contrast (SEC or 'smoke') in RAA"
    )
    clot: RAACClotPresenceEnum = Field(
        default=RAACClotPresenceEnum.NOT_ASSESSED,
        description="Presence of clot in RAA"
    )
    closed_in_previous_surgery: RAACClosedInPreviousSurgeryEnum = Field(
        default=RAACClosedInPreviousSurgeryEnum.NOT_ASSESSED,
        alias="Closed in Previous Surgery",
        description="Previous surgical closure of RAA"
    )


class RAAssessment(BaseModel):
    """Overall assessment of the Right Atrium."""
    model_config = common_model_config

    size: RASizeEnum = Field(
        default=RASizeEnum.NOT_ASSESSED,
        description="Right Atrium size assessment"
    )
    spontaneous_echo_contrast: RASpontaneousEchoContrastEnum = Field(
        default=RASpontaneousEchoContrastEnum.NOT_ASSESSED,
        alias="Spontaneous Echo Contrast (Smoke)",
        description="Presence and severity of spontaneous echo contrast (SEC or 'smoke')"
    )
    clot: RAClotPresenceEnum = Field(
        default=RAClotPresenceEnum.NOT_ASSESSED,
        description="Presence of thrombus in Right Atrium"
    )
    appendage: RAAppendageAssessment = Field(
        default_factory=RAAppendageAssessment,
        alias="Appendage (RAA)",
        description="Right Atrial Appendage assessment details"
    )


# ── Right Atrium Measurement Models ─────────────────────────────────────────────

class RAVolumes(BaseModel):
    """Quantitative measurements of Right Atrial volumes."""
    model_config = common_model_config

    volume_4ch_view: MeasurementValue = Field(
        default="Not Measured",
        alias="Volume (4Ch View)",
        description="Right Atrial Volume from 4-Chamber Apical View",
        unit="cc"
    )

    @field_validator("volume_4ch_view", mode="before")
    @classmethod
    def validate_volume_value(cls, v, info):
        """Validator for RA volume value."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")
        if isinstance(v, (int, float)):
            val = float(v)
            if not (10 <= val <= 250):
                raise ValueError("Volume (4Ch View) value must be between 10 and 250 cc")
            return val
        raise ValueError("Volume value must be a number or 'Not Measured'")


class RAFunctionIndices(BaseModel):
    """Quantitative measurements of Right Atrial function indices."""
    model_config = common_model_config

    ra_ef: MeasurementValue = Field(
        default="Not Measured",
        alias="RA EF",
        description="Right Atrial Ejection Fraction",
        unit="%"
    )
    active_ef: MeasurementValue = Field(
        default="Not Measured",
        alias="Active EF",
        description="Active Ejection Fraction",
        unit="%"
    )
    passive_ef: MeasurementValue = Field(
        default="Not Measured",
        alias="Passive EF",
        description="Passive Ejection Fraction",
        unit="%"
    )

    @field_validator("ra_ef", "active_ef", "passive_ef", mode="before")
    @classmethod
    def validate_function_index_value(cls, v, info):
        """Validator for RA function index values."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")
        if isinstance(v, (int, float)):
            val = float(v)
            # Specific range checks based on the JSON schema
            if cls.__name__ == 'RAFunctionIndices':
                 if 'ra_ef' in cls.__annotations__ and (val < 10 or val > 90):
                     raise ValueError("RA EF value must be between 10 and 90 %")
                 if 'active_ef' in cls.__annotations__ and (val < 5 or val > 60):
                     raise ValueError("Active EF value must be between 5 and 60 %")
                 if 'passive_ef' in cls.__annotations__ and (val < 5 or val > 60):
                     raise ValueError("Passive EF value must be between 5 and 60 %")
            return val
        raise ValueError("Function Index value must be a number or 'Not Measured'")


class RAStrainMeasures(BaseModel):
    """Quantitative measurements of Right Atrial strain."""
    model_config = common_model_config

    global_strain_2d_ste: MeasurementValue = Field(
        default="Not Measured",
        alias="Global Strain (2D-STE)",
        description="Global Strain by 2D Speckle Tracking Echocardiography",
        unit="%"
    )

    @field_validator("global_strain_2d_ste", mode="before")
    @classmethod
    def validate_strain_value(cls, v, info):
        """Validator for RA strain value."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")
        if isinstance(v, (int, float)):
            val = float(v)
            if not (5 <= val <= 60):
                raise ValueError("Global Strain (2D-STE) value must be between 5 and 60 %")
            return val
        raise ValueError("Strain value must be a number or 'Not Measured'")


class RAAppendageMeasurements(BaseModel):
    """Quantitative measurements of Right Atrial Appendage."""
    model_config = common_model_config

    velocity: MeasurementValue = Field(
        default="Not Measured",
        alias="Velocity",
        description="Right Atrial Appendage velocity",
        unit="cm/sec"
    )

    @field_validator("velocity", mode="before")
    @classmethod
    def validate_velocity_value(cls, v, info):
        """Validator for RAA velocity value."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")
        if isinstance(v, (int, float)):
            val = float(v)
            if not (10 <= val <= 100):
                raise ValueError("Velocity value must be between 10 and 100 cm/sec")
            return val
        raise ValueError("Velocity value must be a number or 'Not Measured'")


class RAMeasurements(BaseModel):
    """Quantitative measurements related to the Right Atrium."""
    model_config = common_model_config

    diameter: MeasurementValue = Field(
        default="Not Measured",
        alias="Diameter",
        description="Right Atrial Diameter",
        unit="cm"
    )
    area: MeasurementValue = Field(
        default="Not Measured",
        alias="Area",
        description="Right Atrial Area",
        unit="cm\u00b2"
    )
    volumes: RAVolumes = Field(
        default_factory=RAVolumes,
        alias="Volumes",
        description="Right Atrial volume measurements"
    )
    function_indices: RAFunctionIndices = Field(
        default_factory=RAFunctionIndices,
        alias="Function Indices",
        description="Right Atrial function indices"
    )
    strain_measures: RAStrainMeasures = Field(
        default_factory=RAStrainMeasures,
        alias="Strain Measures",
        description="Right Atrial strain measurements"
    )
    appendage: RAAppendageMeasurements = Field(
        default_factory=RAAppendageMeasurements,
        alias="Appendage (RAA)",
        description="Quantitative measurements for Right Atrial Appendage"
    )

    @field_validator("diameter", "area", mode="before")
    @classmethod
    def validate_simple_measurement_value(cls, v, info):
        """Validator for simple RA measurement values (Diameter, Area)."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == 'diameter' and not (2.0 <= val <= 7.0):
                return "Not Measured"
            if info.field_name == 'area' and not (5.0 <= val <= 60.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── Right Atrium Root ──────────────────────────────────────────────────────────
class RightAtrium(BaseModel):
    """Top-level model for the Right Atrium section of the echo report."""
    model_config = common_model_config

    assessment: RAAssessment = Field(
        ...,
        description="Assessment findings for the Right Atrium"
    )
    measurements: RAMeasurements = Field(
        ...,
        description="Quantitative measurements for the Right Atrium"
    )


















# ── Pericardium  ───────────────────────────────────────────────────────────────
# ── Pericardium Enums ───────────────────────────────────────────────────────────────
class PericardiumMorphologyEnum(str, Enum):
    """Enumeration for pericardial morphology."""
    NORMAL = "Normal"
    THICKENED = "Thickened"
    CALCIFIED = "Calcified"
    ABSENT = "Absent"
    NOT_ASSESSED = "Not Assessed"

class EffusionPresenceEnum(str, Enum):
    """Enumeration for presence assessment."""
    NO = "No"
    YES = "Yes"
    NOT_ASSESSED = "Not Assessed"

class EffusionSizeEnum(str, Enum):
    """Enumeration for pericardial effusion size."""
    SMALL = "Small"
    SMALL_TO_MODERATE = "Small to Moderate"
    MODERATE = "Moderate"
    MODERATE_TO_LARGE = "Moderate to Large"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class EffusionDistributionEnum(str, Enum):
    """Enumeration for effusion distribution."""
    CIRCUMFERENTIAL = "Circumferential"
    POSTERIOR = "Posterior"
    ANTERIOR = "Anterior"
    LOCALIZED = "Localized"
    NOT_ASSESSED = "Not Assessed"

class EffusionHemodynamicImpactEnum(str, Enum):
    """Enumeration for hemodynamic impact of effusion."""
    NONE = "None"
    TAMPONADE_PHYSIOLOGY = "Tamponade Physiology"
    EFFUSIVE_CONSTRICTIVE = "Effusive-Constrictive"
    NOT_ASSESSED = "Not Assessed"

class ConstrictivePericarditisFeatureEnum(str, Enum):
    """Enumeration for features of constrictive pericarditis."""
    SEPTAL_BOUNCE = "Septal Bounce"
    RESPIRATORY_VARIATION_IN_AV_INFLOW = "Respiratory Variation in AV inflow"
    ANNULUS_REVERSUS = "Annulus Reversus"
    ANNULUS_PARADOXUS = "Annulus Paradoxus"
    DILATED_IVC_WITH_REDUCED_COLLAPSE = "Dilated IVC with Reduced Collapse"
    NOT_ASSESSED = "Not Assessed"

# ── Pericardium Assessment Models ─────────────────────────────────────────────────────────────────────
class Effusion(BaseModel):
    """Model for pericardial effusion details."""
    model_config = common_model_config

    presence: EffusionPresenceEnum = Field(
        default=EffusionPresenceEnum.NOT_ASSESSED,
        description="Presence of pericardial effusion"
    )
    size: EffusionSizeEnum = Field(
        default=EffusionSizeEnum.NOT_ASSESSED,
        description="Size/grade of pericardial effusion"
    )
    distribution: EffusionDistributionEnum = Field(
        default=EffusionDistributionEnum.NOT_ASSESSED,
        description="Anatomical distribution of pericardial effusion"
    )
    hemodynamic_impact: EffusionHemodynamicImpactEnum = Field(
        default=EffusionHemodynamicImpactEnum.NOT_ASSESSED,
        description="Hemodynamic consequence of the effusion"
    )

class ConstrictivePericarditis(BaseModel):
    """Model for assessment of constrictive pericarditis."""
    model_config = common_model_config

    presence: EffusionPresenceEnum = Field(
        default=EffusionPresenceEnum.NOT_ASSESSED,
        description="Presence of constrictive physiology"
    )
    features: List[ConstrictivePericarditisFeatureEnum] = Field(
        default_factory=lambda: [ConstrictivePericarditisFeatureEnum.NOT_ASSESSED],
        description="Echocardiographic features supportive of constriction"
    )


# ── Full Pericardium Assessment Root ─────────────────────────────────────────────
class PericardiumAssessment(BaseModel):
    """Overall assessment of the pericardium."""
    model_config = common_model_config

    morphology: PericardiumMorphologyEnum = Field(
        default=PericardiumMorphologyEnum.NOT_ASSESSED,
        description="Anatomical state of the pericardium"
    )
    effusion: Effusion = Field(
        default_factory=lambda: Effusion(),
        description="Pericardial effusion details"
    )
    constrictive_pericarditis: ConstrictivePericarditis = Field(
        default_factory=lambda: ConstrictivePericarditis(),
        description="Assessment of constrictive pericarditis"
    )

# ── Pericardium Measurement Models ─────────────────────────────────────────────────────────────────────
class EffusionSizeMeasurement(BaseModel):
    """Quantitative measurements of effusion size."""
    model_config = common_model_config

    posterior: MeasurementValue = Field(
        default="Not Measured",
        description="Measurement of effusion posterior to LV",
        unit="mm"
    )
    anterior: MeasurementValue = Field(
        default="Not Measured",
        description="Measurement of effusion anterior to RV",
        unit="mm"
    )

    @field_validator("posterior", "anterior", mode="before")
    @classmethod
    def validate_measurement(cls, v):
        """If effusion measurement value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (0 <= val <= 50):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"

# ── Full Pericardium Measurements Root ─────────────────────────────────────────────
class PericardiumMeasurements(BaseModel):
    """Quantitative measurements related to the pericardium."""
    model_config = common_model_config

    pericardial_thickness: MeasurementValue = Field(
        default="Not Measured",
        description="Thickness of pericardium",
        unit="mm"
    )
    effusion_size: EffusionSizeMeasurement = Field(
        default_factory=EffusionSizeMeasurement,
        description="Quantitative effusion measurements"
    )

    @field_validator("pericardial_thickness", mode="before")
    @classmethod
    def validate_thickness(cls, v):
        """If pericardial thickness value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (0.5 <= val <= 10.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"













# ── Shared Enums ───────────────────────────────────────────────────────────────
class PresenceEnum(str, Enum):
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class SeverityEnum(str, Enum):
    NO = "No"
    TRIVIAL = "Trivial"
    MILD = "Mild"
    MILD_TO_MODERATE = "Mild to Moderate"
    MODERATE = "Moderate"
    MODERATE_TO_SEVERE = "Moderate to Severe"
    SEVERE = "Severe"
    VERY_SEVERE = "Very Severe"
    NOT_ASSESSED = "Not Assessed"

class ProstheticTypeEnum(str, Enum):
    MECHANICAL_BILEAFLET = "Mechanical Bileaflet"
    MECHANICAL_MONOLEAFLET = "Mechanical Monoleaflet"
    BIOPROSTHETIC = "Bioprosthetic"
    NOT_APPLICABLE = "Not Applicable"
    NOT_ASSESSED = "Not Assessed"

class FunctionEnum(str, Enum):
    GOOD_FUNCTION = "Good Function"
    MALFUNCTION = "Malfunction"
    NOT_ASSESSED = "Not Assessed"


# ── Mitral Valve ───────────────────────────────────────────────────────────────
# ── Mitral Enums ───────────────────────────────────────────────────────────
class MitralShapeEnum(str, Enum):
    NORMAL = "Normal"
    THICKENED = "Thickened"
    CALCIFIED = "Calcified"
    PROLAPTIC = "Prolaptic"
    MYXOMATOUS = "Myxomatous"
    REPAIRED = "Repaired"
    FLAIL = "Flail"
    NOT_ASSESSED = "Not Assessed"

class SAMEnum(str, Enum):
    NO = "No"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    NOT_ASSESSED = "Not Assessed"


# ── Mitral Valve Assessment Models ─────────────────────────────────────────────
class MitralStenosis(BaseModel):
    """Model for mitral stenosis assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of Mitral Stenosis"
    )


class MitralRegurgitation(BaseModel):
    """Model for mitral regurgitation assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of MR"
    )
    paravalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        alias="Paravalvular Leak",
        description="Severity of paravalvular leak"
    )
    transvalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        alias="Transvalvular Leak",
        description="Severity of transvalvular leak"
    )


class MitralProsthetic(BaseModel):
    """Model for mitral prosthetic valve assessment."""
    model_config = common_model_config

    present: PresenceEnum = Field(
        default=PresenceEnum.NOT_ASSESSED,
        description="Presence of a mitral prosthetic valve"
    )
    type: ProstheticTypeEnum = Field(
        default=ProstheticTypeEnum.NOT_ASSESSED,
        description="Type of mitral prosthetic valve"
    )
    function: FunctionEnum = Field(
        default=FunctionEnum.NOT_ASSESSED,
        description="Function of the mitral prosthetic valve"
    )


# ── Full Mitral Valve Assessment Root ───────────────────────────────────────────────
class MitralValveAssessment(BaseModel):
    """Overall assessment of the mitral valve."""
    model_config = common_model_config

    shape: MitralShapeEnum = Field(
        default=MitralShapeEnum.NOT_ASSESSED,
        description="Anatomical state of the mitral valve"
    )
    sam: SAMEnum = Field(
        default=SAMEnum.NOT_ASSESSED,
        alias="SAM", # Explicit alias needed as generator would make it "Sam"
        description="Systolic Anterior Motion of the mitral valve"
    )
    stenosis: MitralStenosis = Field(
        default_factory=lambda: MitralStenosis(),
        description="Mitral stenosis assessment"
    )
    regurgitation: MitralRegurgitation = Field(
        default_factory=lambda: MitralRegurgitation(),
        description="Mitral regurgitation assessment"
    )
    prosthetic: MitralProsthetic = Field(
        default_factory=lambda: MitralProsthetic(),
        description="Mitral prosthetic valve assessment"
    )


# ── Mitral Valve Measurements ───────────────────────────────────────────────────
class MitralDimensions(BaseModel):
    """Quantitative measurements of mitral valve dimensions."""
    model_config = common_model_config

    annulus_diameter: MeasurementValue = Field(
        default="Not Measured",
        alias="Annulus Diameter",
        description="Mitral annulus diameter",
        unit="cm"
    )
    amvl_length: MeasurementValue = Field(
        default="Not Measured",
        alias="AMVL Length",
        description="Anterior Mitral Valve Leaflet length",
        unit="cm"
    )
    pmvl_length: MeasurementValue = Field(
        default="Not Measured",
        alias="PMVL Length",
        description="Posterior Mitral Valve Leaflet length",
        unit="cm"
    )

    @field_validator("annulus_diameter", "amvl_length", "pmvl_length", mode="before")
    @classmethod
    def validate_dimensions(cls, v, info):
        """If mitral dimension value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "annulus_diameter" and not (2.0 <= val <= 5.0):
                return "Not Measured"
            elif field_name in ["amvl_length", "pmvl_length"] and not (1.5 <= val <= 4.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class MitralRegurgitationParameters(BaseModel):
    """Quantitative measurements related to mitral regurgitation."""
    model_config = common_model_config

    mr_rv: MeasurementValue = Field(
        default="Not Measured",
        alias="MR RV",
        description="Mitral Regurgitation Regurgitant Volume",
        unit="ml"
    )
    mr_roa: MeasurementValue = Field(
        default="Not Measured",
        alias="MR ROA",
        description="Mitral Regurgitation Regurgitant Orifice Area",
        unit="cm²"
    )
    mr_vc_area: MeasurementValue = Field(
        default="Not Measured",
        alias="MR VC Area",
        description="Mitral Regurgitation Vena Contracta Area",
        unit="cm²"
    )

    @field_validator("mr_rv", "mr_roa", "mr_vc_area", mode="before")
    @classmethod
    def validate_mr_params(cls, v, info):
        """If mitral regurgitation parameter value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "mr_rv" and not (1.0 <= val <= 200.0):
                return "Not Measured"
            elif field_name == "mr_roa" and not (0.01 <= val <= 1.5):
                return "Not Measured"
            elif field_name == "mr_vc_area" and not (0.01 <= val <= 1.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class MitralStenosisGradients(BaseModel):
    """Quantitative measurements of mitral valve stenosis gradients."""
    model_config = common_model_config

    mean_gradient: MeasurementValue = Field(
        default="Not Measured",
        alias="Mean Gradient",
        description="Mitral valve mean pressure gradient",
        unit="mmHg"
    )
    pht: MeasurementValue = Field(
        default="Not Measured",
        # No alias needed, generator handles "Pht"
        description="Mitral valve Pressure Half-Time",
        unit="ms"
    )

    @field_validator("mean_gradient", "pht", mode="before")
    @classmethod
    def validate_ms_gradients(cls, v, info):
        """If mitral stenosis gradient value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "mean_gradient" and not (0.0 <= val <= 40.0):
                return "Not Measured"
            elif field_name == "pht" and not (30.0 <= val <= 400.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class MorphoFunctionalIndices(BaseModel):
    """Quantitative morpho-functional measurements of the mitral valve."""
    model_config = common_model_config

    tenting_area: MeasurementValue = Field(
        default="Not Measured",
        alias="Tenting Area",
        description="Mitral valve tenting area",
        unit="cm²"
    )
    coaptation_depth: MeasurementValue = Field(
        default="Not Measured",
        alias="Coaptation Depth",
        description="Mitral valve coaptation depth",
        unit="mm"
    )
    ivrt: MeasurementValue = Field(
        default="Not Measured",
        description="Isovolumetric Relaxation Time",
        unit="ms"
    )

    @field_validator("tenting_area", "coaptation_depth", "ivrt", mode="before")
    @classmethod
    def validate_morpho_functional(cls, v, info):
        """If morpho-functional index value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "tenting_area" and not (0.0 <= val <= 6.0):
                return "Not Measured"
            elif field_name == "coaptation_depth" and not (0.0 <= val <= 20.0):
                return "Not Measured"
            elif field_name == "ivrt" and not (0.0 <= val <= 150.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class MitralDopplerMeasurements(BaseModel):
    """Quantitative Doppler measurements related to the mitral valve (Diastolic Function)."""
    model_config = common_model_config

    e_septal: MeasurementValue = Field(
        default="Not Measured",
        alias="E Septal",
        description="Mitral annular E' velocity (septal)",
        unit="cm/sec"
    )
    e_lateral: MeasurementValue = Field(
        default="Not Measured",
        alias="E Lateral",
        description="Mitral annular E' velocity (lateral)",
        unit="cm/sec"
    )
    a: MeasurementValue = Field(
        default="Not Measured",
        alias="A", # Explicit alias needed as generator would make it "A"
        description="Mitral valve A wave velocity",
        unit="cm/sec"
    )
    s: MeasurementValue = Field(
        default="Not Measured",
        alias="S", # Explicit alias needed as generator would make it "S"
        description="Pulmonary vein S wave velocity",
        unit="cm/sec"
    )
    mve: MeasurementValue = Field(
        default="Not Measured",
        alias="MVE", # Explicit alias needed as generator would make it "Mve"
        description="Mitral Valve E wave velocity",
        unit="m/s"
    )
    vti: MeasurementValue = Field(
        default="Not Measured",
        alias="VTI", # Explicit alias needed as generator would make it "Vti"
        description="Mitral Valve Velocity Time Integral",
        unit="cm"
    )
    vp: MeasurementValue = Field(
        default="Not Measured",
        alias="Vp", # Explicit alias needed as generator would make it "Vp"
        description="Propagation Velocity",
        unit="cm/sec"
    )
    e_a_ratio: MeasurementValue = Field(
        default="Not Measured",
        alias="E/A Ratio",
        description="Ratio of Mitral valve E to A wave velocity"
    )
    e_e_prime_ratio: MeasurementValue = Field(
        default="Not Measured",
        alias="E/e' Ratio",
        description="Ratio of Mitral valve E wave to average annular E' velocity"
    )
    deceleration_time: MeasurementValue = Field(
        default="Not Measured",
        alias="Deceleration Time",
        description="Mitral valve E wave deceleration time",
        unit="ms"
    )

    @field_validator(
        "e_septal",
        "e_lateral",
        "a",
        "s",
        "mve",
        "vti",
        "vp",
        "e_a_ratio",
        "e_e_prime_ratio",
        "deceleration_time",
        mode="before"
    )
    @classmethod
    def validate_mitral_doppler(cls, v, info):
        """If mitral Doppler measurement value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "e_septal" and not (2.0 <= val <= 16.0):
                return "Not Measured"
            elif field_name == "e_lateral" and not (4.0 <= val <= 20.0):
                return "Not Measured"
            elif field_name == "a" and not (2.0 <= val <= 14.0):
                return "Not Measured"
            elif field_name == "s" and not (5.0 <= val <= 112.0):
                return "Not Measured"
            elif field_name == "vp" and not (20.0 <= val <= 90.0):
                return "Not Measured"
            elif field_name == "mve" and not (0.3 <= val <= 3.5):
                return "Not Measured"
            elif field_name == "vti" and not (5.0 <= val <= 150.0):
                return "Not Measured"
            elif field_name == "e_a_ratio" and not (0.5 <= val <= 5.0):
                return "Not Measured"
            elif field_name == "e_e_prime_ratio" and not (3.0 <= val <= 30.0):
                return "Not Measured"
            elif field_name == "deceleration_time" and not (100.0 <= val <= 400.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class AnnulusMotion(BaseModel):
    """Quantitative measurements of mitral annular motion."""
    model_config = common_model_config

    mapse: MeasurementValue = Field(
        default="Not Measured",
        alias="MAPSE", # Explicit alias needed as generator would make it "Mapse"
        description="Mitral Annular Plane Systolic Excursion",
        unit="cm"
    )
    tmad: MeasurementValue = Field(
        default="Not Measured",
        alias="TMAD", # Explicit alias needed as generator would make it "Tmad"
        description="Tricuspid Annular Motion during Diastole (should this be Mitral? Assuming typo and keeping TMAD for now)",
        unit="mm"
    )

    @field_validator("mapse", "tmad", mode="before")
    @classmethod
    def validate_mapse(cls, v, info):
        """If MAPSE or TMAD value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (5.0 <= val <= 25.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── Final MitralValveMeasurements Root ──────────────────────────────────────────
class MitralValveMeasurements(BaseModel):
    """Quantitative measurements related to the mitral valve."""
    model_config = common_model_config

    area: MeasurementValue = Field(
        default="Not Measured",
        description="Mitral Valve Area",
        unit="cm²"
    )
    dimensions: MitralDimensions = Field(
        default_factory=MitralDimensions,
        description="Mitral valve dimensions"
    )
    regurgitation_parameters: MitralRegurgitationParameters = Field(
        default_factory=MitralRegurgitationParameters,
        alias="Regurgitation Parameters",
        description="Quantitative regurgitation parameters"
    )
    gradients: MitralStenosisGradients = Field(
        default_factory=MitralStenosisGradients,
        alias="Gradients (Mitral Stenosis Hemodynamics)",
        description="Mitral valve gradients"
    )
    morpho_functional_indices: MorphoFunctionalIndices = Field(
        default_factory=MorphoFunctionalIndices,
        alias="Morpho-Functional Indices",
        description="Quantitative morpho-functional indices"
    )
    doppler_measurements: MitralDopplerMeasurements = Field(
        default_factory=MitralDopplerMeasurements,
        alias="Doppler Measurements (Diastolic Function)",
        description="Mitral Doppler measurements related to diastolic function"
    )
    annulus_motion: AnnulusMotion = Field(
        default_factory=AnnulusMotion,
        alias="Annulus Motion",
        description="Mitral annular motion measurements"
    )

    @field_validator("area", mode="before")
    @classmethod
    def validate_area(cls, v, info):
        """If mitral valve area is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (0.5 <= val <= 6.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── Mitral Valve Root ───────────────────────────────────────────────────────────────
class MitralValve(BaseModel):
    """Top-level model for the mitral valve section of the echo report."""
    model_config = common_model_config

    assessment: MitralValveAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the mitral valve"
    )
    measurements: MitralValveMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the mitral valve"
    )




# ── Tricuspid Valve ───────────────────────────────────────────────────────────────
# ── Tricuspid Enums ─────────────────────────────────────────────────────────────
class TricuspidShapeEnum(str, Enum):
    NORMAL = "Normal"
    MALCOAPTED = "Malcoapted"
    DISPLACED_INFERIORLY = "Displaced Inferiorly"
    PROLAPTIC = "Prolaptic"
    REPAIRED = "Repaired"
    FLAIL = "Flail"
    DISPLACED = "Displaced"
    NOT_ASSESSED = "Not Assessed"


# ── Tricuspid Valve Assessment Models ─────────────────────────────────────────────
class TricuspidStenosis(BaseModel):
    """Model for tricuspid stenosis assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of Tricuspid Stenosis"
    )


class TricuspidRegurgitation(BaseModel):
    """Model for tricuspid regurgitation assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of Tricuspid Regurgitation"
    )
    paravalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        alias="Paravalvular Leak",
        description="Severity of paravalvular leak"
    )
    transvalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        alias="Transvalvular Leak",
        description="Severity of transvalvular leak"
    )


class TricuspidProsthetic(BaseModel):
    """Model for tricuspid prosthetic valve assessment."""
    model_config = common_model_config

    present: PresenceEnum = Field(
        default=PresenceEnum.NOT_ASSESSED,
        description="Presence of a tricuspid prosthetic valve"
    )
    type: ProstheticTypeEnum = Field(
        default=ProstheticTypeEnum.NOT_ASSESSED,
        description="Type of tricuspid prosthetic valve"
    )
    function: FunctionEnum = Field(
        default=FunctionEnum.NOT_ASSESSED,
        description="Function of the tricuspid prosthetic valve"
    )


# ── Full TricuspidValveAssessment Root ─────────────────────────────────────────────
class TricuspidValveAssessment(BaseModel):
    """Overall assessment of the tricuspid valve."""
    model_config = common_model_config

    shape: TricuspidShapeEnum = Field(
        default=TricuspidShapeEnum.NOT_ASSESSED,
        description="Anatomical state of the tricuspid valve"
    )
    stenosis: TricuspidStenosis = Field(
        default_factory=lambda: TricuspidStenosis(),
        description="Tricuspid stenosis assessment"
    )
    regurgitation: TricuspidRegurgitation = Field(
        default_factory=lambda: TricuspidRegurgitation(),
        description="Tricuspid regurgitation assessment"
    )
    prosthetic: TricuspidProsthetic = Field(
        default_factory=lambda: TricuspidProsthetic(),
        description="Tricuspid prosthetic valve assessment"
    )


# ── Tricuspid Valve Measurements Models ───────────────────────────────────────────────────
class TricuspidDimensions(BaseModel):
    """Quantitative measurements of tricuspid valve dimensions."""
    model_config = common_model_config

    annulus_diameter: MeasurementValue = Field(
        default="Not Measured",
        alias="Annulus Diameter",
        description="Tricuspid annulus diameter",
        unit="cm"
    )
    annulus_area: MeasurementValue = Field(
        default="Not Measured",
        alias="Annulus Area",
        description="Tricuspid annulus area",
        unit="cm²"
    )

    @field_validator("annulus_diameter", "annulus_area", mode="before")
    @classmethod
    def validate_dimensions(cls, v, info):
        """If tricuspid dimension value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "annulus_diameter" and not (2.0 <= val <= 6.0):
                return "Not Measured"
            elif field_name == "annulus_area" and not (3.0 <= val <= 20.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class TricuspidRegurgitationParameters(BaseModel):
    """Quantitative measurements related to tricuspid regurgitation."""
    model_config = common_model_config

    tr_vc: MeasurementValue = Field(
        default="Not Measured",
        alias="TR VC",
        description="Tricuspid Regurgitation Vena Contracta width",
        unit="mm"
    )
    tr_pisa_radius: MeasurementValue = Field(
        default="Not Measured",
        alias="TR PISA Radius",
        description="Tricuspid Regurgitation PISA Radius",
        unit="mm"
    )
    tr_pg: MeasurementValue = Field(
        default="Not Measured",
        alias="TR PG",
        description="Tricuspid Regurgitation Peak Gradient",
        unit="mmHg"
    )

    @field_validator("tr_vc", "tr_pisa_radius", "tr_pg", mode="before")
    @classmethod
    def validate_tr_params(cls, v, info):
        """If tricuspid regurgitation parameter value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name in ["tr_vc", "tr_pisa_radius"] and not (1.0 <= val <= 20.0):
                return "Not Measured"
            elif field_name == "tr_pg" and not (5.0 <= val <= 100.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class TricuspidGradients(BaseModel):
    """Quantitative measurements of tricuspid valve gradients."""
    model_config = common_model_config

    tv_mean_gradient: MeasurementValue = Field(
        default="Not Measured",
        alias="TV Mean Gradient",
        description="Tricuspid valve mean pressure gradient",
        unit="mmHg"
    )
    tv_pht: MeasurementValue = Field(
        default="Not Measured",
        alias="TV PHT",
        description="Tricuspid valve Pressure Half-Time",
        unit="ms"
    )

    @field_validator("tv_mean_gradient", "tv_pht", mode="before")
    @classmethod
    def validate_tv_gradients(cls, v, info):
        """If tricuspid gradient value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "tv_mean_gradient" and not (0.0 <= val <= 20.0):
                return "Not Measured"
            elif field_name == "tv_pht" and not (30.0 <= val <= 400.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class TricuspidDopplerMeasurements(BaseModel):
    """Quantitative Doppler measurements related to the tricuspid valve."""
    model_config = common_model_config

    tv_e_velocity: MeasurementValue = Field(
        default="Not Measured",
        alias="TV E Velocity",
        description="Tricuspid valve E wave velocity",
        unit="m/s"
    )
    tv_a_velocity: MeasurementValue = Field(
        default="Not Measured",
        alias="TV A Velocity",
        description="Tricuspid valve A wave velocity",
        unit="m/s"
    )
    tv_ea_ratio: MeasurementValue = Field(
        default="Not Measured",
        alias="TV E/A Ratio",
        description="Ratio of Tricuspid valve E to A wave velocity"
    )
    tv_deceleration_time: MeasurementValue = Field(
        default="Not Measured",
        alias="TV Deceleration Time",
        description="Tricuspid valve E wave deceleration time",
        unit="ms"
    )
    e_prime: MeasurementValue = Field(
        default="Not Measured",
        alias="E'",
        description="Tricuspid annular E' velocity",
        unit="cm/sec"
    )
    a_prime: MeasurementValue = Field(
        default="Not Measured",
        alias="A'",
        description="Tricuspid annular A' velocity",
        unit="cm/sec"
    )
    e_a_prime_ratio: MeasurementValue = Field(
        default="Not Measured",
        alias="E'/A' Ratio",
        description="Ratio of Tricuspid annular E' to A' velocity"
    )

    @field_validator(
        "tv_e_velocity",
        "tv_a_velocity",
        "tv_ea_ratio",
        "tv_deceleration_time",
        "e_prime",
        "a_prime",
        "e_a_prime_ratio",
        mode="before"
    )
    @classmethod
    def validate_tv_doppler(cls, v, info):
        """Validator for tricuspid Doppler measurement values."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            field_name = info.field_name
            # Example ranges - adjust based on clinical context
            if field_name in ["tv_e_velocity", "tv_a_velocity"] and not (0.1 <= val <= 2.0):
                 raise ValueError(f"{field_name} value must be between 0.1 and 2.0 m/s")
            elif field_name == "tv_ea_ratio" and not (0.5 <= val <= 3.5):
                 raise ValueError(f"{field_name} value must be between 0.5 and 3.5")
            elif field_name == "tv_deceleration_time" and not (100.0 <= val <= 400.0):
                 raise ValueError(f"{field_name} value must be between 100.0 and 400.0 ms")
            elif field_name in ["e_prime", "a_prime"] and not (2.0 <= val <= 15.0):
                 raise ValueError(f"{field_name} value must be between 2.0 and 15.0 cm/sec")
            elif field_name == "e_a_prime_ratio" and not (0.5 <= val <= 30.0):
                 raise ValueError(f"{field_name} value must be between 0.5 and 30.0")
            return val
        raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")


# ── Full Tricuspid Valve Measurements Root ─────────────────────────────────────────────────────────────
class TricuspidValveMeasurements(BaseModel):
    """Quantitative measurements related to the tricuspid valve."""
    model_config = common_model_config

    dimensions: TricuspidDimensions = Field(
        default_factory=TricuspidDimensions,
        description="Tricuspid valve dimensions"
    )
    regurgitation_parameters: TricuspidRegurgitationParameters = Field(
        default_factory=TricuspidRegurgitationParameters,
        alias="Regurgitation Parameters",
        description="Quantitative regurgitation parameters"
    )
    gradients: TricuspidGradients = Field(
        default_factory=TricuspidGradients,
        alias="Gradients (Tricuspid Valve Stenosis Hemodynamics)",
        description="Tricuspid valve gradients"
    )
    doppler_measurements: TricuspidDopplerMeasurements = Field(
        default_factory=TricuspidDopplerMeasurements,
        alias="Doppler Measurements",
        description="Tricuspid Doppler measurements"
    )


# ── Tricuspid Valve Root ───────────────────────────────────────────────────────────────
class TricuspidValve(BaseModel):
    """Top-level model for the tricuspid valve section of the echo report."""
    model_config = common_model_config

    assessment: TricuspidValveAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the tricuspid valve"
    )
    measurements: TricuspidValveMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the tricuspid valve"
    )




# ── Aortic Valve ───────────────────────────────────────────────────────────────
# ── Aortic Enums ─────────────────────────────────────────────────────────────
class AorticShapeEnum(str, Enum):
    NORMAL = "Normal"
    THICKENED = "Thickened"
    CALCIFIED = "Calcified"
    PROLAPTIC = "Prolaptic" 
    REPAIRED = "Repaired"
    FLAIL = "Flail"
    TRICUSPID = "Tricuspid"
    BICUSPID = "Bicuspid"
    NOT_ASSESSED = "Not Assessed"


# ── Aortic Valve Assessment Models ─────────────────────────────────────────────
class AorticStenosis(BaseModel):
    """Model for aortic stenosis assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of Aortic Stenosis"
    )


class AorticRegurgitation(BaseModel):
    """Model for aortic regurgitation assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of Aortic Regurgitation"
    )
    paravalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of paravalvular leak"
    )
    transvalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of transvalvular leak"
    )


class AorticProsthetic(BaseModel):
    """Model for aortic prosthetic valve assessment."""
    model_config = common_model_config

    present: PresenceEnum = Field(
        default=PresenceEnum.NOT_ASSESSED,
        description="Presence of an aortic prosthetic valve"
    )
    type: ProstheticTypeEnum = Field(
        default=ProstheticTypeEnum.NOT_ASSESSED,
        description="Type of aortic prosthetic valve"
    )
    function: FunctionEnum = Field(
        default=FunctionEnum.NOT_ASSESSED,
        description="Function of the aortic prosthetic valve"
    )

# ── Full Aortic Valve Assessment Root ─────────────────────────────────────────────
class AorticValveAssessment(BaseModel):
    """Overall assessment of the aortic valve."""
    model_config = common_model_config

    shape: AorticShapeEnum = Field(
        default=AorticShapeEnum.NOT_ASSESSED,
        description="Anatomical state of the aortic valve"
    )
    stenosis: AorticStenosis = Field(
        default_factory=lambda: AorticStenosis(),
        description="Aortic stenosis assessment"
    )
    regurgitation: AorticRegurgitation = Field(
        default_factory=lambda: AorticRegurgitation(),
        description="Aortic regurgitation assessment"
    )
    prosthetic: AorticProsthetic = Field(
        default_factory=lambda: AorticProsthetic(),
        description="Aortic prosthetic valve assessment"
    )

# ── Aortic Valve Measurements ───────────────────────────────────────────────────
class AorticRegurgitationParameters(BaseModel):
    """Quantitative measurements related to aortic regurgitation."""
    model_config = common_model_config

    ar_rv: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic Regurgitation Regurgitant Volume",
        unit="ml"
    )
    ar_roa: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic Regurgitation Regurgitant Orifice Area",
        unit="cm²"
    )
    vc: MeasurementValue = Field(
        default="Not Measured",
        description="Vena Contracta width",
        unit="mm"
    )
    ar_pht: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic Regurgitation Pressure Half-Time",
        unit="ms"
    )

    @field_validator("ar_rv", "ar_roa", "vc", "ar_pht", mode="before")
    @classmethod
    def validate_ar_params(cls, v, info):
        """If aortic regurgitation parameter value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name == "ar_rv" and not (1.0 <= val <= 100.0):
                return "Not Measured"
            elif field_name == "ar_roa" and not (0.01 <= val <= 1.0):
                return "Not Measured"
            elif field_name == "vc" and not (1.0 <= val <= 10.0):
                return "Not Measured"
            elif field_name == "ar_pht" and not (100 <= val <= 800):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class AorticStenosisGradients(BaseModel):
    """Quantitative measurements of aortic valve stenosis gradients."""
    model_config = common_model_config

    peak_velocity: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic valve peak velocity",
        unit="m/s"
    )
    lvot_peak_velocity: MeasurementValue = Field(
        default="Not Measured",
        description="Left Ventricular Outflow Tract peak velocity",
        unit="m/s"
    )
    lvot_ao_peak_velocity_ratio: MeasurementValue = Field(
        default="Not Measured",
        alias="LVOT/Ao Peak Velocity Ratio",
        description="Ratio of LVOT peak velocity to Aortic peak velocity"
    )
    pressure_recovery: MeasurementValue = Field(
        default="Not Measured",
        description="Pressure recovery",
        unit="mmHg"
    )
    aortic_ppg: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic valve peak pressure gradient",
        unit="mmHg"
    )
    aortic_mpg: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic valve mean pressure gradient",
        unit="mmHg"
    )

    @field_validator(
        "peak_velocity",
        "lvot_peak_velocity",
        "lvot_ao_peak_velocity_ratio",
        "pressure_recovery",
        "aortic_ppg",
        "aortic_mpg",
        mode="before"
    )
    @classmethod
    def validate_as_gradients(cls, v, info):
        """If aortic stenosis gradient value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            field_name = info.field_name
            if field_name in ["peak_velocity", "lvot_peak_velocity"] and not (0.5 <= val <= 6.0):
                return "Not Measured"
            elif field_name == "lvot_ao_peak_velocity_ratio" and not (0.1 <= val <= 1):
                return "Not Measured"
            elif field_name == "pressure_recovery" and not (0 <= val <= 50):
                return "Not Measured"
            elif field_name == "aortic_ppg" and not (0 <= val <= 150):
                return "Not Measured"
            elif field_name == "aortic_mpg" and not (0 <= val <= 100):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class AorticDopplerMeasurements(BaseModel):
    """Quantitative Doppler measurements related to the aortic valve/LVOT."""
    model_config = common_model_config

    # alias_generator handles "Aortic VTI", "LVOT VTI"
    aortic_vti: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic valve Velocity Time Integral",
        unit="cm"
    )
    lvot_vti: MeasurementValue = Field(
        default="Not Measured",
        description="Left Ventricular Outflow Tract Velocity Time Integral",
        unit="cm"
    )

    @field_validator("aortic_vti", "lvot_vti", mode="before")
    @classmethod
    def validate_doppler(cls, v, info):
        """If aortic Doppler measurement value is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (5.0 <= val <= 150.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── Full AorticValveMeasurements Root ─────────────────────────────────────────────
class AorticValveMeasurements(BaseModel):
    """Quantitative measurements related to the aortic valve."""
    model_config = common_model_config

    area: MeasurementValue = Field(
        default="Not Measured",
        description="Aortic Valve Area",
        unit="cm²"
    )
    regurgitation_parameters: AorticRegurgitationParameters = Field(
        default_factory=AorticRegurgitationParameters,
        description="Quantitative regurgitation parameters"
    )
    # Need explicit alias here
    gradients: AorticStenosisGradients = Field(
        default_factory=AorticStenosisGradients,
        alias="Gradients (Aortic Valve Stenosis Hemodynamics)",
        description="Aortic valve gradients"
    )
    doppler_measurements: AorticDopplerMeasurements = Field(
        default_factory=AorticDopplerMeasurements,
        description="Aortic Doppler measurements"
    )

    @field_validator("area", mode="before")
    @classmethod
    def validate_area(cls, v, info):
        """Validator for aortic valve area."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Example range (adjust based on clinical context)
            if not (0.5 <= val <= 5.0):
                 raise ValueError(f"{info.field_name} value must be between 0.5 and 5.0 cm²")
            return val
        raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")


# ── Aortic Valve Root ───────────────────────────────────────────────────────────────
class AorticValve(BaseModel):
    """Top-level model for the aortic valve section of the echo report."""
    model_config = common_model_config

    assessment: AorticValveAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the aortic valve"
    )
    measurements: AorticValveMeasurements = Field(
        ..., # This field is require
        description="Quantitative measurements for the aortic valve"
    )




# ── Pulmonary Valve ───────────────────────────────────────────────────────────────
# ── Pulmonary Enums ─────────────────────────────────────────────────────────────
class PulmonaryShapeEnum(str, Enum):
    NORMAL = "Normal"
    THICKENED = "Thickened"
    HYPOPLASTIC = "Hypoplastic"
    ATRETIC = "Atretic"
    REPAIRED = "Repaired"
    FLAIL = "Flail"
    A_REMNANT = "A Remnant"
    NOT_ASSESSED = "Not Assessed"


# ── Pulmonary Valve Assessment Models ─────────────────────────────────────────────
class PulmonaryStenosis(BaseModel):
    """Model for pulmonary stenosis assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of Pulmonary Stenosis"
    )


class PulmonaryRegurgitation(BaseModel):
    """Model for pulmonary regurgitation assessment."""
    model_config = common_model_config

    severity: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of Pulmonary Regurgitation"
    )
    paravalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of paravalvular leak"
    )
    transvalvular_leak: SeverityEnum = Field(
        default=SeverityEnum.NOT_ASSESSED,
        description="Severity of transvalvular leak"
    )


class PulmonaryProsthetic(BaseModel):
    """Model for pulmonary prosthetic valve assessment."""
    model_config = common_model_config

    present: PresenceEnum = Field(
        default=PresenceEnum.NOT_ASSESSED,
        description="Presence of a pulmonary prosthetic valve"
    )
    type: ProstheticTypeEnum = Field(
        default=ProstheticTypeEnum.NOT_ASSESSED,
        description="Type of pulmonary prosthetic valve"
    )
    function: FunctionEnum = Field(
        default=FunctionEnum.NOT_ASSESSED,
        description="Function of the pulmonary prosthetic valve"
    )


# ── Full PulmonaryValveAssessment Root ─────────────────────────────────────────────
class PulmonaryValveAssessment(BaseModel):
    """Overall assessment of the pulmonary valve."""
    model_config = common_model_config

    shape: PulmonaryShapeEnum = Field(
        default=PulmonaryShapeEnum.NOT_ASSESSED,
        description="Anatomical state of the pulmonary valve"
    )
    stenosis: PulmonaryStenosis = Field(
        default_factory=lambda: PulmonaryStenosis(),
        description="Pulmonary stenosis assessment"
    )
    regurgitation: PulmonaryRegurgitation = Field(
        default_factory=lambda: PulmonaryRegurgitation(),
        description="Pulmonary regurgitation assessment"
    )
    prosthetic: PulmonaryProsthetic = Field(
        default_factory=lambda: PulmonaryProsthetic(),
        description="Pulmonary prosthetic valve assessment"
    )


# ── Pulmonary Valve Measurements ───────────────────────────────────────────────────
class PulmonaryDimensions(BaseModel):
    """Quantitative measurements of pulmonary artery dimensions."""
    model_config = common_model_config

    pa_annulus: MeasurementValue = Field(
        default="Not Measured",
        description="Measurement of the pulmonary artery annulus",
        unit="cm"
    )
    main_pa: MeasurementValue = Field(
        default="Not Measured",
        description="Measurement of the main pulmonary artery",
        unit="cm"
    )
    lpa_diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Diameter of the left pulmonary artery",
        unit="cm"
    )
    rpa_diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Diameter of the right pulmonary artery",
        unit="cm"
    )

    # Consolidate validation logic similar to Pericardium
    @field_validator("pa_annulus", "main_pa", "lpa_diameter", "rpa_diameter", mode="before")
    @classmethod
    def validate_dimensions(cls, v, info):
        """Validator for pulmonary dimension values."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            if info.field_name == "pa_annulus" and not (0.5 <= val <= 4.0):
                 raise ValueError(f"{info.field_name} value must be between 0.5 and 4.0 cm")
            elif info.field_name == "main_pa" and not (0.5 <= val <= 5.0):
                 raise ValueError(f"{info.field_name} value must be between 0.5 and 5.0 cm")
            elif info.field_name in ["lpa_diameter", "rpa_diameter"] and not (0.2 <= val <= 3.0):
                 raise ValueError(f"{info.field_name} value must be between 0.2 and 3.0 cm")
            return val
        raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")


class PulmonaryRegurgitationParameters(BaseModel):
    """Quantitative measurements related to pulmonary regurgitation."""
    model_config = common_model_config

    pr_pht: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary regurgitation pressure half-time",
        unit="ms"
    )

    @field_validator("pr_pht", mode="before")
    @classmethod
    def validate_pht(cls, v):
        """Validator for PR PHT measurement."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError("PR PHT value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            if not (50 <= val <= 800):
                 raise ValueError("PR PHT value must be between 50 and 800 ms")
            return val
        raise ValueError("PR PHT value must be a number or 'Not Measured'")


class PulmonaryGradients(BaseModel):
    """Quantitative measurements of pulmonary valve gradients."""
    model_config = common_model_config

    pv_peak_velocity: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary valve peak velocity",
        unit="m/s"
    )
    pv_ppg: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary valve peak pressure gradient",
        unit="mmHg"
    )
    pv_mpg: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary valve mean pressure gradient",
        unit="mmHg"
    )

    @field_validator("pv_peak_velocity", "pv_ppg", "pv_mpg", mode="before")
    @classmethod
    def validate_gradients(cls, v, info):
        """Validator for pulmonary gradient values."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if info.field_name == "pv_peak_velocity" and not (0.5 <= val <= 8.0):
                return "Not Measured"
            elif info.field_name == "pv_ppg" and not (0 <= val <= 120.0):
                return "Not Measured"
            elif info.field_name == "pv_mpg" and not (0 <= val <= 80.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class PulmonaryDopplerMeasurements(BaseModel):
    """Quantitative Doppler measurements related to the pulmonary valve/RVOT."""
    model_config = common_model_config

    # Use snake_case, alias_generator handles "PV VTI", "RVOT VTI", etc.
    pv_vti: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary valve Velocity Time Integral",
        unit="cm"
    )
    rvot_vti: MeasurementValue = Field(
        default="Not Measured",
        description="Right Ventricular Outflow Tract Velocity Time Integral",
        unit="cm"
    )
    pulmonary_acc_time: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary acceleration time",
        unit="ms"
    )

    @field_validator("pv_vti", "rvot_vti", "pulmonary_acc_time", mode="before")
    @classmethod
    def validate_doppler(cls, v, info):
        """Validator for pulmonary Doppler measurement values."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Example range (adjust based on clinical context)
            if info.field_name in ["pv_vti", "rvot_vti"] and not (5.0 <= val <= 30.0):
                 raise ValueError(f"{info.field_name} value must be between 5.0 and 30.0 cm")
            elif info.field_name == "pulmonary_acc_time" and not (30 <= val <= 200):
                 raise ValueError(f"{info.field_name} value must be between 30 and 200 ms")
            return val
        raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")


class PulmonaryHemodynamicPressures(BaseModel):
    """Estimated hemodynamic pressures related to the pulmonary circulation."""
    model_config = common_model_config

    mean_pap: MeasurementValue = Field(
        default="Not Measured",
        description="Estimated mean pulmonary artery pressure",
        unit="mmHg"
    )
    ra_pressure: MeasurementValue = Field(
        default="Not Measured",
        description="Estimated right atrial pressure",
        unit="mmHg"
    )
    # RVSP and PAP are already snake_case
    rvsp: MeasurementValue = Field(
        default="Not Measured",
        description="Estimated right ventricular systolic pressure",
        unit="mmHg"
    )
    pap: MeasurementValue = Field(
        default="Not Measured",
        description="Estimated pulmonary artery pressure",
        unit="mmHg"
    )

    @field_validator("mean_pap", "ra_pressure", "rvsp", "pap", mode="before")
    @classmethod
    def validate_pressures(cls, v, info):
        """Validator for pulmonary pressure values."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
             try:
                 v = float(v)
             except ValueError:
                 raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            if info.field_name == "mean_pap" and not (5 <= val <= 70):
                 raise ValueError(f"{info.field_name} value must be between 5 and 70 mmHg")
            elif info.field_name == "ra_pressure" and not (0 <= val <= 20):
                 raise ValueError(f"{info.field_name} value must be between 0 and 20 mmHg")
            elif info.field_name in ["rvsp", "pap"] and not (10 <= val <= 120):
                 raise ValueError(f"{info.field_name} value must be between 10 and 120 mmHg")
            return val
        raise ValueError(f"{info.field_name} value must be a number or 'Not Measured'")


# ── Full PulmonaryValveMeasurements Root ─────────────────────────────────────────────
class PulmonaryValveMeasurements(BaseModel):
    """Quantitative measurements related to the pulmonary valve."""
    model_config = common_model_config

    dimensions: PulmonaryDimensions = Field(
        default_factory=PulmonaryDimensions, 
        description="Pulmonary artery dimensions"
    )
    regurgitation_parameters: PulmonaryRegurgitationParameters = Field(
        default_factory=PulmonaryRegurgitationParameters, 
        description="Quantitative regurgitation parameters"
    )
    gradients: PulmonaryGradients = Field(
        default_factory=PulmonaryGradients, 
        alias="Gradients (Pulmonary Valve Stenosis Hemodynamics)", 
        description="Pulmonary valve gradients"
    )
    doppler_measurements: PulmonaryDopplerMeasurements = Field(
        default_factory=PulmonaryDopplerMeasurements, 
        description="Pulmonary Doppler measurements"
    )
    hemodynamic_pressures: PulmonaryHemodynamicPressures = Field(
        default_factory=PulmonaryHemodynamicPressures,
        description="Estimated hemodynamic pressures"
    )


# ── Pulmonary Valve Root ───────────────────────────────────────────────────────────────
class PulmonaryValve(BaseModel):
    """Top-level model for the pulmonary valve section of the echo report."""
    model_config = common_model_config

    # Use lowercase field names to match Pericardium root
    assessment: PulmonaryValveAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the pulmonary valve"
    )
    measurements: PulmonaryValveMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the pulmonary valve"
    )


















# ── Aorta ───────────────────────────────────────────────────────────────
# ── Aorta Enums ───────────────────────────────────────────────────────────────
class AortaMorphologySegmentEnum(str, Enum):
    """Enumeration for aortic segments assessed for morphology."""
    ASCENDING_AORTA = "Ascending Aorta"
    AORTIC_ARCH = "Aortic Arch"
    DESCENDING_AORTA = "Descending Aorta"
    NOT_ASSESSED = "Not Assessed" # Added for consistency, though not in JSON enum


class AortaMorphologyEnum(str, Enum):
    """Enumeration for aortic morphology."""
    NORMAL = "Normal"
    DILATED = "Dilated"
    REPLACED_BY_TUBE_GRAFT = "Replaced by Tube Graft"
    ANEURYSMAL = "Aneurysmal"
    NOT_ASSESSED = "Not Assessed"


class AortaFlowSegmentEnum(str, Enum):
    """Enumeration for aortic segments assessed for flow."""
    THORACIC_DESCENDING_AORTA = "Thoracic Descending Aorta"
    ABDOMINAL_AORTA = "Abdominal Aorta"
    NOT_ASSESSED = "Not Assessed" # Added for consistency, though not in JSON enum


class AortaFlowPatternEnum(str, Enum):
    """Enumeration for aortic flow patterns."""
    NORMAL = "Normal"
    HOLO_DIASTOLIC_REVERSAL = "Holo Diastolic Reversal"
    EARLY_DIASTOLIC_REVERSAL = "Early Diastolic Reversal"
    HOLO_ANTEGRADE_DIASTOLIC = "Holo Antegrade Diastolic"
    EARLY_ANTEGRADE_DIASTOLIC = "Early Antegrade Diastolic"
    NOT_ASSESSED = "Not Assessed"


class AtheroscleroticChangesEnum(str, Enum):
    """Enumeration for presence of atherosclerotic changes."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"


class RightSidedAorticArchEnum(str, Enum):
    """Enumeration for right-sided aortic arch variant."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"


class AortaMeasurementSegmentEnum(str, Enum):
    """Enumeration for aortic segments where dimensions are measured."""
    AORTIC_ANNULUS = "Aortic Annulus"
    SINUSES_OF_VALSALVA = "Sinuses of Valsalva (SOV)"
    SINOTUBULAR_JUNCTION = "Sinotubular Junction (STJ)"
    ASCENDING_AORTA = "Ascending Aorta"
    AORTIC_ARCH = "Aortic Arch"
    DESCENDING_AORTA = "Descending Aorta"
    ABDOMINAL_AORTA = "Abdominal Aorta"
    NOT_MEASURED = "Not Measured" 


# ── Aorta Assessment Models ─────────────────────────────────────────────────────────────────────
class AortaSegmentMorphology(BaseModel):
    """Model for morphology assessment of a specific aortic segment."""
    model_config = common_model_config

    segment: AortaMorphologySegmentEnum = Field(
        default=AortaMorphologySegmentEnum.NOT_ASSESSED,
        description="Segment of the thoracic aorta"
    )
    morphology: AortaMorphologyEnum = Field(
        default=AortaMorphologyEnum.NOT_ASSESSED,
        description="Morphological state of the specified segment"
    )

class AortaSegmentFlow(BaseModel):
    """Model for flow assessment of a specific aortic segment."""
    model_config = common_model_config

    segment: AortaFlowSegmentEnum = Field(
        default=AortaFlowSegmentEnum.NOT_ASSESSED,
        description="Aortic segment in which flow is assessed"
    )
    pattern: AortaFlowPatternEnum = Field(
        default=AortaFlowPatternEnum.NOT_ASSESSED,
        description="Flow pattern in the specified aortic segment"
    )


class AortaAssessment(BaseModel):
    """Overall assessment of the aorta."""
    model_config = common_model_config

    morphology: List[AortaSegmentMorphology] = Field(
        default_factory=list, # Use default_factory for mutable defaults
        description="Morphology assessment for different aortic segments"
    )
    flow: List[AortaSegmentFlow] = Field(
        default_factory=list, # Use default_factory for mutable defaults
        description="Flow assessment for different aortic segments"
    )
    atherosclerotic_changes: AtheroscleroticChangesEnum = Field(
        default=AtheroscleroticChangesEnum.NOT_ASSESSED,
        description="Presence of atherosclerotic changes"
    )
    right_sided_aortic_arch: RightSidedAorticArchEnum = Field(
        default=RightSidedAorticArchEnum.NOT_ASSESSED,
        description="Right-sided aortic arch anatomical variant"
    )

# ── Aorta Measurement Models ─────────────────────────────────────────────────────────────────────
class AortaSegmentDimension(BaseModel):
    """Model for quantitative dimension measurement of a specific aortic segment."""
    model_config = common_model_config

    segment: AortaMeasurementSegmentEnum = Field(
        default=AortaMeasurementSegmentEnum.NOT_MEASURED,
        description="Anatomical segment where diameter is measured"
    )
    diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Measured diameter of the segment",
        unit="cm"
    )

    @field_validator("diameter", mode="before")
    @classmethod
    def validate_diameter(cls, v):
        """Validator for aortic segment diameter measurement."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Diameter value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema
            if not (0.5 <= val <= 6.0):
                raise ValueError("Value must be between 0.5 and 6.0 cm")
            return val
        raise ValueError("Diameter value must be a number or 'Not Measured'")


class AortaDistances(BaseModel):
    """Model for distance measurements related to the aortic root."""
    model_config = common_model_config

    annulus_to_stj: MeasurementValue = Field(
        default="Not Measured", 
        description="Distance from aortic annulus to sinotubular junction",
        unit="cm"
    )

    @field_validator("annulus_to_stj", mode="before")
    @classmethod
    def validate_annulus_to_stj(cls, v):
        """Validator for Annulus to STJ distance measurement."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Annulus to STJ distance must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema
            if not (0.5 <= val <= 3.0):
                raise ValueError("Value must be between 0.5 and 3.0 cm")
            return val
        raise ValueError("Annulus to STJ distance must be a number or 'Not Measured'")


class AortaMeasurements(BaseModel):
    """Quantitative measurements related to the aorta."""
    model_config = common_model_config

    dimensions: List[AortaSegmentDimension] = Field(
        default_factory=list, # Use default_factory for mutable defaults
        description="Quantitative dimensions for different aortic segments"
    )
    distances: AortaDistances = Field(
         default_factory=AortaDistances, # Use default_factory for mutable defaults
         description="Quantitative distance measurements for the aortic root"
    )


# ── Aorta Root ───────────────────────────────────────────────────────────────
class Aorta(BaseModel):
    """Top-level model for the aorta section of the echo report."""
    model_config = common_model_config

    assessment: AortaAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the aorta"
    )
    measurements: AortaMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the aorta"
    )








# ── Pulmonic Vein ───────────────────────────────────────────────────────────────
# ── Pulmonic Vein Enums ───────────────────────────────────────────────────────────────
class PulmonicVeinVenousDrainageEnum(str, Enum):
    """Enumeration for pulmonary venous drainage pattern."""
    NORMAL = "Normal"
    ABNORMAL = "Abnormal"
    NOT_ASSESSED = "Not Assessed"

class PulmonicVeinInflowPatternEnum(str, Enum):
    """Enumeration for pulmonary vein inflow pattern based on Doppler."""
    S_GREATER_THAN_D = "S > D"
    S_EQUALS_D = "S = D"
    S_LESS_THAN_D = "S < D"
    BLUNTED_S_WAVE = "Blunted S Wave"
    SYSTOLIC_FLOW_REVERSAL = "Systolic Flow Reversal"
    NOT_ASSESSED = "Not Assessed"

# ── Pulmonic Vein Assessment Models ───────────────────────────────────────────────
class PulmonicVeinAssessment(BaseModel):
    """Overall assessment of the pulmonic veins."""
    model_config = common_model_config

    venous_drainage: PulmonicVeinVenousDrainageEnum = Field(
        default=PulmonicVeinVenousDrainageEnum.NOT_ASSESSED,
        description="Pattern of pulmonary venous drainage into the left atrium"
    )
    inflow_pattern: PulmonicVeinInflowPatternEnum = Field(
        default=PulmonicVeinInflowPatternEnum.NOT_ASSESSED,
        description="Pulmonary vein flow pattern based on spectral Doppler (S and D wave relationship)"
    )

# ── Pulmonic Vein Measurement Models ───────────────────────────────────────────────
class PulmonicVeinDopplerMeasurements(BaseModel):
    """Quantitative Doppler measurements for pulmonic veins."""
    model_config = common_model_config

    peak_s_velocity: MeasurementValue = Field(
        default="Not Measured",
        description="Peak systolic (S wave) flow velocity",
        unit="cm/sec"
    )
    peak_d_velocity: MeasurementValue = Field(
        default="Not Measured",
        description="Peak diastolic (D wave) flow velocity",
        unit="cm/sec"
    )
    peak_ar_velocity: MeasurementValue = Field(
        default="Not Measured",
        description="Peak Atrial Reversal (AR wave) velocity",
        unit="cm/sec"
    )

    @field_validator("peak_s_velocity", "peak_d_velocity", "peak_ar_velocity", mode="before")
    @classmethod
    def validate_velocity(cls, v):
        """If pulmonary vein velocity measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if ("peak_s_velocity" in cls.__annotations__ and not (10 <= val <= 150)) or \
               ("peak_d_velocity" in cls.__annotations__ and not (10 <= val <= 150)) or \
               ("peak_ar_velocity" in cls.__annotations__ and not (5 <= val <= 100)):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


class PulmonicVeinMeasurements(BaseModel):
    """Quantitative measurements related to the pulmonic veins."""
    model_config = common_model_config

    doppler_measurements: PulmonicVeinDopplerMeasurements = Field(
        default_factory=PulmonicVeinDopplerMeasurements,
        description="Quantitative Doppler measurements for pulmonic veins"
    )
    ar_duration: MeasurementValue = Field(
        default="Not Measured",
        description="Duration of atrial reversal wave (AR) in milliseconds",
        unit="ms"
    )

    @field_validator("ar_duration", mode="before")
    @classmethod
    def validate_ar_duration(cls, v):
        """If AR duration measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (10 <= val <= 300):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── Pulmonic Vein Root ───────────────────────────────────────────────────────────────
class PulmonicVein(BaseModel):
    """Top-level model for the pulmonic vein section of the echo report."""
    model_config = common_model_config

    assessment: PulmonicVeinAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the pulmonic veins"
    )
    measurements: PulmonicVeinMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the pulmonic veins"
    )






# ── IVC ───────────────────────────────────────────────────────────────
# ── IVC Enums ───────────────────────────────────────────────────────────────
class IVCSizeEnum(str, Enum):
    """Enumeration for Inferior Vena Cava size assessment."""
    NORMAL = "Normal"
    SMALL = "Small"
    DILATED = "Dilated"
    PLETHORIC = "Plethoric"
    NOT_ASSESSED = "Not Assessed"

class IVCRespiratoryVariationEnum(str, Enum):
    """Enumeration for IVC respiratory variation assessment."""
    GREATER_THAN_50 = ">50%"
    LESS_THAN_50 = "<50%"
    GREATER_THAN_30 = ">30%" # Added based on common practice, though not in JSON enum
    LESS_THAN_30 = "<30%"   # Added based on common practice, though not in JSON enum
    ABSENT = "Absent"
    NOT_ASSESSED = "Not Assessed"

class IVCPlethoraEnum(str, Enum):
    """Enumeration for visual assessment of IVC plethora."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class IVCSniffTestResultEnum(str, Enum):
    """Enumeration for the result of the IVC sniff test."""
    NORMAL_COLLAPSE = "Normal Collapse"
    REDUCED_COLLAPSE = "Reduced Collapse"
    NO_COLLAPSE = "No Collapse"
    NOT_PERFORMED = "Not Performed"
    NOT_ASSESSED = "Not Assessed"

# ── IVC Assessment Models ───────────────────────────────────────────────
class IVCAssessment(BaseModel):
    """Overall assessment of the IVC."""
    model_config = common_model_config

    size: IVCSizeEnum = Field(
        default=IVCSizeEnum.NOT_ASSESSED,
        description="Inferior Vena Cava size based on diameter and collapsibility"
    )
    respiratory_variation: IVCRespiratoryVariationEnum = Field(
        default=IVCRespiratoryVariationEnum.NOT_ASSESSED,
        description="Collapsibility index with respiratory effort"
    )
    ivc_plethora: IVCPlethoraEnum = Field(
        default=IVCPlethoraEnum.NOT_ASSESSED,
        description="Visual assessment of IVC plethora (lack of inspiratory collapse)"
    )
    sniff_test_result: IVCSniffTestResultEnum = Field(
        default=IVCSniffTestResultEnum.NOT_ASSESSED,
        description="Visual result of IVC collapse with a sniff maneuver"
    )

# ── IVC Measurement Models ───────────────────────────────────────────────
class IVCMeasurements(BaseModel):
    """Quantitative measurements related to the IVC."""
    model_config = common_model_config

    diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Inferior Vena Cava maximal diameter (end-expiration)",
        unit="cm"
    )
    collapsibility_index: MeasurementValue = Field(
        default="Not Measured",
        description="Percent reduction in IVC diameter during inspiration",
        unit="%"
    )

    @field_validator("diameter", mode="before")
    @classmethod
    def validate_diameter(cls, v):
        """If IVC diameter measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (0.5 <= val <= 4.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"

    @field_validator("collapsibility_index", mode="before")
    @classmethod
    def validate_collapsibility_index(cls, v):
        """If IVC collapsibility index measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (0 <= val <= 100):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── IVC Root ───────────────────────────────────────────────────────────────
class IVC(BaseModel):
    """Top-level model for the IVC section of the echo report."""
    model_config = common_model_config

    assessment: IVCAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the IVC"
    )
    measurements: IVCMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the IVC"
    )








# ── VSD Enums ─────────────────────────────────────────────────────────────────
class VSDPresenceEnum(str, Enum):
    """Enumeration for VSD presence assessment."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class VSDLocationEnum(str, Enum):
    """Enumeration for VSD anatomical location."""
    PERIMEMBRANOUS = "Perimembranous"
    MUSCULAR = "Muscular"
    INLET = "Inlet"
    OUTLET = "Outlet"
    SUBPULMONARY = "Subpulmonary"
    MULTIPLE = "Multiple"
    NOT_ASSESSED = "Not Assessed"

class VSDSizeEnum(str, Enum):
    """Enumeration for VSD size estimation."""
    SMALL = "Small"
    MODERATE = "Moderate"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class VSDShuntDirectionEnum(str, Enum):
    """Enumeration for VSD shunt direction."""
    LEFT_TO_RIGHT = "Left to Right"
    RIGHT_TO_LEFT = "Right to Left"
    BIDIRECTIONAL = "Bidirectional"
    NOT_ASSESSED = "Not Assessed"

class VSDAneurysmalTissueEnum(str, Enum):
    """Enumeration for presence of aneurysmal tissue with VSD."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class VSDAssociatedDefectsEnum(str, Enum):
    """Enumeration for associated structural cardiac anomalies with VSD."""
    NONE = "None"
    AV_CANAL = "AV Canal"
    TETRALOGY_OF_FALLOT = "Tetralogy of Fallot"
    AORTIC_VALVE_PROLAPSE = "Aortic Valve Prolapse"
    SUBAORTIC_STENOSIS = "Subaortic Stenosis"
    OTHER = "Other"
    NOT_ASSESSED = "Not Assessed"

# ── VSD Assessment Models ─────────────────────────────────────────────────────
class VSDAssessment(BaseModel):
    """Model for VSD assessment details."""
    model_config = common_model_config

    present: VSDPresenceEnum = Field(
        default=VSDPresenceEnum.NOT_ASSESSED,
        description="Presence of VSD"
    )
    location: VSDLocationEnum = Field(
        default=VSDLocationEnum.NOT_ASSESSED,
        description="Anatomical location of the VSD"
    )
    size: VSDSizeEnum = Field(
        default=VSDSizeEnum.NOT_ASSESSED,
        description="Visual/quantitative size estimation of the VSD"
    )
    shunt_direction: VSDShuntDirectionEnum = Field(
        default=VSDShuntDirectionEnum.NOT_ASSESSED,
        description="Direction of shunting across the VSD"
    )
    aneurysmal_tissue: VSDAneurysmalTissueEnum = Field(
        default=VSDAneurysmalTissueEnum.NOT_ASSESSED,
        description="Presence of aneurysmal tissue surrounding the defect"
    )
    associated_defects: VSDAssociatedDefectsEnum = Field(
        default=VSDAssociatedDefectsEnum.NOT_ASSESSED,
        description="Associated structural cardiac anomalies"
    )

# ── VSD Measurement Models ─────────────────────────────────────────────────────
class VSDMeasurements(BaseModel):
    """Quantitative measurements related to the VSD."""
    model_config = common_model_config

    diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Diameter of the VSD as measured by imaging",
        unit="mm"
    )
    peak_gradient: MeasurementValue = Field(
        default="Not Measured",
        description="Peak systolic gradient across the VSD",
        unit="mmHg"
    )
    qp_qs: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary to Systemic Flow Ratio"
    )

    @field_validator("diameter", mode="before")
    @classmethod
    def validate_diameter(cls, v):
        """If VSD diameter measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Diameter value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema: minimum 1, maximum 20
            if not (1.0 <= val <= 20.0):
                raise ValueError("Diameter value must be between 1.0 and 20.0 mm")
            return val
        raise ValueError("Diameter value must be a number or 'Not Measured'")

    @field_validator("peak_gradient", mode="before")
    @classmethod
    def validate_peak_gradient(cls, v):
        """If VSD peak gradient measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Peak gradient value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema: minimum 5, maximum 120
            if not (5.0 <= val <= 120.0):
                raise ValueError("Peak gradient value must be between 5.0 and 120.0 mmHg")
            return val
        raise ValueError("Peak gradient value must be a number or 'Not Measured'")

    @field_validator("qp_qs", mode="before")
    @classmethod
    def validate_qp_qs(cls, v):
        """If VSD Qp/Qs ratio measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Qp/Qs value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema: minimum 0.5, maximum 5.0
            if not (0.5 <= val <= 5.0):
                raise ValueError("Qp/Qs value must be between 0.5 and 5.0")
            return val
        raise ValueError("Qp/Qs value must be a number or 'Not Measured'")


# ── VSD Root ─────────────────────────────────────────────────────────────────
class VSD(BaseModel):
    """Top-level model for the VSD section of the echo report."""
    model_config = common_model_config

    assessment: VSDAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the VSD"
    )
    measurements: VSDMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the VSD"
    )






# ── ASD Enums ─────────────────────────────────────────────────────────────────
class ASDPresenceEnum(str, Enum):
    """Enumeration for ASD presence assessment."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class ASDTypeEnum(str, Enum):
    """Enumeration for ASD anatomical classification."""
    SECUNDUM = "Secundum"
    PRIMUM = "Primum"
    SINUS_VENOSUS = "Sinus Venosus"
    CORONARY_SINUS = "Coronary Sinus"
    MULTIPLE = "Multiple"
    NOT_ASSESSED = "Not Assessed"

class ASDSizeEnum(str, Enum):
    """Enumeration for ASD size estimation."""
    SMALL = "Small"
    MODERATE = "Moderate"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class ASDShuntDirectionEnum(str, Enum):
    """Enumeration for ASD shunt direction."""
    LEFT_TO_RIGHT = "Left to Right"
    RIGHT_TO_LEFT = "Right to Left"
    BIDIRECTIONAL = "Bidirectional"
    NOT_ASSESSED = "Not Assessed"

class ASDSeptalAneurysmEnum(str, Enum):
    """Enumeration for presence of septal aneurysm with ASD."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class ASDAssociatedDefectsEnum(str, Enum):
    """Enumeration for associated structural cardiac anomalies with ASD."""
    NONE = "None"
    AV_CANAL = "AV Canal"
    PARTIAL_ANOMALOUS_PULMONARY_VENOUS_RETURN = "Partial Anomalous Pulmonary Venous Return"
    OTHER = "Other"
    NOT_ASSESSED = "Not Assessed"

# ── ASD Assessment Models ─────────────────────────────────────────────────────
class ASDAssessment(BaseModel):
    """Model for ASD assessment details."""
    model_config = common_model_config

    present: ASDPresenceEnum = Field(
        default=ASDPresenceEnum.NOT_ASSESSED,
        description="Presence of ASD"
    )
    type: ASDTypeEnum = Field(
        default=ASDTypeEnum.NOT_ASSESSED,
        description="Anatomical classification of the ASD"
    )
    size: ASDSizeEnum = Field(
        default=ASDSizeEnum.NOT_ASSESSED,
        description="Visual/quantitative estimation of the defect size"
    )
    shunt_direction: ASDShuntDirectionEnum = Field(
        default=ASDShuntDirectionEnum.NOT_ASSESSED,
        description="Direction of shunting across the ASD"
    )
    septal_aneurysm: ASDSeptalAneurysmEnum = Field(
        default=ASDSeptalAneurysmEnum.NOT_ASSESSED,
        description="Presence of aneurysmal movement of the interatrial septum"
    )
    associated_defects: ASDAssociatedDefectsEnum = Field(
        default=ASDAssociatedDefectsEnum.NOT_ASSESSED,
        description="Associated structural cardiac anomalies"
    )

# ── ASD Measurement Models ─────────────────────────────────────────────────────
class ASDMeasurements(BaseModel):
    """Quantitative measurements related to the ASD."""
    model_config = common_model_config

    diameter: MeasurementValue = Field(
        default="Not Measured",
        description="Measured maximum diameter of the ASD",
        unit="mm"
    )
    peak_gradient: MeasurementValue = Field(
        default="Not Measured",
        description="Peak pressure gradient across the ASD",
        unit="mmHg"
    )
    qp_qs: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary to systemic flow ratio"
    )

    @field_validator("diameter", mode="before")
    @classmethod
    def validate_diameter(cls, v):
        """Validator for ASD diameter measurement."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Diameter value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema: minimum 1, maximum 40
            if not (1.0 <= val <= 40.0):
                raise ValueError("Diameter value must be between 1.0 and 40.0 mm")
            return val
        raise ValueError("Diameter value must be a number or 'Not Measured'")

    @field_validator("peak_gradient", mode="before")
    @classmethod
    def validate_peak_gradient(cls, v):
        """Validator for ASD peak gradient measurement."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Peak gradient value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema: minimum 1, maximum 50
            if not (1.0 <= val <= 50.0):
                raise ValueError("Peak gradient value must be between 1.0 and 50.0 mmHg")
            return val
        raise ValueError("Peak gradient value must be a number or 'Not Measured'")

    @field_validator("qp_qs", mode="before")
    @classmethod
    def validate_qp_qs(cls, v):
        """Validator for Qp/Qs ratio measurement."""
        if v == "Not Measured":
            return v
        if isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                raise ValueError("Qp/Qs value must be a number or 'Not Measured'")

        if isinstance(v, (int, float)):
            val = float(v)
            # Range based on JSON schema: minimum 0.5, maximum 5.0
            if not (0.5 <= val <= 5.0):
                raise ValueError("Qp/Qs value must be between 0.5 and 5.0")
            return val
        raise ValueError("Qp/Qs value must be a number or 'Not Measured'")


# ── ASD Root ─────────────────────────────────────────────────────────────────
class ASD(BaseModel):
    """Top-level model for the ASD section of the echo report."""
    model_config = common_model_config

    assessment: ASDAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the ASD"
    )
    measurements: ASDMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the ASD"
    )






# ── PFO Enums ─────────────────────────────────────────────────────────────────
class PFOPresenceEnum(str, Enum):
    """Enumeration for PFO presence assessment."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class PFOSizeEnum(str, Enum):
    """Enumeration for PFO size estimation."""
    SMALL = "Small"
    MODERATE = "Moderate"
    LARGE = "Large"
    NOT_ASSESSED = "Not Assessed"

class PFOShuntDirectionEnum(str, Enum):
    """Enumeration for PFO shunt direction."""
    LEFT_TO_RIGHT = "Left to Right"
    RIGHT_TO_LEFT = "Right to Left"
    BIDIRECTIONAL = "Bidirectional"
    NOT_ASSESSED = "Not Assessed"

class PFOAssociatedAneurysmEnum(str, Enum):
    """Enumeration for presence of associated atrial septal aneurysm with PFO."""
    YES = "Yes"
    NO = "No"
    NOT_ASSESSED = "Not Assessed"

class PFOBubbleStudyEnum(str, Enum):
    """Enumeration for bubble study results for PFO."""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NOT_PERFORMED = "Not Performed"
    NOT_ASSESSED = "Not Assessed"

class PFOAssociatedDefectsEnum(str, Enum):
    """Enumeration for other structural anomalies associated with PFO."""
    NONE = "None"
    ASD = "ASD"
    ANEURYSMAL_SEPTUM = "Aneurysmal Septum"
    CHIARI_NETWORK = "Chiari Network"
    OTHER = "Other"
    NOT_ASSESSED = "Not Assessed"

# ── PFO Assessment Models ─────────────────────────────────────────────────────
class PFOAssessment(BaseModel):
    """Model for PFO assessment details."""
    model_config = common_model_config

    present: PFOPresenceEnum = Field(
        default=PFOPresenceEnum.NOT_ASSESSED,
        description="Presence of PFO"
    )
    size: PFOSizeEnum = Field(
        default=PFOSizeEnum.NOT_ASSESSED,
        description="Visual/quantitative estimation of PFO size"
    )
    shunt_direction: PFOShuntDirectionEnum = Field(
        default=PFOShuntDirectionEnum.NOT_ASSESSED,
        description="Direction of shunting through the PFO, may depend on provocative maneuvers"
    )
    associated_aneurysm: PFOAssociatedAneurysmEnum = Field(
        default=PFOAssociatedAneurysmEnum.NOT_ASSESSED,
        description="Presence of atrial septal aneurysm (ASA) associated with the PFO"
    )
    bubble_study: PFOBubbleStudyEnum = Field(
        default=PFOBubbleStudyEnum.NOT_ASSESSED,
        description="Result of contrast bubble test used to detect right-to-left shunt"
    )
    associated_defects: PFOAssociatedDefectsEnum = Field(
        default=PFOAssociatedDefectsEnum.NOT_ASSESSED,
        description="Other structural anomalies associated with PFO"
    )

# ── PFO Measurement Models ─────────────────────────────────────────────────────
class PFOMeasurements(BaseModel):
    """Quantitative measurements related to the PFO."""
    model_config = common_model_config

    tunnel_length: MeasurementValue = Field(
        default="Not Measured",
        description="Length of the PFO tunnel measured in millimeters",
        unit="mm"
    )
    qp_qs: MeasurementValue = Field(
        default="Not Measured",
        description="Pulmonary to systemic flow ratio"
    )

    @field_validator("tunnel_length", mode="before")
    @classmethod
    def validate_tunnel_length(cls, v):
        """If PFO tunnel length measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (1.0 <= val <= 20.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"

    @field_validator("qp_qs", mode="before")
    @classmethod
    def validate_qp_qs(cls, v):
        """If PFO Qp/Qs ratio measurement is invalid, only default that field."""
        if v == "Not Measured":
            return v
        try:
            val = float(v)
            if not (0.5 <= val <= 5.0):
                return "Not Measured"
            return val
        except Exception:
            return "Not Measured"


# ── PFO Root ─────────────────────────────────────────────────────────────────
class PFO(BaseModel):
    """Top-level model for the PFO section of the echo report."""
    model_config = common_model_config

    assessment: PFOAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the PFO"
    )
    measurements: PFOMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the PFO"
    )

















class CardiacChambers(BaseModel):
    model_config = common_model_config

    Left_Ventricle: LeftVentricle = Field(..., description="Left Ventricle assessments and measurements")
    Right_Ventricle: RightVentricle = Field(..., description="Right Ventricle assessments and measurements")
    Left_Atrium: LeftAtrium = Field(..., description="Left Atrium assessments and measurements")
    Right_Atrium: RightAtrium = Field(..., description="Right Atrium assessments and measurements")


class ValvularApparatus(BaseModel):
    model_config = common_model_config

    Mitral_Valve: MitralValve = Field(..., description="Mitral valve assessments and measurements")
    Aortic_Valve: AorticValve = Field(..., description="Aortic valve assessments and measurements")
    Pulmonary_Valve: PulmonaryValve = Field(..., description="Pulmonary valve assessments and measurements")
    Tricuspid_Valve: TricuspidValve = Field(..., description="Tricuspid valve assessments and measurements")

class GreatVesselsAndVenousReturn(BaseModel):
    model_config = common_model_config

    aorta: Aorta = Field(..., description="Aorta assessments and measurements")
    pulmonic_vein: PulmonicVein = Field(..., description="Pulmonic Vein assessments and measurements")
    ivc: IVC = Field(..., description="Inferior Vena Cava assessments and measurements")

class CongenitalAndStructuralDefects(BaseModel):
    model_config = common_model_config

    vsd:VSD = Field(..., description="Ventricular Septal Defect Assessments and Measurements")
    asd:ASD = Field(..., description="Atrial Septal Defect Assessments and Measurements")
    pfo:PFO = Field(..., description="Patent Foramen Ovale Assessments and Measurements")

class Pericardium(BaseModel):
    """Top-level model for the pericardium section of the echo report."""
    model_config = common_model_config

    assessment: PericardiumAssessment = Field(
        ..., # This field is required
        description="Assessment findings for the pericardium"
    )
    measurements: PericardiumMeasurements = Field(
        ..., # This field is required
        description="Quantitative measurements for the pericardium"
    )


class EchoReport(BaseModel):
    """Root model representing the extracted echo report data."""
    model_config = common_model_config

    Cardiac_Chambers: CardiacChambers = Field(..., description="Details of each cardiac chambers inluding left ventricle, left atrium, right ventricle, and right atrium")
    Valvular_Apparatus: ValvularApparatus = Field(..., description="Valvular apparatus including Mitral, Aortic, Pulmonary, and Tricuspid valves and their assessments and measurements")
    GreatVessels_and_VenousReturn: GreatVesselsAndVenousReturn = Field(..., description="great vessels and venous return including Aorta, Pulmonic Vein, and IVC")
    Congenital_and_Structural_Defects: CongenitalAndStructuralDefects = Field(..., description="Details of congenital and structural defects including VSD, ASD, and PFO")
    pericardium: Pericardium = Field(..., description="pericardium assessments and measurements")
