"""
Tests for validation layer.

Tests BaseValidator, ValidationResult, and SchemaValidator.
"""

import pytest
from datetime import datetime, date
from pathlib import Path

from v2.pipeline.validators import BaseValidator, ValidationResult, SchemaValidator
from v2.models.license import LicenseData
from v2.models.usage import UsageData


# ============================================================================
# Test ValidationResult
# ============================================================================

class TestValidationResult:
    """Tests for ValidationResult dataclass"""
    
    def test_successful_result(self):
        """Successful result with no issues"""
        result = ValidationResult(passed=True)
        
        assert result.passed == True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0
        assert result.has_errors == False
        assert result.has_warnings == False
        assert result.issue_count == 0
    
    def test_failed_result_with_errors(self):
        """Failed result must have errors"""
        result = ValidationResult(
            passed=False,
            errors=["Error 1", "Error 2"]
        )
        
        assert result.passed == False
        assert len(result.errors) == 2
        assert result.has_errors == True
        assert result.issue_count == 2
    
    def test_result_with_warnings(self):
        """Result can have warnings even if passed"""
        result = ValidationResult(
            passed=True,
            warnings=["Warning 1"]
        )
        
        assert result.passed == True
        assert result.has_warnings == True
        assert result.issue_count == 1
    
    def test_result_consistency_errors_require_failed(self):
        """Result with errors cannot be passed"""
        with pytest.raises(ValueError) as exc_info:
            ValidationResult(passed=True, errors=["Some error"])
        
        assert "cannot have passed=True" in str(exc_info.value)
    
    def test_result_consistency_failed_requires_errors(self):
        """Failed result must have at least one error"""
        with pytest.raises(ValueError) as exc_info:
            ValidationResult(passed=False)
        
        assert "must have at least one error" in str(exc_info.value)
    
    def test_result_to_dict(self):
        """Serialize result to dictionary"""
        result = ValidationResult(
            passed=True,
            warnings=["Warning"],
            validator_name="TestValidator"
        )
        
        d = result.to_dict()
        assert d['passed'] == True
        assert d['warnings'] == ["Warning"]
        assert d['validator_name'] == "TestValidator"
        assert 'validation_time' in d


# ============================================================================
# Test BaseValidator
# ============================================================================

class ConcreteValidator(BaseValidator):
    """Concrete validator for testing BaseValidator"""
    
    def validate(self, data):
        """Simple validation for testing"""
        self.reset()
        
        if data == "error":
            self._add_error("This is an error")
        elif data == "warning":
            self._add_warning("This is a warning")
        elif data == "info":
            self._add_info("This is info")
        
        passed = len(self._errors) == 0
        return self._create_result(passed)


class TestBaseValidator:
    """Tests for BaseValidator abstract class"""
    
    def test_validator_initialization(self):
        """Validator starts with empty state"""
        validator = ConcreteValidator()
        
        assert len(validator._errors) == 0
        assert len(validator._warnings) == 0
        assert len(validator._info) == 0
    
    def test_add_error(self):
        """Add error message"""
        validator = ConcreteValidator()
        result = validator.validate("error")
        
        assert result.passed == False
        assert len(result.errors) == 1
        assert "[ERROR]" in result.errors[0]
    
    def test_add_warning(self):
        """Add warning message"""
        validator = ConcreteValidator()
        result = validator.validate("warning")
        
        assert result.passed == True
        assert len(result.warnings) == 1
        assert "[WARNING]" in result.warnings[0]
    
    def test_add_info(self):
        """Add info message"""
        validator = ConcreteValidator()
        result = validator.validate("info")
        
        assert result.passed == True
        assert len(result.info) == 1
        assert "[INFO]" in result.info[0]
    
    def test_reset_clears_state(self):
        """Reset clears accumulated messages"""
        validator = ConcreteValidator()
        
        # First validation
        validator.validate("error")
        
        # Second validation should not have first error
        result = validator.validate("warning")
        assert len(result.errors) == 0
        assert len(result.warnings) == 1


# ============================================================================
# Test SchemaValidator - LicenseData
# ============================================================================

class TestSchemaValidatorLicenseData:
    """Tests for SchemaValidator with LicenseData"""
    
    def test_valid_license_data(self):
        """Valid license passes validation"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            release='R520',
            product='Experion PKS',
            customer='Marathon Petroleum',
            license_date=date(2025, 1, 1),
            file_version=40,
            cluster='Carson',
            licensed={'PROCESSPOINTS': 4750, 'SCADAPOINTS': 1500},
            file_path='test.xml'
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == True
        assert len(result.errors) == 0
    
    def test_invalid_msid_format(self):
        """Invalid MSID format fails validation"""
        license = LicenseData(
            msid='INVALID',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == False
        assert any('Invalid MSID format' in e for e in result.errors)
    
    def test_unknown_msid_fails(self):
        """MSID 'Unknown' fails validation - caught at model construction"""
        # LicenseData validates MSID in __post_init__, so 'Unknown' raises ValidationError
        from v2.models.license import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            license = LicenseData(
                msid='Unknown',
                system_number='60806',
                cluster='Carson',
                release='R520',
                licensed={'PROCESSPOINTS': 100}
            )
        
        assert "Invalid MSID: 'Unknown'" in str(exc_info.value)
    
    def test_msid_with_extension(self):
        """MSID with -EX## extension is valid"""
        license = LicenseData(
            msid='M13287-EX10',
            system_number='12345',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == True
    
    def test_invalid_system_number_format(self):
        """Invalid system number format fails"""
        license = LicenseData(
            msid='M0614',
            system_number='123',  # Too short
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == False
        assert any('Invalid system number format' in e for e in result.errors)
    
    def test_empty_licensed_quantities_fails(self):
        """Empty licensed dict fails validation"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={}
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == False
        assert any('No licensed quantities' in e for e in result.errors)
    
    def test_negative_quantity_fails(self):
        """Negative licensed quantity fails"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': -100}
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == False
        assert any('Negative' in e for e in result.errors)
    
    def test_missing_optional_fields_warns(self):
        """Missing optional fields generate warnings"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == True
        assert result.has_warnings == True
        # Should warn about missing customer, product left as default, no license_date, etc.
        assert any('not specified' in w for w in result.warnings)
    
    def test_unknown_cluster_warns(self):
        """Unknown cluster generates warning"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Unknown Site',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        validator = SchemaValidator()
        result = validator.validate(license)
        
        assert result.passed == True
        assert any('Unknown cluster' in w for w in result.warnings)
    
    def test_valid_clusters(self):
        """Valid cluster names pass without warnings"""
        for cluster in ['Carson', 'Wilmington', 'Salt Lake City']:
            license = LicenseData(
                msid='M0614',
                system_number='60806',
                cluster=cluster,
                licensed={'PROCESSPOINTS': 100},
                release='R520',
                product='PKS',
                customer='Test',
                license_date=date(2025, 1, 1),
                file_path='test.xml'
            )
            
            validator = SchemaValidator()
            result = validator.validate(license)
            
            assert result.passed == True
            # Should have info about cluster but no warnings about it
            assert any(cluster in i for i in result.info)


# ============================================================================
# Test SchemaValidator - UsageData
# ============================================================================

class TestSchemaValidatorUsageData:
    """Tests for SchemaValidator with UsageData"""
    
    def test_valid_usage_data(self):
        """Valid usage passes validation"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=108,
            cluster='Carson',
            file_path='test.csv'
        )
        
        validator = SchemaValidator()
        result = validator.validate(usage)
        
        assert result.passed == True
        assert len(result.errors) == 0
    
    def test_missing_msid_fails(self):
        """Missing MSID fails validation - caught at model construction"""
        # UsageData validates in __post_init__, so empty MSID raises ValidationError
        from v2.models.license import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            usage = UsageData(
                msid='',
                license_type='PROCESSPOINTS',
                used_quantity=108
            )
        
        assert 'MSID required' in str(exc_info.value)
    
    def test_invalid_msid_format_fails(self):
        """Invalid MSID format fails"""
        usage = UsageData(
            msid='BAD',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = SchemaValidator()
        result = validator.validate(usage)
        
        assert result.passed == False
        assert any('Invalid MSID format' in e for e in result.errors)
    
    def test_negative_used_quantity_fails(self):
        """Negative used quantity fails - caught at model construction"""
        # UsageData validates in __post_init__, so negative quantity raises ValidationError
        from v2.models.license import ValidationError
        
        with pytest.raises(ValidationError) as exc_info:
            usage = UsageData(
                msid='M0614',
                license_type='PROCESSPOINTS',
                used_quantity=-10
            )
        
        assert 'cannot be negative' in str(exc_info.value)
    
    def test_zero_used_quantity_warns(self):
        """Zero used quantity generates warning"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=0
        )
        
        validator = SchemaValidator()
        result = validator.validate(usage)
        
        assert result.passed == True
        assert any('Used quantity is zero' in w for w in result.warnings)
    
    def test_missing_optional_fields_warns(self):
        """Missing optional fields generate warnings"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        validator = SchemaValidator()
        result = validator.validate(usage)
        
        assert result.passed == True
        assert result.has_warnings == True


# ============================================================================
# Test SchemaValidator - Edge Cases
# ============================================================================

class TestSchemaValidatorEdgeCases:
    """Edge case tests for SchemaValidator"""
    
    def test_unsupported_data_type_fails(self):
        """Unsupported data type fails validation"""
        validator = SchemaValidator()
        result = validator.validate("not a valid type")
        
        assert result.passed == False
        assert any('Unsupported data type' in e for e in result.errors)
    
    def test_validator_reset_between_calls(self):
        """Validator resets state between validate calls"""
        validator = SchemaValidator()
        
        # First validation with error
        bad_license = LicenseData(
            msid='INVALID',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        result1 = validator.validate(bad_license)
        assert result1.passed == False
        
        # Second validation should be independent
        good_license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        result2 = validator.validate(good_license)
        assert result2.passed == True
        assert len(result2.errors) == 0  # No carryover from first validation
    
    def test_validator_name_in_result(self):
        """Validator name is set in result"""
        validator = SchemaValidator()
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 100}
        )
        
        result = validator.validate(license)
        assert result.validator_name == 'SchemaValidator'
