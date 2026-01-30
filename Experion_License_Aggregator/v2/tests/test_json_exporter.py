"""
Tests for JSON exporter.

Tests JsonExporter with various data types and export scenarios.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
from tempfile import TemporaryDirectory

from v2.pipeline.exporters import JsonExporter, ExportResult
from v2.models.license import LicenseData
from v2.models.usage import UsageData
from v2.models.cost import CostCalculation
from v2.models.transfer import TransferCandidate


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_output_dir():
    """Provide temporary directory for test exports"""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def json_exporter(temp_output_dir):
    """Provide JsonExporter with temp output directory"""
    return JsonExporter(output_dir=temp_output_dir)


@pytest.fixture
def sample_license():
    """Sample LicenseData for testing"""
    return LicenseData(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        release='R520',
        product='PKS',
        customer='Marathon Petroleum',
        licensed={'PROCESSPOINTS': 4750, 'DIRECTSTATIONS': 4}
    )


@pytest.fixture
def sample_licenses():
    """Multiple sample licenses"""
    return [
        LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        ),
        LicenseData(
            msid='M0615',
            system_number='60807',
            cluster='Wilmington',
            release='R510',
            licensed={'PROCESSPOINTS': 3200}
        )
    ]


@pytest.fixture
def sample_cost():
    """Sample CostCalculation for testing"""
    return CostCalculation(
        msid='M0614',
        system_number='60806',
        license_type='PROCESSPOINTS',
        licensed_quantity=4750,
        unit_price=45.00,
        total_cost=213750.00,
        price_source='MPC 2026 Confirmed'
    )


@pytest.fixture
def sample_transfer():
    """Sample TransferCandidate for testing"""
    return TransferCandidate(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        license_type='PROCESSPOINTS',
        licensed_quantity=4750,
        used_quantity=108,
        excess_quantity=4642,
        excess_value=208890.00,
        unit_price=45.00,
        priority='HIGH'
    )


# ============================================================================
# Test JsonExporter Initialization
# ============================================================================

class TestJsonExporterInitialization:
    """Tests for JsonExporter initialization"""
    
    def test_initialization_with_output_dir(self, temp_output_dir):
        """Exporter initializes with provided output directory"""
        exporter = JsonExporter(output_dir=temp_output_dir)
        
        assert exporter.output_dir == temp_output_dir
        assert exporter.indent == 2
        assert exporter.ensure_ascii == False
    
    def test_initialization_creates_output_dir(self, temp_output_dir):
        """Exporter creates output directory if it doesn't exist"""
        subdir = temp_output_dir / 'nested' / 'export'
        exporter = JsonExporter(output_dir=subdir)
        
        assert subdir.exists()
        assert subdir.is_dir()
    
    def test_initialization_with_custom_indent(self, temp_output_dir):
        """Exporter accepts custom indentation"""
        exporter = JsonExporter(output_dir=temp_output_dir, indent=4)
        
        assert exporter.indent == 4


# ============================================================================
# Test Single Record Export
# ============================================================================

class TestSingleRecordExport:
    """Tests for exporting single records"""
    
    def test_export_single_license(self, json_exporter, sample_license):
        """Export single LicenseData to JSON"""
        result = json_exporter.export(sample_license, 'single_license.json')
        
        assert result.success == True
        assert result.output_path.exists()
        assert result.format == 'json'
        assert result.record_count == 1
        
        # Verify JSON content
        with open(result.output_path) as f:
            data = json.load(f)
        
        assert data['msid'] == 'M0614'
        assert data['cluster'] == 'Carson'
        assert 'PROCESSPOINTS' in data['licensed']
    
    def test_export_single_cost(self, json_exporter, sample_cost):
        """Export single CostCalculation to JSON"""
        result = json_exporter.export(sample_cost, 'single_cost.json')
        
        assert result.success == True
        
        with open(result.output_path) as f:
            data = json.load(f)
        
        assert data['msid'] == 'M0614'
        assert data['total_cost'] == 213750.00
        assert data['price_source'] == 'MPC 2026 Confirmed'
    
    def test_filename_without_extension_gets_json(self, json_exporter, sample_license):
        """Filename without .json extension gets it added"""
        result = json_exporter.export(sample_license, 'test_file')
        
        assert result.output_path.name == 'test_file.json'
    
    def test_filename_with_extension_unchanged(self, json_exporter, sample_license):
        """Filename with .json extension is not modified"""
        result = json_exporter.export(sample_license, 'test.json')
        
        assert result.output_path.name == 'test.json'


# ============================================================================
# Test List Export
# ============================================================================

class TestListExport:
    """Tests for exporting lists of records"""
    
    def test_export_license_list(self, json_exporter, sample_licenses):
        """Export list of licenses to JSON"""
        result = json_exporter.export(sample_licenses, 'licenses.json')
        
        assert result.success == True
        assert result.record_count == 2
        
        with open(result.output_path) as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]['msid'] == 'M0614'
        assert data[1]['msid'] == 'M0615'
    
    def test_export_empty_list(self, json_exporter):
        """Export empty list succeeds"""
        result = json_exporter.export([], 'empty.json')
        
        assert result.success == True
        assert result.record_count == 0
        
        with open(result.output_path) as f:
            data = json.load(f)
        
        assert data == []


# ============================================================================
# Test Dictionary Export
# ============================================================================

class TestDictionaryExport:
    """Tests for exporting dictionary structures"""
    
    def test_export_nested_dict(self, json_exporter, sample_licenses):
        """Export nested dictionary structure"""
        data = {
            'metadata': {
                'export_time': datetime.now().isoformat(),
                'total': len(sample_licenses)
            },
            'licenses': sample_licenses
        }
        
        result = json_exporter.export(data, 'nested.json')
        
        assert result.success == True
        
        with open(result.output_path) as f:
            loaded = json.load(f)
        
        assert 'metadata' in loaded
        assert 'licenses' in loaded
        assert len(loaded['licenses']) == 2
    
    def test_record_count_from_dict(self, json_exporter, sample_licenses):
        """Record count calculated from dictionary with list"""
        data = {'licenses': sample_licenses}
        
        result = json_exporter.export(data, 'dict_count.json')
        
        assert result.record_count == 2


# ============================================================================
# Test Summary Export
# ============================================================================

class TestSummaryExport:
    """Tests for export_summary method"""
    
    def test_export_summary_all_data(
        self, json_exporter, sample_licenses, sample_cost, sample_transfer
    ):
        """Export comprehensive summary with all data types"""
        result = json_exporter.export_summary(
            licenses=sample_licenses,
            costs=[sample_cost],
            transfers=[sample_transfer],
            filename='summary.json'
        )
        
        assert result.success == True
        
        with open(result.output_path) as f:
            data = json.load(f)
        
        assert 'export_metadata' in data
        assert 'licenses' in data
        assert 'costs' in data
        assert 'transfers' in data
        assert 'statistics' in data
        
        assert len(data['licenses']) == 2
        assert len(data['costs']) == 1
        assert len(data['transfers']) == 1
    
    def test_summary_statistics_calculated(
        self, json_exporter, sample_licenses, sample_cost, sample_transfer
    ):
        """Summary includes calculated statistics"""
        result = json_exporter.export_summary(
            licenses=sample_licenses,
            costs=[sample_cost],
            transfers=[sample_transfer]
        )
        
        with open(result.output_path) as f:
            data = json.load(f)
        
        stats = data['statistics']
        assert stats['total_systems'] == 2
        assert stats['total_cost'] == 213750.00
        assert stats['total_transfers'] == 1
        assert 'clusters' in stats
        assert 'transfer_priorities' in stats


# ============================================================================
# Test Formatting Options
# ============================================================================

class TestFormattingOptions:
    """Tests for JSON formatting options"""
    
    def test_compact_format_no_indent(self, temp_output_dir, sample_license):
        """Compact format with indent=0"""
        exporter = JsonExporter(output_dir=temp_output_dir, indent=0)
        result = exporter.export(sample_license, 'compact.json')
        
        with open(result.output_path) as f:
            content = f.read()
        
        # Compact format has no newlines except at end
        assert content.count('\n') <= 1
    
    def test_pretty_format_with_indent(self, temp_output_dir, sample_license):
        """Pretty format with indent=2"""
        exporter = JsonExporter(output_dir=temp_output_dir, indent=2)
        result = exporter.export(sample_license, 'pretty.json')
        
        with open(result.output_path) as f:
            content = f.read()
        
        # Pretty format has multiple newlines
        assert content.count('\n') > 5
    
    def test_override_indent_in_export(self, json_exporter, sample_license):
        """Export accepts indent override"""
        result = json_exporter.export(sample_license, 'override.json', indent=4)
        
        # Check metadata includes custom indent
        assert result.metadata['indent'] == 4


# ============================================================================
# Test Datetime Serialization
# ============================================================================

class TestDatetimeSerialization:
    """Tests for datetime handling"""
    
    def test_datetime_serialized_to_iso(self, json_exporter):
        """Datetime objects serialized to ISO format"""
        data = {
            'timestamp': datetime(2025, 1, 29, 12, 0, 0)
        }
        
        result = json_exporter.export(data, 'datetime.json')
        
        with open(result.output_path) as f:
            loaded = json.load(f)
        
        assert loaded['timestamp'] == '2025-01-29T12:00:00'
    
    def test_license_with_date_serialized(self, json_exporter):
        """License with license_date serializes correctly"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            license_date=datetime(2025, 1, 15),
            licensed={}
        )
        
        result = json_exporter.export(license, 'dated.json')
        
        with open(result.output_path) as f:
            data = json.load(f)
        
        assert 'license_date' in data
        assert data['license_date'] == '2025-01-15T00:00:00'


# ============================================================================
# Test Error Handling
# ============================================================================

class TestErrorHandling:
    """Tests for error scenarios"""
    
    def test_invalid_output_path_fails_gracefully(self, temp_output_dir):
        """Invalid output path returns error result"""
        # Create exporter with valid dir
        exporter = JsonExporter(output_dir=temp_output_dir)
        
        # Make export fail by using invalid data that can't be serialized
        class UnserializableClass:
            def __init__(self):
                self.circular = self  # Circular reference
        
        result = exporter.export(UnserializableClass(), 'test.json')
        
        assert result.success == False
        assert len(result.errors) > 0
        assert 'failed' in result.errors[0].lower()
    
    def test_export_result_validation(self):
        """ExportResult validates consistency"""
        # Success with errors should raise
        with pytest.raises(ValueError, match="cannot have success=True"):
            ExportResult(success=True, errors=['error'])
        
        # Failure without errors should raise
        with pytest.raises(ValueError, match="must have at least one error"):
            ExportResult(success=False, errors=[])


# ============================================================================
# Test File Metadata
# ============================================================================

class TestFileMetadata:
    """Tests for export metadata"""
    
    def test_result_includes_file_size(self, json_exporter, sample_licenses):
        """Export result includes file size"""
        result = json_exporter.export(sample_licenses, 'sizes.json')
        
        assert 'file_size' in result.metadata
        assert result.metadata['file_size'] > 0
    
    def test_result_includes_export_time(self, json_exporter, sample_license):
        """Export result includes timestamp"""
        before = datetime.now()
        result = json_exporter.export(sample_license, 'time.json')
        after = datetime.now()
        
        assert before <= result.export_time <= after


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and unusual inputs"""
    
    def test_export_none_value(self, json_exporter):
        """Export None value"""
        result = json_exporter.export(None, 'none.json')
        
        assert result.success == True
        
        with open(result.output_path) as f:
            data = json.load(f)
        
        assert data is None
    
    def test_export_complex_nested_structure(self, json_exporter, sample_licenses):
        """Export deeply nested structure"""
        data = {
            'level1': {
                'level2': {
                    'level3': {
                        'licenses': sample_licenses
                    }
                }
            }
        }
        
        result = json_exporter.export(data, 'nested.json')
        
        assert result.success == True
        
        with open(result.output_path) as f:
            loaded = json.load(f)
        
        assert len(loaded['level1']['level2']['level3']['licenses']) == 2
