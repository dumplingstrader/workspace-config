"""
Schema validator for V2.0 pipeline.

Validates LicenseData and UsageData against required schema.
"""

import re
from typing import Union
from v2.pipeline.validators.base_validator import BaseValidator, ValidationResult
from v2.models.license import LicenseData
from v2.models.usage import UsageData


class SchemaValidator(BaseValidator):
    """
    Validates data objects against schema requirements.
    
    Checks:
    - Required fields are present and non-empty
    - Field formats are valid (MSID pattern, dates, etc.)
    - Numeric values are in valid ranges
    - Enumerations match expected values
    """
    
    # MSID pattern: M followed by digits, optionally with -EX## suffix
    MSID_PATTERN = re.compile(r'^M\d+(-EX\d+)?$', re.IGNORECASE)
    
    # System number pattern: 5 digits
    SYSTEM_NUMBER_PATTERN = re.compile(r'^\d{5}$')
    
    # Valid clusters
    VALID_CLUSTERS = ['Carson', 'Wilmington', 'Salt Lake City']
    
    def validate(self, data: Union[LicenseData, UsageData]) -> ValidationResult:
        """
        Validate LicenseData or UsageData object.
        
        Args:
            data: LicenseData or UsageData instance
            
        Returns:
            ValidationResult with pass/fail status
        """
        self.reset()
        
        if isinstance(data, LicenseData):
            self._validate_license_data(data)
        elif isinstance(data, UsageData):
            self._validate_usage_data(data)
        else:
            self._add_error(f"Unsupported data type: {type(data).__name__}")
            return self._create_result(passed=False)
        
        # Validation passes if no errors
        passed = len(self._errors) == 0
        return self._create_result(passed)
    
    def _validate_license_data(self, license: LicenseData) -> None:
        """
        Validate LicenseData fields.
        
        Args:
            license: LicenseData to validate
        """
        # Required string fields
        self._validate_msid(license.msid)
        self._validate_system_number(license.system_number)
        
        # Optional but important fields
        if license.cluster:
            self._validate_cluster(license.cluster)
        else:
            self._add_warning("Cluster not specified")
        
        if not license.release:
            self._add_warning("Release not specified")
        
        if not license.product:
            self._add_warning("Product not specified")
        
        if not license.customer:
            self._add_warning("Customer not specified")
        
        # Validate license date if present
        if license.license_date:
            self._add_info(f"License date: {license.license_date}")
        else:
            self._add_warning("License date not specified")
        
        # Validate file version
        if license.file_version is not None:
            if license.file_version < 0:
                self._add_error(f"Invalid file version: {license.file_version}")
            elif license.file_version < 40:
                self._add_warning(f"Old file version: {license.file_version}")
        
        # Validate licensed quantities
        if not license.licensed:
            self._add_error("No licensed quantities found")
        else:
            self._validate_quantities(license.licensed, "licensed")
        
        # Validate file path
        if not license.file_path:
            self._add_warning("File path not specified")
    
    def _validate_usage_data(self, usage: UsageData) -> None:
        """
        Validate UsageData fields.
        
        Args:
            usage: UsageData to validate
        """
        # Required fields
        self._validate_msid(usage.msid)
        
        if not usage.license_type:
            self._add_error("License type is required")
        else:
            self._add_info(f"License type: {usage.license_type}")
        
        # Validate used quantity
        if usage.used_quantity < 0:
            self._add_error(f"Used quantity cannot be negative: {usage.used_quantity}")
        elif usage.used_quantity == 0:
            self._add_warning(f"Used quantity is zero for {usage.license_type}")
        
        # Optional fields
        if usage.cluster:
            self._validate_cluster(usage.cluster)
        else:
            self._add_warning("Cluster not specified")
        
        if not usage.file_path:
            self._add_warning("File path not specified")
    
    def _validate_msid(self, msid: str) -> None:
        """
        Validate MSID format.
        
        Args:
            msid: MSID to validate
        """
        if not msid:
            self._add_error("MSID is required")
            return
        
        if msid.upper() == 'UNKNOWN':
            self._add_error("MSID cannot be 'Unknown'")
            return
        
        if not self.MSID_PATTERN.match(msid):
            self._add_error(
                f"Invalid MSID format: '{msid}' "
                f"(expected M#### or M####-EX##)"
            )
        else:
            self._add_info(f"Valid MSID: {msid}")
    
    def _validate_system_number(self, system_number: str) -> None:
        """
        Validate system number format.
        
        Args:
            system_number: System number to validate
        """
        if not system_number:
            self._add_warning("System number not specified")
            return
        
        if system_number == '00000':
            self._add_warning("System number is default value (00000)")
            return
        
        if not self.SYSTEM_NUMBER_PATTERN.match(system_number):
            self._add_error(
                f"Invalid system number format: '{system_number}' "
                f"(expected 5 digits)"
            )
        else:
            self._add_info(f"System number: {system_number}")
    
    def _validate_cluster(self, cluster: str) -> None:
        """
        Validate cluster name.
        
        Args:
            cluster: Cluster name to validate
        """
        if cluster not in self.VALID_CLUSTERS:
            self._add_warning(
                f"Unknown cluster: '{cluster}' "
                f"(expected: {', '.join(self.VALID_CLUSTERS)})"
            )
        else:
            self._add_info(f"Cluster: {cluster}")
    
    def _validate_quantities(self, quantities: dict, label: str) -> None:
        """
        Validate license quantity dictionary.
        
        Args:
            quantities: Dictionary of license_type -> quantity
            label: Label for error messages
        """
        if not quantities:
            self._add_error(f"Empty {label} quantities")
            return
        
        for license_type, quantity in quantities.items():
            if not license_type:
                self._add_error(f"Empty license type in {label}")
                continue
            
            if not isinstance(quantity, (int, float)):
                self._add_error(
                    f"Invalid quantity type for {license_type}: "
                    f"{type(quantity).__name__}"
                )
                continue
            
            if quantity < 0:
                self._add_error(
                    f"Negative {label} quantity for {license_type}: {quantity}"
                )
            elif quantity == 0:
                self._add_warning(
                    f"Zero {label} quantity for {license_type}"
                )
