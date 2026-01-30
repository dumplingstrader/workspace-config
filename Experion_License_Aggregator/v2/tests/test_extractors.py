"""
Test Suite for XML Extractor

Tests XML parsing, file metadata extraction, validation, and error handling.
"""

import pytest
from pathlib import Path
from datetime import datetime

from v2.pipeline.extractors.xml_extractor import XmlExtractor
from v2.pipeline.extractors.base_extractor import ExtractionResult
from v2.models.license import LicenseData
from v2.core.exceptions import XmlParsingError


class TestXmlExtractorBasics:
    """Test basic extractor functionality."""
    
    def test_can_handle_xml_file(self):
        """Extractor recognizes XML files"""
        extractor = XmlExtractor()
        assert extractor.can_handle(Path('test.xml')) == True
        assert extractor.can_handle(Path('TEST.XML')) == True
    
    def test_cannot_handle_non_xml(self):
        """Extractor rejects non-XML files"""
        extractor = XmlExtractor()
        assert extractor.can_handle(Path('test.csv')) == False
        assert extractor.can_handle(Path('test.txt')) == False
    
    def test_extractor_initialization(self):
        """Extractor initializes with correct defaults"""
        extractor = XmlExtractor()
        assert extractor.strict_mode == False
        assert len(extractor.warnings) == 0
        assert len(extractor.errors) == 0
    
    def test_strict_mode_initialization(self):
        """Extractor can be initialized in strict mode"""
        extractor = XmlExtractor(strict_mode=True)
        assert extractor.strict_mode == True


class TestXmlValidation:
    """Test XML structure validation."""
    
    def test_valid_xml_structure(self):
        """Valid XML passes structure validation"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        assert extractor.validate_structure(xml_path) == True
    
    def test_missing_details_element(self):
        """XML without <details> raises error"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/malformed.xml')
        
        with pytest.raises(XmlParsingError) as exc_info:
            extractor.validate_structure(xml_path)
        
        assert 'Missing <details> element' in str(exc_info.value)
    
    def test_missing_file_raises_error(self):
        """Non-existent file fails extraction"""
        extractor = XmlExtractor()
        result = extractor.extract_from_file(Path('nonexistent.xml'))
        
        assert result.success == False
        assert len(result.errors) > 0
        assert 'not found' in result.errors[0].lower()


class TestMetadataExtraction:
    """Test extraction of metadata from file paths and names."""
    
    def test_extract_msid_from_filename(self):
        """Extract MSID from filename pattern"""
        extractor = XmlExtractor()
        path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        msid = extractor._extract_msid(path)
        assert msid == 'M0614'
    
    def test_extract_msid_with_extension(self):
        """Extract MSID with -EX extension"""
        extractor = XmlExtractor()
        path = Path('M13287-EX10_Experion_PKS_R52X_x_131844_2.xml')
        
        msid = extractor._extract_msid(path)
        assert msid == 'M13287-EX10'
    
    def test_extract_system_number(self):
        """Extract system number from filename"""
        extractor = XmlExtractor()
        path = Path('M0614_Experion_PKS_R520_x_60806_40.xml')
        
        system_number = extractor._extract_system_number(path)
        assert system_number == '60806'
    
    def test_extract_version(self):
        """Extract version number from filename"""
        extractor = XmlExtractor()
        path = Path('M0614_Experion_PKS_R520_x_60806_40.xml')
        
        version = extractor._extract_version(path)
        assert version == 40
    
    def test_extract_cluster_from_path(self):
        """Extract cluster from file path"""
        extractor = XmlExtractor()
        path = Path('data/raw/Carson/ESVT0 M0614 60806/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        cluster = extractor._extract_cluster(path)
        assert cluster == 'Carson'


class TestLicenseDataExtraction:
    """Test extraction of complete LicenseData from XML."""
    
    def test_successful_extraction(self):
        """Extract complete LicenseData from valid XML"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        result = extractor.extract_from_file(xml_path)
        
        assert result.success == True
        assert result.data is not None
        assert isinstance(result.data, LicenseData)
    
    def test_extraction_result_metadata(self):
        """Extraction result contains correct metadata"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        result = extractor.extract_from_file(xml_path)
        
        assert result.source_file == xml_path
        assert isinstance(result.extraction_time, datetime)
        assert len(result.errors) == 0
    
    def test_extracted_license_basic_fields(self):
        """Extracted license has correct basic fields"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        result = extractor.extract_from_file(xml_path)
        license_data = result.data
        
        assert license_data.msid == 'M0614'
        assert license_data.system_number == '60806'
        assert license_data.release == '520'
        assert license_data.product == 'EXP_PKS'
        assert license_data.customer == 'Marathon Petroleum Corp'
        assert license_data.file_version == 40
    
    def test_extracted_license_date(self):
        """Extracted license has parsed date"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        result = extractor.extract_from_file(xml_path)
        license_data = result.data
        
        assert license_data.license_date is not None
        assert isinstance(license_data.license_date, datetime)
        assert license_data.license_date.year == 2025
        assert license_data.license_date.month == 1
        assert license_data.license_date.day == 15
    
    def test_extracted_license_options(self):
        """Extracted license has correct options"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        result = extractor.extract_from_file(xml_path)
        license_data = result.data
        
        assert license_data.licensed['PROCESSPOINTS'] == 4750
        assert license_data.licensed['SCADAPOINTS'] == 1500
        assert license_data.licensed['DIRECTSTATIONS'] == 6
        assert license_data.licensed['STATIONS'] == 3
        assert license_data.licensed['CDA_IO_ANA'] == 200
        assert license_data.licensed['CDA_IO_DIG'] == 600
    
    def test_extracted_license_unique_key(self):
        """Extracted license generates correct unique key"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/M0614_Experion_PKS_R520_x_60806_40.xml')
        
        result = extractor.extract_from_file(xml_path)
        license_data = result.data
        
        # unique_key should be (cluster, msid, system_number)
        # Cluster extraction will fail from this test path, so check structure
        assert isinstance(license_data.unique_key, tuple)
        assert len(license_data.unique_key) == 3
        assert license_data.unique_key[1] == 'M0614'  # msid
        assert license_data.unique_key[2] == '60806'  # system_number


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_malformed_xml_fails(self):
        """Malformed XML returns failure result"""
        extractor = XmlExtractor()
        xml_path = Path('v2/tests/test_data/malformed.xml')
        
        with pytest.raises(XmlParsingError):
            extractor.extract_from_file(xml_path)
    
    def test_extractor_reset(self):
        """Extractor resets warnings and errors"""
        extractor = XmlExtractor()
        
        # Add some warnings/errors
        extractor._add_warning("Test warning")
        extractor._add_error("Test error")
        
        assert len(extractor.warnings) > 0
        assert len(extractor.errors) > 0
        
        # Reset
        extractor.reset()
        
        assert len(extractor.warnings) == 0
        assert len(extractor.errors) == 0


class TestExtractionResultValidation:
    """Test ExtractionResult validation rules."""
    
    def test_successful_result_must_have_data(self):
        """Successful result requires data"""
        from v2.pipeline.extractors.base_extractor import ExtractionResult
        from v2.core.constants import ProcessingStage
        
        with pytest.raises(ValueError) as exc_info:
            ExtractionResult(
                success=True,
                data=None,  # Invalid: success but no data
                source_file=Path('test.xml'),
                warnings=[],
                errors=[],
                extraction_time=datetime.now(),
                stage=ProcessingStage.EXTRACTION
            )
        
        assert 'must have data' in str(exc_info.value)
    
    def test_failed_result_must_have_errors(self):
        """Failed result requires errors"""
        from v2.pipeline.extractors.base_extractor import ExtractionResult
        from v2.core.constants import ProcessingStage
        
        with pytest.raises(ValueError) as exc_info:
            ExtractionResult(
                success=False,
                data=None,
                source_file=Path('test.xml'),
                warnings=[],
                errors=[],  # Invalid: failure but no errors
                extraction_time=datetime.now(),
                stage=ProcessingStage.EXTRACTION
            )
        
        assert 'must have errors' in str(exc_info.value)
