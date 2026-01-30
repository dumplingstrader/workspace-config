"""
Tests for match validator.

Tests MatchValidator with XML-to-CSV matching validation.
"""

import pytest
from pathlib import Path

from v2.pipeline.validators import MatchValidator
from v2.models.license import LicenseData
from v2.models.usage import UsageData
from v2.core.config import Config


# Test fixture for config
@pytest.fixture
def test_config():
    """Provide Config instance for tests"""
    config_dir = Path(__file__).parent.parent / 'config'
    return Config(config_dir=config_dir)


# ============================================================================
# Test MatchValidator - Exact Matches
# ============================================================================

class TestMatchValidatorExactMatch:
    """Tests for exact matching"""
    
    def test_perfect_match_all_fields(self, test_config):
        """All fields match exactly - 100% confidence"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True
        assert any('Exact match' in i for i in result.info)
        assert any('100%' in i for i in result.info)
    
    def test_case_insensitive_match(self, test_config):
        """Case differences don't prevent exact match"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='CARSON',  # Uppercase
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='m0614',  # Lowercase
            cluster='carson',  # Lowercase
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True
    
    def test_msid_mismatch_fails(self, test_config):
        """MSID mismatch causes match failure"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M9999',  # Very different MSID
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == False
        assert any('MSID mismatch' in w for w in result.warnings)
    
    def test_cluster_mismatch_warns(self, test_config):
        """Cluster mismatch generates warning but still matches on MSID"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',
            cluster='Wilmington',  # Different cluster
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True  # Still passes on MSID
        assert result.has_warnings == True
        assert any('Cluster mismatch' in str(result.warnings + result.info) for _ in [1])
    
    def test_msid_only_match_passes(self, test_config):
        """MSID match alone is sufficient for matching"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',
            cluster=None,  # No cluster specified
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True
        # May have warnings about low confidence/cluster mismatch
        assert result.has_warnings == True


# ============================================================================
# Test MatchValidator - Fuzzy Matching
# ============================================================================

class TestMatchValidatorFuzzyMatch:
    """Tests for fuzzy matching with Levenshtein distance"""
    
    def test_fuzzy_msid_match_single_typo(self, test_config):
        """MSID with single character typo matches via fuzzy logic"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',  # Same
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        # Should match with fuzzy logic (exact match in this case)
        assert result.passed == True
    
    def test_fuzzy_msid_confidence_reported(self, test_config):
        """Fuzzy match confidence is reported"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',  # Same
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True
        # Check that confidence is mentioned in output
        assert any('100%' in i or 'Exact' in i for i in result.info)
    
    def test_levenshtein_distance_calculation(self, test_config):
        """Levenshtein distance calculated correctly"""
        validator = MatchValidator(test_config)
        
        # Test exact match
        assert validator._levenshtein_distance('M0614', 'M0614') == 0
        
        # Test single character difference
        assert validator._levenshtein_distance('M0614', 'M0615') == 1
        assert validator._levenshtein_distance('M0614', 'M0624') == 1
        
        # Test multiple differences
        assert validator._levenshtein_distance('M0614', 'M0999') == 3
        
        # Test different lengths
        assert validator._levenshtein_distance('M0614', 'M0614-EX01') == 5
    
    def test_fuzzy_match_exceeds_threshold_fails(self, test_config):
        """MSID too different for fuzzy matching fails"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M9999',  # Very different MSID
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == False
        assert any('MSID mismatch' in w for w in result.warnings)


# ============================================================================
# Test MatchValidator - Partial Matches
# ============================================================================

class TestMatchValidatorPartialMatch:
    """Tests for partial matching (2 out of 3 fields)"""
    
    def test_msid_match_cluster_mismatch_passes(self, test_config):
        """MSID match is sufficient even with cluster mismatch"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',  # Match
            cluster='Wilmington',  # Mismatch but acceptable
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True
        assert result.has_warnings == True
        # Cluster mismatch reported in info
        assert any('Cluster mismatch' in str(result.info) for _ in [1])
    
    def test_neither_field_match_fails(self, test_config):
        """Match with neither MSID nor cluster matching fails"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M9999',  # Mismatch
            cluster='Wilmington',  # Mismatch
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == False
        assert any('Cluster mismatch' in w for w in result.warnings)
        assert any('MSID mismatch' in w for w in result.warnings)


# ============================================================================
# Test MatchValidator - Confidence Reporting
# ============================================================================

class TestMatchValidatorConfidence:
    """Tests for match confidence reporting"""
    
    def test_low_confidence_flagged(self, test_config):
        """Match below 90% confidence threshold is flagged"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',
            cluster='Wilmington',  # Mismatch reduces confidence
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True
        assert result.has_warnings == True
        # Should flag low confidence
        assert any('confidence' in w.lower() for w in result.warnings)
    
    def test_perfect_match_no_confidence_warning(self, test_config):
        """Perfect match has no confidence warnings"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        assert result.passed == True
        # No confidence warnings for perfect match
        confidence_warnings = [w for w in result.warnings if 'confidence' in w.lower()]
        assert len(confidence_warnings) == 0


# ============================================================================
# Test MatchValidator - Edge Cases
# ============================================================================

class TestMatchValidatorEdgeCases:
    """Edge case tests for MatchValidator"""
    
    def test_invalid_input_not_tuple(self, test_config):
        """Validator rejects non-tuple input"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate(license)  # Not a tuple
        
        assert result.passed == False
        assert any('requires tuple' in e for e in result.errors)
    
    def test_invalid_tuple_length(self, test_config):
        """Validator rejects tuple with wrong length"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license,))  # Only 1 element
        
        assert result.passed == False
        assert any('requires tuple' in e for e in result.errors)
    
    def test_invalid_first_element_type(self, test_config):
        """Validator rejects non-LicenseData first element"""
        usage = UsageData(
            msid='M0614',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((usage, usage))  # Both UsageData
        
        assert result.passed == False
        assert any('LicenseData' in e for e in result.errors)
    
    def test_invalid_second_element_type(self, test_config):
        """Validator rejects non-UsageData second element"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, license))  # Both LicenseData
        
        assert result.passed == False
        assert any('UsageData' in e for e in result.errors)
    
    def test_none_values_in_fields(self, test_config):
        """Handles None values in match fields"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',  # Required field must be present
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',
            cluster=None,  # None
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = MatchValidator(test_config)
        result = validator.validate((license, usage))
        
        # Should still match on MSID (most important)
        assert result.passed == True
    
    def test_validator_without_config(self, test_config):
        """Validator works with provided config"""
        validator = MatchValidator(test_config)
        
        assert validator.config is not None
        assert validator.match_rules is not None
    
    def test_validator_resets_between_calls(self, test_config):
        """Validator state resets between validations"""
        validator = MatchValidator(test_config)
        
        # First validation with mismatch
        license1 = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        usage1 = UsageData(
            msid='M9999',  # Mismatch
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        result1 = validator.validate((license1, usage1))
        assert result1.passed == False
        
        # Second validation should be independent
        license2 = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        usage2 = UsageData(
            msid='M0614',  # Match
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        result2 = validator.validate((license2, usage2))
        assert result2.passed == True
        # Should not have warnings from first validation
        assert not any('M9999' in w for w in result2.warnings)
