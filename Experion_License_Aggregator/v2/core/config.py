"""
Configuration management for V2.0.

Loads and manages YAML and JSON configuration files with validation.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from v2.core.exceptions import ConfigurationError, MissingConfigError, InvalidConfigError


class Config:
    """
    Configuration manager for V2.0 pipeline.
    
    Loads all YAML and JSON configuration files and provides
    a unified interface for accessing settings.
    
    Attributes:
        config_dir: Path to configuration directory
        field_mappings: XML↔CSV field mapping rules
        cost_rules: Pricing cascade configuration
        validation_rules: Business validation rules
        transfer_rules: Transfer candidate criteria
        system_names: System name catalog (JSON)
        cost_catalog: Honeywell baseline pricing (JSON)
        cost_catalog_mpc: MPC 2026 confirmed pricing (JSON)
        settings: General settings (JSON)
    """
    
    def __init__(self, config_dir: str = 'config'):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Path to configuration directory
        
        Raises:
            ConfigurationError: If config directory doesn't exist
        """
        self.config_dir = Path(config_dir)
        
        if not self.config_dir.exists():
            raise ConfigurationError(
                f"Configuration directory not found: {self.config_dir}"
            )
        
        # Load all configurations
        self.field_mappings = self._load_yaml('field_mappings.yaml')
        self.cost_rules = self._load_yaml('cost_rules.yaml')
        self.validation_rules = self._load_yaml('validation_rules.yaml')
        self.transfer_rules = self._load_yaml('transfer_rules.yaml')
        
        # Load JSON catalogs
        self.system_names = self._load_json('system_names.json')
        self.cost_catalog = self._load_json('cost_catalog.json')
        self.cost_catalog_mpc = self._load_json('cost_catalog_mpc_2026.json')
        self.settings = self._load_json('settings.json')
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load YAML configuration file (supports multi-document YAML).
        
        Args:
            filename: Name of YAML file
        
        Returns:
            Parsed YAML as dictionary (merges multiple documents)
        
        Raises:
            ConfigurationError: If file not found or invalid
        """
        file_path = self.config_dir / filename
        
        if not file_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {file_path}"
            )
        
        try:
            with open(file_path, 'r') as f:
                # Handle multi-document YAML (separated by ---)
                documents = list(yaml.safe_load_all(f))
                
                # Merge all documents into single dict
                config = {}
                for doc in documents:
                    if doc:  # Skip empty documents
                        config.update(doc)
                
                return config
        except yaml.YAMLError as e:
            raise InvalidConfigError(
                f"Invalid YAML in {filename}: {e}"
            )
    
    def _load_json(self, filename: str) -> Dict[str, Any]:
        """
        Load JSON configuration file.
        
        Args:
            filename: Name of JSON file
        
        Returns:
            Parsed JSON as dictionary
        
        Raises:
            ConfigurationError: If file not found or invalid
        """
        file_path = self.config_dir / filename
        
        if not file_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {file_path}"
            )
        
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            return config if config else {}
        except json.JSONDecodeError as e:
            raise InvalidConfigError(
                f"Invalid JSON in {filename}: {e}"
            )
    
    @classmethod
    def from_directory(cls, config_dir: str) -> 'Config':
        """
        Factory method to create Config from directory.
        
        Args:
            config_dir: Path to configuration directory
        
        Returns:
            Configured Config instance
        """
        return cls(config_dir=config_dir)
    
    # ========================================================================
    # Field Mapping Methods
    # ========================================================================
    
    def get_csv_field_name(self, xml_field: str) -> Optional[str]:
        """
        Get CSV field name for XML field.
        
        Args:
            xml_field: XML field name (e.g., 'DIRECTSTATIONS')
        
        Returns:
            CSV equivalent (e.g., 'CONSOLE_STATIONS') or None
        """
        mappings = self.field_mappings.get('license_to_usage', {})
        csv_field = mappings.get(xml_field)
        
        # Handle complex mapping (dict with primary/fallback)
        if isinstance(csv_field, dict):
            return csv_field.get('primary')
        
        return csv_field
    
    def get_display_name(self, internal_name: str) -> str:
        """
        Get human-readable display name.
        
        Args:
            internal_name: Internal field name
        
        Returns:
            Display name or original name if not found
        """
        display_names = self.field_mappings.get('display_names', {})
        return display_names.get(internal_name, internal_name)
    
    # ========================================================================
    # Cost Rule Methods
    # ========================================================================
    
    def get_cost_for(self, license_type: str) -> Optional[float]:
        """
        Get cost for license type using cascade strategy.
        
        Cascade order:
        1. MPC 2026 Confirmed
        2. Honeywell Baseline
        3. Placeholder $100
        
        Args:
            license_type: License type name
        
        Returns:
            Unit price or None if not found
        """
        # Try MPC 2026 first
        if license_type in self.cost_catalog_mpc:
            cost_data = self.cost_catalog_mpc[license_type]
            if isinstance(cost_data, dict):
                return float(cost_data.get('unit_cost', 100.0))
            return float(cost_data)
        
        # Try Honeywell baseline
        if license_type in self.cost_catalog:
            cost_data = self.cost_catalog[license_type]
            if isinstance(cost_data, dict):
                return float(cost_data.get('unit_cost', 100.0))
            return float(cost_data)
        
        # Return placeholder
        placeholder = self.cost_rules.get('pricing_strategy', {}).get(
            'placeholder_price', 100.0
        )
        return float(placeholder)
    
    def get_price_source(self, license_type: str) -> str:
        """
        Get price source label for license type.
        
        Args:
            license_type: License type name
        
        Returns:
            Source label ('MPC 2026 Confirmed', 'Honeywell Baseline', etc.)
        """
        if license_type in self.cost_catalog_mpc:
            return 'MPC 2026 Confirmed'
        elif license_type in self.cost_catalog:
            return 'Honeywell Baseline'
        else:
            return 'Placeholder $100'
    
    # ========================================================================
    # Validation Rule Methods
    # ========================================================================
    
    def get_validation_threshold(self, metric: str) -> float:
        """
        Get data quality threshold.
        
        Args:
            metric: Metric name ('extraction_success_rate', 'utilization_match_rate', etc.)
        
        Returns:
            Threshold value (0.0-1.0)
        
        Raises:
            MissingConfigError: If threshold not found
        """
        thresholds = self.validation_rules.get('quality_thresholds', {})
        
        if metric not in thresholds:
            raise MissingConfigError(
                key=f"quality_thresholds.{metric}",
                config_file='validation_rules.yaml'
            )
        
        threshold_data = thresholds[metric]
        if isinstance(threshold_data, dict):
            # Extract min_percent and convert to decimal (90 -> 0.9)
            return float(threshold_data.get('min_percent', 0)) / 100.0
        return float(threshold_data)
    
    # ========================================================================
    # Transfer Rule Methods
    # ========================================================================
    
    def get_transfer_threshold(self, license_type: str, 
                              threshold_type: str) -> Optional[int]:
        """
        Get transfer detection threshold.
        
        Args:
            license_type: License type name
            threshold_type: 'absolute', 'percentage', or 'value'
        
        Returns:
            Threshold value or None
        """
        criteria = self.transfer_rules.get('criteria', {}).get(license_type, [])
        
        # criteria is a list of threshold objects
        for criterion in criteria:
            if criterion.get('type') == threshold_type and criterion.get('enabled', False):
                return criterion.get('threshold')
        
        return None
    
    # ========================================================================
    # System Catalog Methods
    # ========================================================================
    
    def get_friendly_name(self, msid: str, system_number: str) -> str:
        """
        Get friendly system name from catalog.
        
        Args:
            msid: System MSID
            system_number: System number
        
        Returns:
            Friendly name or concatenated MSID/number
        """
        key = f"{msid}|{system_number}"
        
        # Try exact match
        if key in self.system_names:
            return self.system_names[key]
        
        # Try without cluster prefix
        for catalog_key, friendly_name in self.system_names.items():
            if catalog_key.endswith(f"|{msid}|{system_number}"):
                return friendly_name
        
        # Return default
        return f"{msid}/{system_number}"
    
    @property
    def clusters(self) -> List[str]:
        """Get list of configured clusters"""
        return self.settings.get('clusters', ['Carson', 'Wilmington'])
    
    @property
    def excluded_releases(self) -> List[str]:
        """Get list of excluded release versions"""
        return self.settings.get('exclude_releases', [])
