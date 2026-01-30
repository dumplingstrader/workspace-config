"""
Constants and enumerations for V2.0 pipeline.

Centralized constants prevent magic values in code.
"""

from enum import Enum, auto


class LicenseType(Enum):
    """
    All supported Experion license types.
    
    Note: DIRECTSTATIONS (XML) and CONSOLE_STATIONS (CSV) are synonyms
    handled by field mapping configuration.
    """
    PROCESSPOINTS = "PROCESSPOINTS"
    SCADAPOINTS = "SCADAPOINTS"
    STATIONS = "STATIONS"
    MULTISTATIONS = "MULTISTATIONS"
    DIRECTSTATIONS = "DIRECTSTATIONS"
    CONSOLE_STATIONS = "CONSOLE_STATIONS"
    DUAL = "DUAL"
    DAS = "DAS"
    API = "API"
    SQL = "SQL"
    HISTORIAN = "HISTORIAN"
    REPORTING = "REPORTING"
    ADVANCED = "ADVANCED"
    BATCH = "BATCH"
    CONTROLLER = "CONTROLLER"
    CONTROLLERIO = "CONTROLLERIO"
    REMOTETERMINALUNIT = "REMOTETERMINALUNIT"
    WEBSERVER = "WEBSERVER"
    DATAHISTORIAN = "DATAHISTORIAN"
    ALARMMANAGER = "ALARMMANAGER"
    TRENDMANAGER = "TRENDMANAGER"
    BATCHMANAGER = "BATCHMANAGER"
    # Add more as discovered in data


class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "ERROR"      # Must fix - blocks processing
    WARNING = "WARNING"  # Should fix - allows processing
    INFO = "INFO"        # Informational only


class ProcessingStage(Enum):
    """Pipeline processing stages"""
    EXTRACTION = auto()      # XML/CSV parsing
    VALIDATION = auto()      # Quality gates
    TRANSFORMATION = auto()  # Dedup, matching, enrichment
    EXPORT = auto()         # JSON/Excel generation


class PriceSource(Enum):
    """Cost pricing sources"""
    MPC_2026_CONFIRMED = "MPC 2026 Confirmed"
    HONEYWELL_BASELINE = "Honeywell Baseline"
    PLACEHOLDER = "Placeholder $100"


class TransferPriority(Enum):
    """Transfer candidate priority levels"""
    HIGH = "HIGH"      # >$50k excess value
    MEDIUM = "MEDIUM"  # $10k-$50k excess value
    LOW = "LOW"        # <$10k excess value


class ExcelSheetName(Enum):
    """Standard Excel sheet names"""
    PKS = "PKS"
    CARSON = "Carson"
    WILMINGTON = "Wilmington"
    TRANSFER_CANDIDATES = "Transfer Candidates"
    SUMMARY = "Summary"
    RAW_DATA = "Raw Data"


# ============================================================================
# File Path Constants
# ============================================================================

# Data directories
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
VALIDATED_DATA_DIR = f"{DATA_DIR}/validated"
ENRICHED_DATA_DIR = f"{DATA_DIR}/enriched"
OUTPUT_DIR = f"{DATA_DIR}/output"
CHECKPOINT_DIR = f"{DATA_DIR}/checkpoints"

# Configuration
CONFIG_DIR = "config"
V2_CONFIG_DIR = "v2/config"

# ============================================================================
# Data Quality Thresholds (Default - override in config)
# ============================================================================

# Minimum percentage of systems that must have valid data
MIN_EXTRACTION_RATE = 0.90  # 90% of XML files must parse successfully
MIN_MATCH_RATE = 0.50       # 50% of licenses must match usage data
MIN_VALIDATION_PASS_RATE = 0.80  # 80% of records must pass validation

# Fuzzy matching
MIN_MATCH_CONFIDENCE = 0.80  # 80% confidence for MSID matching
LEVENSHTEIN_THRESHOLD = 2    # Max character differences for fuzzy match

# ============================================================================
# Business Rules (Default - override in config)
# ============================================================================

# License age (days)
MAX_LICENSE_AGE_DAYS = 3650  # 10 years

# Customer name patterns (for validation)
VALID_CUSTOMER_PATTERNS = ['Marathon', 'MPC', 'Marathon Petroleum']

# Transfer candidate thresholds (examples)
HIGH_VALUE_THRESHOLD = 50000  # $50k
MEDIUM_VALUE_THRESHOLD = 10000  # $10k

# ============================================================================
# File Naming Patterns
# ============================================================================

# XML file pattern: {cluster}/MSID_SystemNumber_vVersion.xml
XML_FILE_PATTERN = r"(?P<msid>M\d+)_(?P<system_number>\d+)(_v(?P<version>\d+))?\.xml"

# CSV file pattern: BC-LAR-{course_number}.csv
CSV_FILE_PATTERN = r"BC-LAR-(?P<course>\d+)\.csv"

# Output file timestamp format
OUTPUT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# ============================================================================
# Excel Formatting Constants
# ============================================================================

# Column widths (characters)
EXCEL_COL_WIDTH_SYSTEM = 20
EXCEL_COL_WIDTH_LICENSE_TYPE = 25
EXCEL_COL_WIDTH_NUMBER = 12
EXCEL_COL_WIDTH_CURRENCY = 15

# Colors (RGB tuples)
COLOR_HEADER_FILL = (0, 51, 102)      # Dark blue
COLOR_HEADER_TEXT = (255, 255, 255)   # White
COLOR_HIGH_PRIORITY = (255, 0, 0)     # Red
COLOR_MEDIUM_PRIORITY = (255, 165, 0) # Orange
COLOR_LOW_PRIORITY = (255, 255, 0)    # Yellow

# Number formats
FORMAT_CURRENCY = '$#,##0.00'
FORMAT_INTEGER = '#,##0'
FORMAT_PERCENTAGE = '0.0%'
FORMAT_DATE = 'yyyy-mm-dd'

# ============================================================================
# Logging Configuration
# ============================================================================

# Log levels by stage
LOG_LEVEL_EXTRACTION = "INFO"
LOG_LEVEL_VALIDATION = "WARNING"
LOG_LEVEL_TRANSFORMATION = "INFO"
LOG_LEVEL_EXPORT = "INFO"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
