"""
Tests for business rule validator.

Tests BusinessValidator with configuration-based rules.
"""

import pytest
from datetime import datetime, date, timedelta
from pathlib import Path

from v2.pipeline.validators import BusinessValidator
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
# Test BusinessValidator - Customer Name
# ============================================================================

class TestBusinessValidatorCustomerName:
    """Tests for customer name validation"""
    
    def test_valid_customer_with_marathon(self, test_config):
        """Customer containing 'Marathon' passes"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            customer='Marathon Petroleum Company',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('Valid customer' in i for i in result.info)
    
    def test_valid_customer_with_mpc(self, test_config):
        """Customer containing 'MPC' passes"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            customer='MPC Corporation',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
    
    def test_invalid_customer_name_warns(self, test_config):
        """Customer without Marathon/MPC generates warning"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            customer='Other Company',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True  # Warning doesn't fail validation
        assert result.has_warnings == True
        assert any('should contain' in w for w in result.warnings)
    
    def test_missing_customer_warns(self, test_config):
        """Missing customer generates warning"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('not specified' in w for w in result.warnings)
    
    def test_customer_name_case_insensitive(self, test_config):
        """Customer check is case insensitive"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            customer='marathon petroleum',  # lowercase
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('Valid customer' in i for i in result.info)


# ============================================================================
# Test BusinessValidator - License Age
# ============================================================================

class TestBusinessValidatorLicenseAge:
    """Tests for license age validation"""
    
    def test_recent_license_passes(self, test_config):
        """License less than 2 years old passes"""
        recent_date = datetime.now() - timedelta(days=365)  # 1 year old
        
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            license_date=recent_date,
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('age acceptable' in i for i in result.info)
    
    def test_old_license_warns(self, test_config):
        """License older than 2 years generates warning"""
        old_date = datetime.now() - timedelta(days=800)  # > 2 years
        
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            license_date=old_date,
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True  # Warning doesn't fail
        assert result.has_warnings == True
        assert any('older than' in w.lower() for w in result.warnings)
    
    def test_missing_license_date_info(self, test_config):
        """Missing license date generates info message"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('not available' in i for i in result.info)


# ============================================================================
# Test BusinessValidator - Release Version
# ============================================================================

class TestBusinessValidatorReleaseVersion:
    """Tests for release version validation"""
    
    def test_known_release_exact_match(self, test_config):
        """Known release (exact match) passes"""
        for release in ['R410', 'R431', 'R500', 'R510', 'R520']:
            license = LicenseData(
                msid='M0614',
                system_number='60806',
                cluster='Carson',
                release=release,
                licensed={'PROCESSPOINTS': 4750}
            )
            
            validator = BusinessValidator(test_config)
            result = validator.validate(license)
            
            assert result.passed == True
            assert any('Known release' in i for i in result.info)
    
    def test_known_release_pattern_match(self, test_config):
        """Release matching pattern (R51X) passes"""
        for release in ['R510', 'R511', 'R512', 'R513']:
            license = LicenseData(
                msid='M0614',
                system_number='60806',
                cluster='Carson',
                release=release,
                licensed={'PROCESSPOINTS': 4750}
            )
            
            validator = BusinessValidator(test_config)
            result = validator.validate(license)
            
            assert result.passed == True
    
    def test_unknown_release_info(self, test_config):
        """Unknown release generates info message"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R999',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('not in known list' in i for i in result.info)
    
    def test_missing_release_info(self, test_config):
        """Missing release generates info message"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('not specified' in i for i in result.info)


# ============================================================================
# Test BusinessValidator - Licensed Quantities
# ============================================================================

class TestBusinessValidatorLicensedQuantities:
    """Tests for licensed quantity validation"""
    
    def test_processpoints_in_range(self, test_config):
        """Process points within 50-50,000 passes"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}  # Within range
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('within acceptable range' in i for i in result.info)
    
    def test_processpoints_too_low_warns(self, test_config):
        """Process points below 50 generates warning"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 25}  # Too low
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert result.has_warnings == True
        assert any('outside range' in w for w in result.warnings)
    
    def test_processpoints_too_high_warns(self, test_config):
        """Process points above 50,000 generates warning"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 75000}  # Too high
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert result.has_warnings == True
    
    def test_directstations_in_range(self, test_config):
        """Direct stations within 1-50 passes"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'DIRECTSTATIONS': 6}
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
    
    def test_directstations_out_of_range_warns(self, test_config):
        """Direct stations outside 1-50 generates warning"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'DIRECTSTATIONS': 100}  # Too high
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert result.has_warnings == True
    
    def test_multiple_quantities_checked(self, test_config):
        """Multiple license types are all checked"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={
                'PROCESSPOINTS': 4750,  # OK
                'SCADAPOINTS': 1500,    # OK
                'DIRECTSTATIONS': 200   # Too high
            }
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(license)
        
        assert result.passed == True
        assert result.has_warnings == True
        # Should have warnings for DIRECTSTATIONS but not others
        assert any('DIRECTSTATIONS' in w for w in result.warnings)


# ============================================================================
# Test BusinessValidator - Utilization
# ============================================================================

class TestBusinessValidatorUtilization:
    """Tests for utilization validation (with UsageData)"""
    
    def test_usage_within_licensed(self, test_config):
        """Usage within licensed quantity passes"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate_with_usage(license, usage)
        
        assert result.passed == True
        assert any('utilized' in i for i in result.info)
    
    def test_usage_exceeds_licensed_warns(self, test_config):
        """Usage exceeding licensed generates warning"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=150  # Exceeds licensed
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate_with_usage(license, usage)
        
        assert result.passed == True  # Warning doesn't fail
        assert result.has_warnings == True
        assert any('exceeds' in w.lower() for w in result.warnings)
    
    def test_usage_at_100_percent(self, test_config):
        """Usage at 100% utilization passes with info"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=100
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate_with_usage(license, usage)
        
        assert result.passed == True
        assert any('100.0%' in i for i in result.info)


# ============================================================================
# Test BusinessValidator - Edge Cases
# ============================================================================

class TestBusinessValidatorEdgeCases:
    """Edge case tests for BusinessValidator"""
    
    def test_validates_only_license_data(self, test_config):
        """BusinessValidator rejects non-LicenseData"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=100
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate(usage)
        
        assert result.passed == False
        assert any('only supports LicenseData' in e for e in result.errors)
    
    def test_validator_with_no_config(self, test_config):
        """Validator works without explicit config"""
        validator = BusinessValidator(test_config)
        
        assert validator.config is not None
        assert validator.business_rules is not None
    
    def test_validator_resets_between_calls(self, test_config):
        """Validator state resets between validations"""
        validator = BusinessValidator(test_config)
        
        # First validation with warning
        bad_license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            customer='Other Company',  # Generates warning
            licensed={'PROCESSPOINTS': 4750}
        )
        result1 = validator.validate(bad_license)
        assert result1.has_warnings == True
        
        # Second validation should be independent
        good_license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            customer='Marathon Petroleum',
            licensed={'PROCESSPOINTS': 4750}
        )
        result2 = validator.validate(good_license)
        # Should not have customer warning from first validation
        assert not any('should contain' in w for w in result2.warnings)
    
    def test_combined_validation_accumulates_issues(self, test_config):
        """validate_with_usage includes both standard and utilization checks"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            customer='Other Company',  # Warning
            licensed={'PROCESSPOINTS': 100}
        )
        
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=150  # Warning (exceeds)
        )
        
        validator = BusinessValidator(test_config)
        result = validator.validate_with_usage(license, usage)
        
        assert result.passed == True
        assert result.has_warnings == True
        # Should have warnings from both checks
        assert len(result.warnings) >= 2
