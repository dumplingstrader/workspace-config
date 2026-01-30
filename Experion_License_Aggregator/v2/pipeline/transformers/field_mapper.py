"""
Field Mapper - License type normalization and field mapping.

This module handles the mapping of XML license field names to CSV usage field names,
including fallback chains for fields that may have multiple possible names.

Key Mappings:
- DIRECTSTATIONS (XML) → CONSOLE_STATIONS (CSV)
- STATIONS → STATIONS, fallback to MULTISTATIONS, DIRECTSTATIONS
- Most fields have 1:1 mappings

The field_mappings.yaml configuration drives all mapping logic.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Union

from v2.core.config import Config


@dataclass
class MappingResult:
    """
    Result of a field mapping operation.
    
    Attributes:
        target_field: The mapped field name (from CSV/usage side)
        fallback_used: True if fallback chain was used
        fallback_field: Which fallback field was actually found (if any)
        available: Whether the target field or fallback was found
    
    Examples:
        >>> result = mapper.get_target_field('DIRECTSTATIONS')
        >>> print(result.target_field)
        CONSOLE_STATIONS
        >>> print(result.fallback_used)
        False
    """
    target_field: str
    fallback_used: bool = False
    fallback_field: Optional[str] = None
    available: bool = True


class FieldMapper:
    """
    Maps XML license fields to CSV usage fields with fallback support.
    
    Handles naming differences between data sources:
    - XML files use 'DIRECTSTATIONS'
    - CSV files use 'CONSOLE_STATIONS'
    - Some fields have fallback chains (STATIONS → MULTISTATIONS → DIRECTSTATIONS)
    
    The field_mappings.yaml configuration defines all mappings and fallback chains.
    
    Examples:
        >>> mapper = FieldMapper(config)
        >>> result = mapper.get_target_field('DIRECTSTATIONS')
        >>> assert result.target_field == 'CONSOLE_STATIONS'
        
        >>> # Fallback chain
        >>> result = mapper.get_target_field('STATIONS')
        >>> # If STATIONS not found, tries MULTISTATIONS, then DIRECTSTATIONS
    """
    
    def __init__(self, config: Config):
        """
        Initialize field mapper with configuration.
        
        Args:
            config: Config instance with field_mappings.yaml loaded
        
        Raises:
            KeyError: If field_mappings.license_to_usage not in config
        """
        self.config = config
        
        # Load field mappings from config
        if not hasattr(config, 'field_mappings') or 'license_to_usage' not in config.field_mappings:
            raise KeyError("Config must contain field_mappings.license_to_usage")
        
        self.mappings = config.field_mappings['license_to_usage']
    
    def get_target_field(
        self, 
        license_field: str,
        usage_data: Optional[Dict[str, Any]] = None
    ) -> MappingResult:
        """
        Map license field name to usage field name with fallback support.
        
        Args:
            license_field: Field name from XML license (e.g., 'DIRECTSTATIONS')
            usage_data: Optional usage data dict to check for field availability
        
        Returns:
            MappingResult with target field and fallback information
        
        Examples:
            >>> # Simple 1:1 mapping
            >>> result = mapper.get_target_field('PROCESSPOINTS')
            >>> assert result.target_field == 'PROCESSPOINTS'
            
            >>> # Name variation
            >>> result = mapper.get_target_field('DIRECTSTATIONS')
            >>> assert result.target_field == 'CONSOLE_STATIONS'
            
            >>> # Fallback chain (with usage data)
            >>> usage = {'MULTISTATIONS': 10}  # STATIONS not present
            >>> result = mapper.get_target_field('STATIONS', usage)
            >>> assert result.target_field == 'MULTISTATIONS'
            >>> assert result.fallback_used == True
        """
        if license_field not in self.mappings:
            # No mapping defined - use field as-is
            return MappingResult(
                target_field=license_field,
                available=usage_data is None or license_field in usage_data
            )
        
        mapping = self.mappings[license_field]
        
        # Handle simple string mapping (1:1)
        if isinstance(mapping, str):
            return MappingResult(
                target_field=mapping,
                available=usage_data is None or mapping in usage_data
            )
        
        # Handle complex mapping with fallback chain
        if isinstance(mapping, dict):
            primary = mapping.get('primary', license_field)
            fallbacks = mapping.get('fallback', [])
            
            # If no usage data provided, return primary without checking availability
            if usage_data is None:
                return MappingResult(target_field=primary, available=True)
            
            # Check primary field first
            if primary in usage_data:
                return MappingResult(target_field=primary, available=True)
            
            # Try fallback chain
            for fallback in fallbacks:
                # Resolve fallback through mappings (may itself be a mapping)
                fallback_result = self.get_target_field(fallback, usage_data)
                if fallback_result.available and fallback_result.target_field in usage_data:
                    return MappingResult(
                        target_field=fallback_result.target_field,
                        fallback_used=True,
                        fallback_field=fallback,
                        available=True
                    )
            
            # No primary or fallback found
            return MappingResult(
                target_field=primary,
                fallback_used=False,
                available=False
            )
        
        # Unknown mapping type
        return MappingResult(
            target_field=license_field,
            available=False
        )
    
    def map_license_quantities(
        self,
        licensed: Dict[str, int],
        usage_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, int]:
        """
        Map all license quantities to usage field names.
        
        Args:
            licensed: Dict of license field -> quantity from XML
            usage_data: Optional usage data for fallback resolution
        
        Returns:
            Dict of usage field names -> quantities
        
        Examples:
            >>> licensed = {'PROCESSPOINTS': 4750, 'DIRECTSTATIONS': 8}
            >>> mapped = mapper.map_license_quantities(licensed)
            >>> assert mapped == {'PROCESSPOINTS': 4750, 'CONSOLE_STATIONS': 8}
        """
        mapped = {}
        
        for license_field, quantity in licensed.items():
            result = self.get_target_field(license_field, usage_data)
            if result.available:
                mapped[result.target_field] = quantity
        
        return mapped
    
    def get_usage_value(
        self,
        license_field: str,
        usage_data: Dict[str, Any]
    ) -> Optional[Any]:
        """
        Get usage value for a license field, applying mappings and fallbacks.
        
        Args:
            license_field: Field name from license (e.g., 'DIRECTSTATIONS')
            usage_data: Dict of usage data from CSV
        
        Returns:
            Usage value if found, None otherwise
        
        Examples:
            >>> usage = {'CONSOLE_STATIONS': 5, 'PROCESSPOINTS': 108}
            >>> value = mapper.get_usage_value('DIRECTSTATIONS', usage)
            >>> assert value == 5  # Mapped to CONSOLE_STATIONS
            
            >>> # Fallback chain
            >>> usage = {'MULTISTATIONS': 10}  # STATIONS not present
            >>> value = mapper.get_usage_value('STATIONS', usage)
            >>> assert value == 10  # Used fallback
        """
        result = self.get_target_field(license_field, usage_data)
        
        if result.available and result.target_field in usage_data:
            return usage_data[result.target_field]
        
        return None
    
    def get_reverse_mapping(self, usage_field: str) -> List[str]:
        """
        Get all license fields that map to a given usage field.
        
        Useful for understanding which license fields correspond to
        a usage field when processing CSV data.
        
        Args:
            usage_field: Field name from CSV usage data
        
        Returns:
            List of license field names that map to this usage field
        
        Examples:
            >>> license_fields = mapper.get_reverse_mapping('CONSOLE_STATIONS')
            >>> assert 'DIRECTSTATIONS' in license_fields
        """
        reverse = []
        
        for license_field, mapping in self.mappings.items():
            if isinstance(mapping, str):
                if mapping == usage_field:
                    reverse.append(license_field)
            elif isinstance(mapping, dict):
                primary = mapping.get('primary')
                if primary == usage_field:
                    reverse.append(license_field)
                
                # Check fallbacks
                fallbacks = mapping.get('fallback', [])
                if usage_field in fallbacks:
                    reverse.append(license_field)
        
        return reverse
    
    def get_all_mapped_fields(self) -> Dict[str, str]:
        """
        Get flattened dict of all license -> usage field mappings.
        
        Ignores fallback chains, only returns primary mappings.
        
        Returns:
            Dict mapping license field names to usage field names
        
        Examples:
            >>> mappings = mapper.get_all_mapped_fields()
            >>> assert mappings['DIRECTSTATIONS'] == 'CONSOLE_STATIONS'
            >>> assert mappings['PROCESSPOINTS'] == 'PROCESSPOINTS'
        """
        flat_mappings = {}
        
        for license_field, mapping in self.mappings.items():
            if isinstance(mapping, str):
                flat_mappings[license_field] = mapping
            elif isinstance(mapping, dict):
                primary = mapping.get('primary', license_field)
                flat_mappings[license_field] = primary
        
        return flat_mappings
