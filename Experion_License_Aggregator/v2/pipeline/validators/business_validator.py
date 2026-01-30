"""
Business rule validator for V2.0 pipeline.

Applies domain-specific validation rules from validation_rules.yaml.
"""

from datetime import datetime, timedelta
from typing import Optional
from v2.pipeline.validators.base_validator import BaseValidator, ValidationResult
from v2.models.license import LicenseData
from v2.models.usage import UsageData
from v2.core.config import Config


class BusinessValidator(BaseValidator):
    """
    Validates data against business rules from configuration.
    
    Checks:
    - Customer name contains expected patterns (Marathon, MPC)
    - License age is within acceptable range (< 2 years)
    - Release version is in known list
    - Licensed quantities are within typical ranges
    - Usage doesn't exceed licensed (when applicable)
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize business validator with configuration.
        
        Args:
            config: Configuration object (loads from default path if None)
        """
        super().__init__()
        self.config = config or Config()
        
        # Load business rules from config
        self.business_rules = self.config.validation_rules.get('business', {})
    
    def validate(self, data: LicenseData) -> ValidationResult:
        """
        Validate LicenseData against business rules.
        
        Args:
            data: LicenseData instance
            
        Returns:
            ValidationResult with business rule violations
        """
        self.reset()
        
        if not isinstance(data, LicenseData):
            self._add_error(f"BusinessValidator only supports LicenseData, got {type(data).__name__}")
            return self._create_result(passed=False)
        
        # Apply business rules
        self._validate_customer_name(data)
        self._validate_license_age(data)
        self._validate_release_version(data)
        self._validate_licensed_quantities(data)
        
        # Business validation passes if no errors (warnings are acceptable)
        passed = len(self._errors) == 0
        return self._create_result(passed)
    
    def validate_with_usage(self, license: LicenseData, usage: UsageData) -> ValidationResult:
        """
        Validate LicenseData with corresponding UsageData.
        
        Checks utilization rules (usage vs licensed).
        
        Args:
            license: LicenseData instance
            usage: UsageData instance for same system
            
        Returns:
            ValidationResult with utilization checks
        """
        self.reset()
        
        # First run standard business validation
        standard_result = self.validate(license)
        
        # Copy errors/warnings from standard validation
        self._errors.extend(standard_result.errors)
        self._warnings.extend(standard_result.warnings)
        self._info.extend(standard_result.info)
        
        # Add utilization validation
        self._validate_utilization(license, usage)
        
        passed = len(self._errors) == 0
        return self._create_result(passed)
    
    def _validate_customer_name(self, license: LicenseData) -> None:
        """
        Validate customer name contains expected patterns.
        
        Rule: customer_name from config
        - Must contain 'Marathon' or 'MPC'
        - Severity: warning
        
        Args:
            license: LicenseData to check
        """
        customer_rule = self.business_rules.get('customer_name', {})
        
        if not license.customer:
            self._add_warning("Customer name not specified")
            return
        
        patterns = customer_rule.get('patterns', ['Marathon', 'MPC'])
        customer_lower = license.customer.lower()
        
        if not any(pattern.lower() in customer_lower for pattern in patterns):
            message = customer_rule.get('message', 
                                       f"Customer name should contain {' or '.join(patterns)}")
            self._add_warning(f"{message}: '{license.customer}'")
        else:
            self._add_info(f"Valid customer: {license.customer}")
    
    def _validate_license_age(self, license: LicenseData) -> None:
        """
        Validate license age is within acceptable range.
        
        Rule: license_age from config
        - Max age: 730 days (2 years)
        - Severity: warning
        
        Args:
            license: LicenseData to check
        """
        age_rule = self.business_rules.get('license_age', {})
        
        if not license.license_date:
            self._add_info("License date not available for age check")
            return
        
        max_age_days = age_rule.get('threshold', 730)
        age = datetime.now() - license.license_date
        
        if age.days > max_age_days:
            message = age_rule.get('message', f"License older than {max_age_days} days")
            self._add_warning(f"{message}: {age.days} days old")
        else:
            self._add_info(f"License age acceptable: {age.days} days")
    
    def _validate_release_version(self, license: LicenseData) -> None:
        """
        Validate release version against known releases.
        
        Rule: release_version from config
        - Known releases: R410, R431, R500, R510, R520, R51X, R52X
        - Severity: info
        
        Args:
            license: LicenseData to check
        """
        release_rule = self.business_rules.get('release_version', {})
        
        if not license.release:
            self._add_info("Release version not specified")
            return
        
        valid_releases = release_rule.get('valid_releases', [])
        release = license.release.upper()
        
        # Check exact match or pattern match (R51X matches R510, R511, etc.)
        is_valid = False
        for valid_release in valid_releases:
            if 'X' in valid_release:
                # Pattern match: R51X matches R510, R511, R512, etc.
                pattern = valid_release.replace('X', '')
                if release.startswith(pattern):
                    is_valid = True
                    break
            elif release == valid_release:
                is_valid = True
                break
        
        if not is_valid:
            message = release_rule.get('message', "Release not in known list")
            self._add_info(f"{message}: {license.release}")
        else:
            self._add_info(f"Known release: {license.release}")
    
    def _validate_licensed_quantities(self, license: LicenseData) -> None:
        """
        Validate licensed quantities are within typical ranges.
        
        Rule: licensed_quantities from config
        - PROCESSPOINTS: 50-50,000
        - SCADAPOINTS: 0-100,000
        - DIRECTSTATIONS: 1-50
        - Severity: warning
        
        Args:
            license: LicenseData to check
        """
        quantity_rules = self.business_rules.get('licensed_quantities', {})
        
        for license_type, quantity in license.licensed.items():
            rule = quantity_rules.get(license_type, {})
            
            if not rule:
                continue
            
            min_val = rule.get('min', 0)
            max_val = rule.get('max', float('inf'))
            
            if quantity < min_val or quantity > max_val:
                message = rule.get('message', f"Quantity outside typical range")
                self._add_warning(
                    f"{license_type}: {quantity} outside range [{min_val}-{max_val}] - {message}"
                )
            else:
                self._add_info(f"{license_type}: {quantity} within acceptable range")
    
    def _validate_utilization(self, license: LicenseData, usage: UsageData) -> None:
        """
        Validate usage doesn't exceed licensed quantity.
        
        Rule: utilization from config
        - Usage must not exceed licensed
        - Severity: warning
        
        Args:
            license: LicenseData with licensed quantities
            usage: UsageData with used quantities
        """
        utilization_rule = self.business_rules.get('utilization', {})
        
        # Get licensed quantity for this license type
        licensed_qty = license.licensed.get(usage.license_type, 0)
        used_qty = usage.used_quantity
        
        if used_qty > licensed_qty:
            message = utilization_rule.get('message', 
                                          "Usage exceeds licensed quantity")
            self._add_warning(
                f"{usage.license_type}: Used {used_qty} > Licensed {licensed_qty} - {message}"
            )
        else:
            utilization_pct = (used_qty / licensed_qty * 100) if licensed_qty > 0 else 0
            self._add_info(
                f"{usage.license_type}: {utilization_pct:.1f}% utilized "
                f"({used_qty}/{licensed_qty})"
            )
