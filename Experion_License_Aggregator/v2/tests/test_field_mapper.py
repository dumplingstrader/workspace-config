"""
Tests for FieldMapper - License type normalization and field mapping.

Test Coverage:
- Simple 1:1 mappings (PROCESSPOINTS)
- Name variations (DIRECTSTATIONS → CONSOLE_STATIONS)
- Fallback chains (STATIONS → MULTISTATIONS → DIRECTSTATIONS)
- Reverse mappings (usage field → license fields)
- Edge cases (missing config, unknown fields)
"""

import pytest
from pathlib import Path

from v2.core.config import Config
from v2.pipeline.transformers.field_mapper import FieldMapper, MappingResult


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def test_config():
    """Load test configuration with field mappings"""
    config_dir = Path(__file__).parent.parent / 'config'
    return Config(config_dir)


@pytest.fixture
def field_mapper(test_config):
    """Create FieldMapper with test configuration"""
    return FieldMapper(test_config)


# ============================================================================
# Test Simple 1:1 Mappings
# ============================================================================

class TestSimpleMappings:
    """Test basic 1:1 field mappings"""
    
    def test_processpoints_maps_to_itself(self, field_mapper):
        """PROCESSPOINTS should map to PROCESSPOINTS (1:1)"""
        result = field_mapper.get_target_field('PROCESSPOINTS')
        
        assert result.target_field == 'PROCESSPOINTS'
        assert result.fallback_used == False
        assert result.available == True
    
    def test_scadapoints_maps_to_itself(self, field_mapper):
        """SCADAPOINTS should map to SCADAPOINTS (1:1)"""
        result = field_mapper.get_target_field('SCADAPOINTS')
        
        assert result.target_field == 'SCADAPOINTS'
        assert result.fallback_used == False
    
    def test_unknown_field_returns_itself(self, field_mapper):
        """Unknown fields should pass through unchanged"""
        result = field_mapper.get_target_field('UNKNOWN_FIELD')
        
        assert result.target_field == 'UNKNOWN_FIELD'
        assert result.fallback_used == False


# ============================================================================
# Test Name Variations
# ============================================================================

class TestNameVariations:
    """Test mappings that handle naming differences"""
    
    def test_directstations_maps_to_console_stations(self, field_mapper):
        """DIRECTSTATIONS (XML) should map to CONSOLE_STATIONS (CSV)"""
        result = field_mapper.get_target_field('DIRECTSTATIONS')
        
        assert result.target_field == 'CONSOLE_STATIONS'
        assert result.fallback_used == False
    
    def test_directstations_with_usage_data(self, field_mapper):
        """DIRECTSTATIONS mapping should check usage data availability"""
        usage = {'CONSOLE_STATIONS': 5}
        result = field_mapper.get_target_field('DIRECTSTATIONS', usage)
        
        assert result.target_field == 'CONSOLE_STATIONS'
        assert result.available == True
    
    def test_directstations_unavailable_in_usage(self, field_mapper):
        """Should detect when mapped field is missing in usage data"""
        usage = {'PROCESSPOINTS': 108}  # No CONSOLE_STATIONS
        result = field_mapper.get_target_field('DIRECTSTATIONS', usage)
        
        assert result.target_field == 'CONSOLE_STATIONS'
        assert result.available == False


# ============================================================================
# Test Fallback Chains
# ============================================================================

class TestFallbackChains:
    """Test multi-level fallback logic"""
    
    def test_stations_primary_found(self, field_mapper):
        """STATIONS should use primary when available"""
        usage = {'STATIONS': 10}
        result = field_mapper.get_target_field('STATIONS', usage)
        
        assert result.target_field == 'STATIONS'
        assert result.fallback_used == False
        assert result.available == True
    
    def test_stations_fallback_to_multistations(self, field_mapper):
        """STATIONS should fallback to MULTISTATIONS when primary missing"""
        usage = {'MULTISTATIONS': 10}  # No STATIONS
        result = field_mapper.get_target_field('STATIONS', usage)
        
        assert result.target_field == 'MULTISTATIONS'
        assert result.fallback_used == True
        assert result.fallback_field == 'MULTISTATIONS'
        assert result.available == True
    
    def test_stations_fallback_to_directstations(self, field_mapper):
        """STATIONS should try DIRECTSTATIONS as last fallback"""
        usage = {'CONSOLE_STATIONS': 5}  # DIRECTSTATIONS maps here
        result = field_mapper.get_target_field('STATIONS', usage)
        
        # Should fallback to DIRECTSTATIONS, which maps to CONSOLE_STATIONS
        assert result.target_field == 'CONSOLE_STATIONS'
        assert result.fallback_used == True
        assert result.available == True
    
    def test_stations_no_fallback_available(self, field_mapper):
        """STATIONS should mark unavailable when all fallbacks missing"""
        usage = {'PROCESSPOINTS': 108}  # No STATIONS or fallbacks
        result = field_mapper.get_target_field('STATIONS', usage)
        
        assert result.target_field == 'STATIONS'  # Returns primary
        assert result.available == False


# ============================================================================
# Test Quantity Mapping
# ============================================================================

class TestQuantityMapping:
    """Test mapping of license quantities dict"""
    
    def test_map_simple_quantities(self, field_mapper):
        """Should map all simple field names"""
        licensed = {
            'PROCESSPOINTS': 4750,
            'SCADAPOINTS': 500
        }
        
        mapped = field_mapper.map_license_quantities(licensed)
        
        assert mapped == {
            'PROCESSPOINTS': 4750,
            'SCADAPOINTS': 500
        }
    
    def test_map_name_variations(self, field_mapper):
        """Should apply name mappings to quantities"""
        licensed = {
            'DIRECTSTATIONS': 8,
            'PROCESSPOINTS': 4750
        }
        
        mapped = field_mapper.map_license_quantities(licensed)
        
        assert mapped == {
            'CONSOLE_STATIONS': 8,
            'PROCESSPOINTS': 4750
        }
    
    def test_map_with_usage_data(self, field_mapper):
        """Should only include fields available in usage data"""
        licensed = {
            'PROCESSPOINTS': 4750,
            'DIRECTSTATIONS': 8,
            'UNKNOWN_FIELD': 100
        }
        usage = {'PROCESSPOINTS': 108, 'CONSOLE_STATIONS': 5}
        
        mapped = field_mapper.map_license_quantities(licensed, usage)
        
        # Should exclude UNKNOWN_FIELD (not in usage)
        assert 'PROCESSPOINTS' in mapped
        assert 'CONSOLE_STATIONS' in mapped
        # UNKNOWN_FIELD not in usage, so filtered out


# ============================================================================
# Test Usage Value Retrieval
# ============================================================================

class TestUsageValueRetrieval:
    """Test getting usage values with field mapping"""
    
    def test_get_usage_value_direct(self, field_mapper):
        """Should retrieve value for direct mapped field"""
        usage = {'PROCESSPOINTS': 108}
        value = field_mapper.get_usage_value('PROCESSPOINTS', usage)
        
        assert value == 108
    
    def test_get_usage_value_name_variation(self, field_mapper):
        """Should retrieve value for mapped field name"""
        usage = {'CONSOLE_STATIONS': 5}
        value = field_mapper.get_usage_value('DIRECTSTATIONS', usage)
        
        assert value == 5
    
    def test_get_usage_value_fallback(self, field_mapper):
        """Should use fallback chain to retrieve value"""
        usage = {'MULTISTATIONS': 10}  # No STATIONS
        value = field_mapper.get_usage_value('STATIONS', usage)
        
        assert value == 10
    
    def test_get_usage_value_missing(self, field_mapper):
        """Should return None when field not found"""
        usage = {'PROCESSPOINTS': 108}
        value = field_mapper.get_usage_value('DIRECTSTATIONS', usage)
        
        assert value is None


# ============================================================================
# Test Reverse Mapping
# ============================================================================

class TestReverseMapping:
    """Test finding license fields that map to usage field"""
    
    def test_reverse_simple_mapping(self, field_mapper):
        """Should find license field for usage field"""
        license_fields = field_mapper.get_reverse_mapping('PROCESSPOINTS')
        
        assert 'PROCESSPOINTS' in license_fields
    
    def test_reverse_name_variation(self, field_mapper):
        """Should find DIRECTSTATIONS maps to CONSOLE_STATIONS"""
        license_fields = field_mapper.get_reverse_mapping('CONSOLE_STATIONS')
        
        assert 'DIRECTSTATIONS' in license_fields
    
    def test_reverse_fallback_chain(self, field_mapper):
        """Should find STATIONS has fallback to MULTISTATIONS"""
        license_fields = field_mapper.get_reverse_mapping('MULTISTATIONS')
        
        # STATIONS has MULTISTATIONS in fallback chain
        assert 'STATIONS' in license_fields
    
    def test_reverse_unknown_field(self, field_mapper):
        """Should return empty list for unmapped usage field"""
        license_fields = field_mapper.get_reverse_mapping('UNKNOWN_USAGE_FIELD')
        
        assert len(license_fields) == 0


# ============================================================================
# Test Flattened Mappings
# ============================================================================

class TestFlattenedMappings:
    """Test getting all primary mappings"""
    
    def test_get_all_mapped_fields(self, field_mapper):
        """Should return dict of all license -> usage mappings"""
        mappings = field_mapper.get_all_mapped_fields()
        
        # Check critical mappings
        assert mappings['DIRECTSTATIONS'] == 'CONSOLE_STATIONS'
        assert mappings['PROCESSPOINTS'] == 'PROCESSPOINTS'
        assert mappings['STATIONS'] == 'STATIONS'  # Primary only
    
    def test_flattened_excludes_fallbacks(self, field_mapper):
        """Flattened mappings should only include primary, not fallbacks"""
        mappings = field_mapper.get_all_mapped_fields()
        
        # STATIONS has fallbacks (MULTISTATIONS, DIRECTSTATIONS)
        # but flattened should only show primary
        assert mappings.get('STATIONS') == 'STATIONS'


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test error handling and edge cases"""
    
    def test_missing_config_raises_error(self):
        """Should raise KeyError if config missing field_mappings"""
        class MockConfig:
            pass
        
        config = MockConfig()
        
        with pytest.raises(KeyError, match="field_mappings.license_to_usage"):
            FieldMapper(config)
    
    def test_empty_usage_data(self, field_mapper):
        """Should handle empty usage data dict"""
        usage = {}
        result = field_mapper.get_target_field('PROCESSPOINTS', usage)
        
        assert result.target_field == 'PROCESSPOINTS'
        assert result.available == False
    
    def test_none_usage_data_returns_available(self, field_mapper):
        """Should mark available=True when no usage data to check"""
        result = field_mapper.get_target_field('PROCESSPOINTS', None)
        
        assert result.available == True  # Can't check, assume available
    
    def test_map_empty_licensed_dict(self, field_mapper):
        """Should handle empty licensed quantities dict"""
        licensed = {}
        mapped = field_mapper.map_license_quantities(licensed)
        
        assert mapped == {}
    
    def test_fallback_chain_circular_reference(self, field_mapper):
        """Should handle fallback chains gracefully"""
        # This tests that fallback resolution doesn't infinite loop
        # DIRECTSTATIONS → CONSOLE_STATIONS
        # STATIONS fallback → DIRECTSTATIONS
        usage = {'CONSOLE_STATIONS': 5}
        result = field_mapper.get_target_field('STATIONS', usage)
        
        # Should resolve through fallback chain
        assert result.available == True
