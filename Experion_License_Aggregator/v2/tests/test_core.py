"""
Test suite for core infrastructure (exceptions, config, constants).
"""

import pytest
from pathlib import Path
from v2.core.config import Config
from v2.core.constants import LicenseType, ValidationLevel, ProcessingStage
from v2.core.exceptions import (
    DataverseBaseError,
    XmlParsingError,
    DataValidationError,
    MissingConfigError,
    ConfigurationError,
    format_error_context
)


# ============================================================================
# Exception Tests
# ============================================================================

class TestExceptionHierarchy:
    """Test exception inheritance and attributes"""
    
    def test_xml_parsing_error_with_file_path(self):
        """XmlParsingError stores file path"""
        error = XmlParsingError("Bad XML", file_path="test.xml")
        assert error.file_path == "test.xml"
        assert "test.xml" in str(error)
    
    def test_validation_error_with_field(self):
        """DataValidationError stores field and value"""
        error = DataValidationError("Invalid", field="msid", value="")
        assert error.field == "msid"
        assert error.value == ""
        assert "msid" in str(error)
    
    def test_missing_config_error(self):
        """MissingConfigError stores key and file"""
        error = MissingConfigError(key="threshold", config_file="rules.yaml")
        assert error.key == "threshold"
        assert error.config_file == "rules.yaml"
    
    def test_exception_hierarchy(self):
        """All exceptions inherit from DataverseBaseError"""
        try:
            raise XmlParsingError("Test")
        except DataverseBaseError:
            pass  # Should catch
    
    def test_format_error_context(self):
        """Format error with context for logging"""
        error = XmlParsingError("Bad XML", file_path="test.xml")
        context = format_error_context(error, {"stage": "extraction"})
        
        assert context['type'] == 'XmlParsingError'
        assert context['file_path'] == 'test.xml'
        assert context['context']['stage'] == 'extraction'


# ============================================================================
# Constants Tests
# ============================================================================

class TestConstants:
    """Test constant enumerations"""
    
    def test_license_type_enum(self):
        """LicenseType enum has expected values"""
        assert LicenseType.PROCESSPOINTS.value == "PROCESSPOINTS"
        assert LicenseType.DIRECTSTATIONS.value == "DIRECTSTATIONS"
        assert LicenseType.CONSOLE_STATIONS.value == "CONSOLE_STATIONS"
    
    def test_validation_level_enum(self):
        """ValidationLevel enum has ERROR, WARNING, INFO"""
        assert ValidationLevel.ERROR.value == "ERROR"
        assert ValidationLevel.WARNING.value == "WARNING"
        assert ValidationLevel.INFO.value == "INFO"
    
    def test_processing_stage_enum(self):
        """ProcessingStage enum has all stages"""
        assert ProcessingStage.EXTRACTION
        assert ProcessingStage.VALIDATION
        assert ProcessingStage.TRANSFORMATION
        assert ProcessingStage.EXPORT


# ============================================================================
# Config Tests
# ============================================================================

class TestConfigLoading:
    """Test configuration loading"""
    
    def test_config_loads_from_directory(self):
        """Config loads all files from directory"""
        config = Config.from_directory('v2/config')
        
        # Check YAML files loaded
        assert config.field_mappings is not None
        assert config.cost_rules is not None
        assert config.validation_rules is not None
        assert config.transfer_rules is not None
        
        # Check JSON files loaded
        assert config.system_names is not None
        assert config.cost_catalog is not None
        assert config.cost_catalog_mpc is not None
        assert config.settings is not None
    
    def test_config_fails_on_missing_directory(self):
        """Config raises error for missing directory"""
        with pytest.raises(ConfigurationError, match="not found"):
            Config(config_dir='nonexistent')
    
    def test_get_csv_field_name(self):
        """Get CSV field name from XML name"""
        config = Config.from_directory('v2/config')
        csv_name = config.get_csv_field_name('DIRECTSTATIONS')
        assert csv_name == 'CONSOLE_STATIONS'
    
    def test_get_display_name(self):
        """Get display name for field"""
        config = Config.from_directory('v2/config')
        display = config.get_display_name('PROCESSPOINTS')
        assert display is not None
    
    def test_get_cost_for_license_type(self):
        """Get cost using cascade strategy"""
        config = Config.from_directory('v2/config')
        
        # Should try MPC 2026 first, then Honeywell, then placeholder
        cost = config.get_cost_for('PROCESSPOINTS')
        assert cost is not None
        assert cost > 0
    
    def test_get_price_source(self):
        """Get price source label"""
        config = Config.from_directory('v2/config')
        source = config.get_price_source('PROCESSPOINTS')
        assert source in ['MPC 2026 Confirmed', 'Honeywell Baseline', 'Placeholder $100']
    
    def test_get_validation_threshold(self):
        """Get data quality threshold"""
        config = Config.from_directory('v2/config')
        threshold = config.get_validation_threshold('extraction_success_rate')
        assert threshold > 0
        assert threshold <= 1.0
    
    def test_get_transfer_threshold(self):
        """Get transfer detection threshold"""
        config = Config.from_directory('v2/config')
        threshold = config.get_transfer_threshold('PROCESSPOINTS', 'absolute')
        assert threshold is not None
        assert threshold > 0
    
    def test_get_friendly_name(self):
        """Get friendly system name from catalog"""
        config = Config.from_directory('v2/config')
        # Use real system from catalog or fallback
        friendly = config.get_friendly_name('M0614', '60806')
        assert friendly is not None
    
    def test_clusters_property(self):
        """Get list of clusters"""
        config = Config.from_directory('v2/config')
        clusters = config.clusters
        assert isinstance(clusters, list)
        assert len(clusters) > 0
