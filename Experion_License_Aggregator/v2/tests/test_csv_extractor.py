"""
Test Suite for CSV Extractor

Tests CSV parsing, usage data extraction, validation, and error handling.
"""

import pytest
from pathlib import Path
from datetime import datetime

from v2.pipeline.extractors.csv_extractor import CsvExtractor
from v2.pipeline.extractors.base_extractor import ExtractionResult
from v2.models.usage import UsageData
from v2.core.exceptions import CsvParsingError


class TestCsvExtractorBasics:
    """Test basic extractor functionality."""
    
    def test_can_handle_csv_file(self):
        """Extractor recognizes CSV files"""
        extractor = CsvExtractor()
        assert extractor.can_handle(Path('test.csv')) == True
        assert extractor.can_handle(Path('TEST.CSV')) == True
    
    def test_cannot_handle_non_csv(self):
        """Extractor rejects non-CSV files"""
        extractor = CsvExtractor()
        assert extractor.can_handle(Path('test.xml')) == False
        assert extractor.can_handle(Path('test.txt')) == False
    
    def test_extractor_initialization(self):
        """Extractor initializes with correct defaults"""
        extractor = CsvExtractor()
        assert extractor.strict_mode == False
        assert len(extractor.warnings) == 0
        assert len(extractor.errors) == 0
    
    def test_csv_to_license_type_mapping(self):
        """CSV field names map correctly to license types"""
        assert CsvExtractor.CSV_TO_LICENSE_TYPE['Process point(s)'] == 'PROCESSPOINTS'
        assert CsvExtractor.CSV_TO_LICENSE_TYPE['SCADA point(s)'] == 'SCADAPOINTS'
        assert CsvExtractor.CSV_TO_LICENSE_TYPE['Console station(s)'] == 'CONSOLE_STATIONS'
        assert CsvExtractor.CSV_TO_LICENSE_TYPE['Flex station(s)'] == 'STATIONS'


class TestCsvValidation:
    """Test CSV structure validation."""
    
    def test_valid_csv_structure(self):
        """Valid CSV passes structure validation"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/ESVT2.csv')
        
        assert extractor.validate_structure(csv_path) == True
    
    def test_malformed_csv_headers(self):
        """CSV with wrong headers raises error"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/malformed.csv')
        
        with pytest.raises(CsvParsingError) as exc_info:
            extractor.validate_structure(csv_path)
        
        # Check that error message mentions column count
        assert 'Expected at least 4 columns' in str(exc_info.value)
    
    def test_missing_file_raises_error(self):
        """Non-existent file fails extraction"""
        extractor = CsvExtractor()
        result = extractor.extract_from_file(Path('nonexistent.csv'))
        
        assert result.success == False
        assert len(result.errors) > 0
        assert 'not found' in result.errors[0].lower()


class TestMetadataExtraction:
    """Test extraction of metadata from CSV content."""
    
    def test_extract_system_name_from_header(self):
        """Extract system name from CSV header row"""
        extractor = CsvExtractor()
        rows = [
            ['Category', 'License Option', 'Detail Type', 'ESVT2'],
            ['Collate header', 'Collate date', 'License', '1/27/2026']
        ]
        
        system_name = extractor._extract_system_name(rows, Path('test.csv'))
        assert system_name == 'ESVT2'
    
    def test_extract_msid_from_rows(self):
        """Extract MSID from License certificate rows"""
        extractor = CsvExtractor()
        rows = [
            ['Category', 'License Option', 'Detail Type', 'ESVT2'],
            ['License certificate', 'System number', 'License', '68851'],
            ['License certificate', 'MSID/ESID', 'License', 'M8564']
        ]
        
        msid = extractor._extract_msid(rows)
        assert msid == 'M8564'
    
    def test_extract_system_number_from_rows(self):
        """Extract system number from License certificate rows"""
        extractor = CsvExtractor()
        rows = [
            ['Category', 'License Option', 'Detail Type', 'ESVT2'],
            ['License certificate', 'System number', 'License', '68851'],
            ['License certificate', 'MSID/ESID', 'License', 'M8564']
        ]
        
        system_number = extractor._extract_system_number(rows)
        assert system_number == '68851'


class TestUsageDataExtraction:
    """Test extraction of complete UsageData from CSV."""
    
    def test_successful_extraction(self):
        """Extract complete usage data list from valid CSV"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/ESVT2.csv')
        
        result = extractor.extract_from_file(csv_path)
        
        assert result.success == True
        assert result.data is not None
        assert isinstance(result.data, list)
        assert len(result.data) > 0
        assert all(isinstance(item, UsageData) for item in result.data)
    
    def test_extraction_result_metadata(self):
        """Extraction result contains correct metadata"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/ESVT2.csv')
        
        result = extractor.extract_from_file(csv_path)
        
        assert result.source_file == csv_path
        assert isinstance(result.extraction_time, datetime)
        assert len(result.errors) == 0
    
    def test_extracted_usage_basic_fields(self):
        """Extracted usage data has correct basic fields"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/ESVT2.csv')
        
        result = extractor.extract_from_file(csv_path)
        usage_list = result.data
        
        # All items should have same MSID
        assert all(u.msid == 'M8564' for u in usage_list)
    
    def test_extracted_usage_license_types(self):
        """Extracted usage includes expected license types"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/ESVT2.csv')
        
        result = extractor.extract_from_file(csv_path)
        usage_list = result.data
        
        # Create dict for easy lookup
        usage_dict = {u.license_type: u.used_quantity for u in usage_list}
        
        # Check key license types
        assert 'PROCESSPOINTS' in usage_dict
        assert usage_dict['PROCESSPOINTS'] == 3332
        
        assert 'SCADAPOINTS' in usage_dict
        assert usage_dict['SCADAPOINTS'] == 2274
        
        assert 'CONSOLE_STATIONS' in usage_dict
        assert usage_dict['CONSOLE_STATIONS'] == 4
        
        assert 'STATIONS' in usage_dict
        assert usage_dict['STATIONS'] == 2
    
    def test_extracted_usage_cda_io_points(self):
        """Extracted usage includes CDA IO points"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/ESVT2.csv')
        
        result = extractor.extract_from_file(csv_path)
        usage_dict = {u.license_type: u.used_quantity for u in result.data}
        
        assert 'CDA_IO_ANA' in usage_dict
        assert usage_dict['CDA_IO_ANA'] == 150
        
        assert 'CDA_IO_DIG' in usage_dict
        assert usage_dict['CDA_IO_DIG'] == 450
    
    def test_extracted_usage_match_keys(self):
        """Extracted usage has correct match keys"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/ESVT2.csv')
        
        result = extractor.extract_from_file(csv_path)
        
        # Check match_key property (msid, license_type)
        for usage in result.data:
            match_key = usage.match_key
            assert isinstance(match_key, tuple)
            assert len(match_key) == 2
            assert match_key[0] == 'M8564'  # msid
            assert match_key[1] == usage.license_type


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_malformed_csv_fails(self):
        """Malformed CSV returns failure"""
        extractor = CsvExtractor()
        csv_path = Path('v2/tests/test_data/malformed.csv')
        
        with pytest.raises(CsvParsingError):
            extractor.extract_from_file(csv_path)
    
    def test_extractor_reset(self):
        """Extractor resets warnings and errors"""
        extractor = CsvExtractor()
        
        # Add some warnings/errors
        extractor._add_warning("Test warning")
        extractor._add_error("Test error")
        
        assert len(extractor.warnings) > 0
        assert len(extractor.errors) > 0
        
        # Reset
        extractor.reset()
        
        assert len(extractor.warnings) == 0
        assert len(extractor.errors) == 0
    
    def test_empty_csv_no_usage_data(self):
        """CSV with no usage rows returns failure"""
        extractor = CsvExtractor()
        
        # Create minimal CSV with no usage data
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('Category,License Option,Detail Type,TEST\n')
            f.write('License certificate,System number,License,12345\n')
            f.write('License certificate,MSID/ESID,License,M0000\n')
            temp_path = Path(f.name)
        
        try:
            result = extractor.extract_from_file(temp_path)
            
            assert result.success == False
            assert 'No usage data found' in result.errors[0]
        finally:
            temp_path.unlink()


class TestMultipleExtractors:
    """Test using both XML and CSV extractors together."""
    
    def test_different_extractors_for_different_files(self):
        """XML and CSV extractors handle their respective formats"""
        from v2.pipeline.extractors import XmlExtractor
        
        xml_extractor = XmlExtractor()
        csv_extractor = CsvExtractor()
        
        xml_path = Path('test.xml')
        csv_path = Path('test.csv')
        
        assert xml_extractor.can_handle(xml_path) == True
        assert xml_extractor.can_handle(csv_path) == False
        
        assert csv_extractor.can_handle(csv_path) == True
        assert csv_extractor.can_handle(xml_path) == False
