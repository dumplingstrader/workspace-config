"""
Pipeline Coordinator for V2.0.

Orchestrates end-to-end license processing workflow:
1. Extract data from XML/CSV sources
2. Validate extracted data
3. Transform data (matching, costing, transfer detection)
4. Export to JSON/Excel

Provides both programmatic API and CLI interface.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import logging

from ..models.license import LicenseData
from ..models.usage import UsageData
from ..models.cost import CostCalculation
from ..models.transfer import TransferCandidate
from ..core.config import Config
from ..core.exceptions import (
    DataExtractionError,
    DataValidationError,
    ProcessingError
)

from .extractors.xml_extractor import XmlExtractor
from .extractors.csv_extractor import CsvExtractor
from .validators.schema_validator import SchemaValidator
from .validators.business_validator import BusinessValidator
from .validators.match_validator import MatchValidator
from .transformers.usage_matcher import UsageMatcher
from .transformers.field_mapper import FieldMapper
from .transformers.cost_calculator import CostCalculator
from .transformers.transfer_detector import TransferDetector
from .exporters.json_exporter import JsonExporter
from .exporters.excel_exporter import ExcelExporter


logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """
    Result of pipeline execution.
    
    Contains all processed data and execution metrics.
    """
    
    success: bool
    licenses: List[LicenseData] = field(default_factory=list)
    usage_data: List[UsageData] = field(default_factory=list)
    costs: List[CostCalculation] = field(default_factory=list)
    transfers: List[TransferCandidate] = field(default_factory=list)
    
    # Execution metadata
    execution_time: float = 0.0
    stage_times: Dict[str, float] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Statistics
    stats: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize result to dictionary."""
        return {
            'success': self.success,
            'execution_time': self.execution_time,
            'stage_times': self.stage_times,
            'errors': self.errors,
            'warnings': self.warnings,
            'statistics': {
                'licenses': len(self.licenses),
                'usage_records': len(self.usage_data),
                'cost_records': len(self.costs),
                'transfer_candidates': len(self.transfers),
                **self.stats
            }
        }


class PipelineCoordinator:
    """
    Coordinates end-to-end license processing pipeline.
    
    Orchestrates extraction, validation, transformation, and export stages.
    """
    
    def __init__(
        self,
        config_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        """
        Initialize pipeline coordinator.
        
        Args:
            config_dir: Directory containing config files (default: ../config)
            output_dir: Directory for output files (default: ../data/output)
        """
        self.config_dir = config_dir or Path(__file__).parent.parent / "config"
        self.output_dir = output_dir or Path(__file__).parent.parent / "data" / "output"
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize config manager
        self.config = Config(self.config_dir)
        
        # Initialize components (lazy loading)
        self._xml_extractor: Optional[XmlExtractor] = None
        self._csv_extractor: Optional[CsvExtractor] = None
        self._schema_validator: Optional[SchemaValidator] = None
        self._business_validator: Optional[BusinessValidator] = None
        self._match_validator: Optional[MatchValidator] = None
        self._field_mapper: Optional[FieldMapper] = None
        self._usage_matcher: Optional[UsageMatcher] = None
        self._cost_calculator: Optional[CostCalculator] = None
        self._transfer_detector: Optional[TransferDetector] = None
        self._json_exporter: Optional[JsonExporter] = None
        self._excel_exporter: Optional[ExcelExporter] = None
    
    # Component properties (lazy initialization)
    
    @property
    def xml_extractor(self) -> XmlExtractor:
        """Get XML extractor instance."""
        if self._xml_extractor is None:
            self._xml_extractor = XmlExtractor()
        return self._xml_extractor
    
    @property
    def csv_extractor(self) -> CsvExtractor:
        """Get CSV extractor instance."""
        if self._csv_extractor is None:
            self._csv_extractor = CsvExtractor()
        return self._csv_extractor
    
    @property
    def schema_validator(self) -> SchemaValidator:
        """Get schema validator instance."""
        if self._schema_validator is None:
            self._schema_validator = SchemaValidator()
        return self._schema_validator
    
    @property
    def business_validator(self) -> BusinessValidator:
        """Get business validator instance."""
        if self._business_validator is None:
            self._business_validator = BusinessValidator(self.config)
        return self._business_validator
    
    @property
    def match_validator(self) -> MatchValidator:
        """Get match validator instance."""
        if self._match_validator is None:
            self._match_validator = MatchValidator(config=self.config)
        return self._match_validator
    
    @property
    def field_mapper(self) -> FieldMapper:
        """Get field mapper instance."""
        if self._field_mapper is None:
            self._field_mapper = FieldMapper(self.config)
        return self._field_mapper
    
    @property
    def usage_matcher(self) -> UsageMatcher:
        """Get usage matcher instance."""
        if self._usage_matcher is None:
            self._usage_matcher = UsageMatcher(
                field_mapper=self.field_mapper,
                match_validator=self.match_validator
            )
        return self._usage_matcher
    
    @property
    def cost_calculator(self) -> CostCalculator:
        """Get cost calculator instance."""
        if self._cost_calculator is None:
            self._cost_calculator = CostCalculator(self.config)
        return self._cost_calculator
    
    @property
    def transfer_detector(self) -> TransferDetector:
        """Get transfer detector instance."""
        if self._transfer_detector is None:
            self._transfer_detector = TransferDetector(self.config)
        return self._transfer_detector
    
    @property
    def json_exporter(self) -> JsonExporter:
        """Get JSON exporter instance."""
        if self._json_exporter is None:
            self._json_exporter = JsonExporter(self.output_dir)
        return self._json_exporter
    
    @property
    def excel_exporter(self) -> ExcelExporter:
        """Get Excel exporter instance."""
        if self._excel_exporter is None:
            self._excel_exporter = ExcelExporter(self.output_dir)
        return self._excel_exporter
    
    def run_pipeline(
        self,
        xml_dir: Path,
        csv_file: Optional[Path] = None,
        usage_data: Optional[List[UsageData]] = None,
        clusters: Optional[List[str]] = None,
        export_json: bool = True,
        export_excel: bool = True,
        validate_business_rules: bool = True
    ) -> PipelineResult:
        """
        Execute complete pipeline.
        
        Args:
            xml_dir: Directory containing XML license files
            csv_file: Optional CSV utilization file
            usage_data: Optional pre-extracted usage data (alternative to csv_file)
            clusters: Optional list of clusters to process
            export_json: Export results to JSON
            export_excel: Export results to Excel
            validate_business_rules: Run business validation
            
        Returns:
            PipelineResult with all processed data and metrics
        """
        start_time = datetime.now()
        result = PipelineResult(success=False)
        
        try:
            logger.info("Starting pipeline execution")
            logger.info(f"XML directory: {xml_dir}")
            if csv_file:
                logger.info(f"CSV file: {csv_file}")
            
            # Stage 1: Extract licenses from XML
            stage_start = datetime.now()
            logger.info("[1/6] Extracting license data from XML...")
            licenses = self._extract_licenses(xml_dir, clusters)
            result.licenses = licenses
            result.stage_times['extraction'] = (datetime.now() - stage_start).total_seconds()
            logger.info(f"Extracted {len(licenses)} license records")
            
            # Stage 2: Validate license data
            stage_start = datetime.now()
            logger.info("[2/6] Validating license data...")
            validation_errors = self._validate_licenses(licenses, validate_business_rules)
            result.stage_times['validation'] = (datetime.now() - stage_start).total_seconds()
            
            if validation_errors:
                result.warnings.extend(validation_errors)
                logger.warning(f"Found {len(validation_errors)} validation warnings")
            
            # Stage 3: Extract usage data (if CSV provided or usage_data pre-loaded)
            extracted_usage = []
            if usage_data:
                # Use pre-extracted usage data
                logger.info("[3/6] Using pre-loaded usage data...")
                extracted_usage = usage_data
                logger.info(f"Loaded {len(extracted_usage)} usage records")
            elif csv_file and csv_file.exists():
                stage_start = datetime.now()
                logger.info("[3/6] Extracting usage data from CSV...")
                try:
                    extracted_usage = self._extract_usage(csv_file)
                    result.usage_data = extracted_usage
                    result.stage_times['usage_extraction'] = (datetime.now() - stage_start).total_seconds()
                    logger.info(f"Extracted {len(extracted_usage)} usage records")
                except DataExtractionError as e:
                    # CSV extraction is optional - log warning and continue
                    result.warnings.append(f"CSV extraction failed: {e}")
                    logger.warning(f"CSV extraction failed: {e}")
                    result.stage_times['usage_extraction'] = (datetime.now() - stage_start).total_seconds()
            else:
                logger.info("[3/6] No usage data provided, skipping...")
            
            result.usage_data = extracted_usage
            
            # Stage 4: Transform - Match licenses with usage
            stage_start = datetime.now()
            logger.info("[4/6] Matching licenses with usage data...")
            matched_licenses, matched_usage = self._match_license_usage(licenses, extracted_usage)
            result.stage_times['matching'] = (datetime.now() - stage_start).total_seconds()
            logger.info(f"Matched {len(matched_usage)} usage records to licenses")
            
            # Stage 5: Transform - Calculate costs and detect transfers
            stage_start = datetime.now()
            logger.info("[5/6] Calculating costs and detecting transfer opportunities...")
            costs = self._calculate_costs(matched_licenses)
            transfers = self._detect_transfers(matched_licenses, matched_usage, costs)
            result.costs = costs
            result.transfers = transfers
            result.stage_times['transformation'] = (datetime.now() - stage_start).total_seconds()
            logger.info(f"Calculated costs for {len(costs)} records")
            logger.info(f"Found {len(transfers)} transfer candidates")
            
            # Stage 6: Export results
            stage_start = datetime.now()
            logger.info("[6/6] Exporting results...")
            export_errors = self._export_results(
                licenses=matched_licenses,
                usage_data=matched_usage,
                costs=costs,
                transfers=transfers,
                export_json=export_json,
                export_excel=export_excel
            )
            result.stage_times['export'] = (datetime.now() - stage_start).total_seconds()
            
            if export_errors:
                result.errors.extend(export_errors)
                logger.error(f"Export errors: {export_errors}")
            
            # Calculate statistics
            result.stats = self._calculate_statistics(
                licenses, usage_data, costs, transfers
            )
            
            # Mark success
            result.success = len(result.errors) == 0
            result.execution_time = (datetime.now() - start_time).total_seconds()
            
            logger.info("Pipeline execution complete")
            logger.info(f"Total execution time: {result.execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            result.success = False
            result.errors.append(str(e))
            result.execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Pipeline execution failed: {e}", exc_info=True)
            return result
    
    def _extract_licenses(
        self,
        xml_dir: Path,
        clusters: Optional[List[str]] = None
    ) -> List[LicenseData]:
        """Extract licenses from XML files."""
        try:
            all_licenses = []
            
            # Validate directory exists
            if not xml_dir.exists():
                raise DataExtractionError(f"XML directory does not exist: {xml_dir}")
            
            # Find all XML files in directory (recursive)
            xml_files = list(xml_dir.glob("**/*.xml"))
            if not xml_files:
                logger.warning(f"No XML files found in {xml_dir}")
                return []
            
            logger.info(f"Found {len(xml_files)} XML files to process")
            
            # Extract from each file
            for xml_file in xml_files:
                extraction_result = self.xml_extractor.extract_from_file(xml_file)
                
                if not extraction_result.success:
                    error_msg = '; '.join(extraction_result.errors)
                    logger.warning(
                        f"Failed to extract from {xml_file.name}: {error_msg}"
                    )
                    continue
                
                # extraction_result.data is a single LicenseData, not a list
                license_data = extraction_result.data
                
                # Filter by clusters if specified
                if clusters and license_data.cluster not in clusters:
                    continue
                
                all_licenses.append(license_data)
            
            return all_licenses
            
        except Exception as e:
            raise DataExtractionError(f"Failed to extract licenses: {e}")
    
    def _validate_licenses(
        self,
        licenses: List[LicenseData],
        validate_business_rules: bool = True
    ) -> List[str]:
        """Validate license data, return list of validation errors/warnings."""
        errors = []
        
        # Schema validation
        for idx, license in enumerate(licenses):
            schema_result = self.schema_validator.validate(license)
            if not schema_result.passed:
                errors.append(
                    f"License {idx} schema validation failed: {schema_result.errors}"
                )
        
        # Business rule validation
        if validate_business_rules:
            for idx, license in enumerate(licenses):
                business_result = self.business_validator.validate(license)
                if not business_result.passed:
                    errors.extend([
                        f"License {idx}: {error}" 
                        for error in business_result.errors
                    ])
        
        return errors
    
    def _extract_usage(self, csv_file: Path) -> List[UsageData]:
        """Extract usage data from CSV."""
        try:
            extraction_result = self.csv_extractor.extract_from_file(csv_file)
            
            if not extraction_result.success:
                error_msg = '; '.join(extraction_result.errors)
                raise DataExtractionError(f"CSV extraction failed: {error_msg}")
            
            return extraction_result.data
            
        except Exception as e:
            raise DataExtractionError(f"Failed to extract usage data: {e}")
    
    def _match_license_usage(
        self,
        licenses: List[LicenseData],
        usage_data: List[UsageData]
    ) -> Tuple[List[LicenseData], List[UsageData]]:
        """Match licenses with usage data at license-type level.
        
        Note: Matching happens at the license-type level, not system level.
        Each UsageData represents one license type for one system.
        Each LicenseData contains all license types for one system.
        """
        if not usage_data:
            return licenses, []
        
        try:
            # Create usage lookup by (msid, license_type)
            usage_lookup = {}
            for usage in usage_data:
                key = (usage.msid, usage.license_type)
                usage_lookup[key] = usage
            
            # Count how many license types have matching usage data
            matched_types = 0
            total_types = 0
            
            for license_obj in licenses:
                for license_type in license_obj.licensed.keys():
                    total_types += 1
                    key = (license_obj.msid, license_type)
                    if key in usage_lookup:
                        matched_types += 1
            
            # Debug output
            print(f"\n[DEBUG] Usage Matching Summary:")
            print(f"  Total license systems: {len(licenses)}")
            print(f"  Total license types across all systems: {total_types}")
            print(f"  Total usage records: {len(usage_data)}")
            print(f"  Matched license types: {matched_types}")
            print(f"  Match rate: {matched_types/total_types*100:.1f}%")
            
            if matched_types > 0:
                # Show sample match
                for lic in licenses[:1]:
                    for lt in list(lic.licensed.keys())[:1]:
                        key = (lic.msid, lt)
                        if key in usage_lookup:
                            usage = usage_lookup[key]
                            print(f"  Sample match: {lic.msid} {lt}: {lic.licensed[lt]} licensed, {usage.used_quantity} used")
                            break
                    else:
                        continue
                    break
            
            logger.info(f"Matched {matched_types}/{total_types} license types to usage data")
            
            # Return all licenses and all usage data
            # Matching at license-type level happens in _detect_transfers
            return licenses, usage_data
            
        except Exception as e:
            raise ProcessingError(f"Failed to match licenses: {e}")
    
    def _calculate_costs(
        self,
        licenses: List[LicenseData]
    ) -> List[CostCalculation]:
        """Calculate costs for licenses."""
        try:
            all_costs = []
            
            # Group licenses by system (msid + system_number)
            systems = {}
            for lic in licenses:
                key = (lic.msid, lic.system_number, lic.cluster)
                if key not in systems:
                    systems[key] = {}
                # Merge licensed quantities from this license into system dict
                for license_type, quantity in lic.licensed.items():
                    if license_type in systems[key]:
                        # If multiple versions of same license exist, use max quantity
                        systems[key][license_type] = max(systems[key][license_type], quantity)
                    else:
                        systems[key][license_type] = quantity
            
            # Calculate costs for each system
            for (msid, system_number, cluster), licensed in systems.items():
                summary = self.cost_calculator.calculate_license_cost(
                    licensed=licensed,
                    msid=msid,
                    cluster=cluster,
                    system_number=system_number
                )
                
                # Convert LicenseCostSummary.costs (List[CostResult]) 
                # to List[CostCalculation]
                for cost_result in summary.costs:
                    cost_calc = CostCalculation(
                        msid=msid,
                        system_number=system_number,
                        license_type=cost_result.license_type,
                        licensed_quantity=cost_result.quantity,
                        unit_price=cost_result.unit_cost,
                        total_cost=cost_result.total_cost,
                        price_source=cost_result.pricing_source,
                        cluster=cluster
                    )
                    all_costs.append(cost_calc)
            
            return all_costs
            
        except Exception as e:
            raise ProcessingError(f"Failed to calculate costs: {e}")
    
    def _detect_transfers(
        self,
        licenses: List[LicenseData],
        usage_data: List[UsageData],
        costs: List[CostCalculation]
    ) -> List[TransferCandidate]:
        """Detect transfer opportunities."""
        try:
            # Transform LicenseData and UsageData into enriched dict format
            # that TransferDetector expects
            enriched_licenses = []
            
            # Create usage lookup by (msid, license_type)
            # Note: UsageData has msid and license_type, but NOT system_number
            usage_by_msid_type = {}
            for usage in usage_data:
                key = (usage.msid, usage.license_type)
                usage_by_msid_type[key] = usage.used_quantity
            
            # Create cost lookup by (msid, system_number, license_type)
            cost_lookup = {}
            for cost in costs:
                key = (cost.msid, cost.system_number, cost.license_type)
                # TransferDetector expects cost_data dict with unit_cost key
                cost_lookup[key] = {
                    'unit_cost': cost.unit_price,
                    'total_cost': cost.total_cost
                }
            
            # Group licenses by system and enrich with usage
            systems = {}
            for lic in licenses:
                key = (lic.msid, lic.system_number, lic.cluster)
                if key not in systems:
                    systems[key] = {
                        'msid': lic.msid,
                        'system_number': lic.system_number,
                        'cluster': lic.cluster,
                        'licensed': {},
                        'usage': {},
                        'costs': {}
                    }
                # Merge licensed quantities (take max for multiple versions)
                for license_type, qty in lic.licensed.items():
                    if license_type in systems[key]['licensed']:
                        systems[key]['licensed'][license_type] = max(
                            systems[key]['licensed'][license_type], qty
                        )
                    else:
                        systems[key]['licensed'][license_type] = qty
                    
                    # Add usage data for this specific license type
                    usage_key = (lic.msid, license_type)
                    if usage_key in usage_by_msid_type:
                        systems[key]['usage'][license_type] = usage_by_msid_type[usage_key]
                    
                    # Add cost data for this specific license type
                    cost_key = (lic.msid, lic.system_number, license_type)
                    if cost_key in cost_lookup:
                        systems[key]['costs'][license_type] = cost_lookup[cost_key]
            
            # Convert systems dict to list of enriched licenses
            for (msid, system_number, cluster), enriched in systems.items():
                enriched_licenses.append(enriched)
            
            # Debug: Check if costs are in enriched licenses
            print(f"\n[DEBUG] Transfer Detection:")
            print(f"  Enriched licenses: {len(enriched_licenses)}")
            if len(enriched_licenses) > 0:
                sample = enriched_licenses[0]
                print(f"  Sample system: {sample['msid']}")
                print(f"    Licensed types: {len(sample['licensed'])}")
                print(f"    Usage types: {len(sample['usage'])}")
                print(f"    Cost types: {len(sample['costs'])}")
                if sample['costs']:
                    first_cost_type = list(sample['costs'].keys())[0]
                    first_cost_value = sample['costs'][first_cost_type]
                    print(f"    Sample cost key: {first_cost_type}")
                    print(f"    Sample cost value: {first_cost_value}")
                    print(f"    Value type: {type(first_cost_value)}")
                    if isinstance(first_cost_value, dict):
                        print(f"    unit_cost: ${first_cost_value.get('unit_cost', 0):,.2f}")
            
            # Detect transfers
            transfer_result = self.transfer_detector.detect(enriched_licenses, usage_data)
            
            return transfer_result.candidates
            
        except Exception as e:
            raise ProcessingError(f"Failed to detect transfers: {e}")
    
    def _export_results(
        self,
        licenses: List[LicenseData],
        usage_data: List[UsageData],
        costs: List[CostCalculation],
        transfers: List[TransferCandidate],
        export_json: bool = True,
        export_excel: bool = True
    ) -> List[str]:
        """Export results to JSON and/or Excel."""
        errors = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to JSON
        if export_json:
            try:
                # Build comprehensive data structure
                json_data = {
                    'licenses': [asdict(lic) for lic in licenses],
                    'usage_data': [asdict(u) for u in usage_data] if usage_data else [],
                    'costs': [asdict(c) for c in costs] if costs else [],
                    'transfers': [asdict(t) for t in transfers] if transfers else [],
                    'metadata': {
                        'export_timestamp': datetime.now().isoformat(),
                        'record_count': len(licenses),
                        'total_licenses': len(licenses),
                        'total_usage_records': len(usage_data) if usage_data else 0,
                        'total_cost': sum(c.total_cost for c in costs) if costs else 0,
                        'total_transfers': len(transfers) if transfers else 0
                    }
                }
                
                json_result = self.json_exporter.export(
                    data=json_data,
                    filename=f"license_report_{timestamp}.json"
                )
                
                if not json_result.success:
                    errors.append(f"JSON export failed: {json_result.errors}")
                else:
                    logger.info(f"JSON exported to: {json_result.output_path}")
                    
            except Exception as e:
                errors.append(f"JSON export error: {e}")
        
        # Export to Excel
        if export_excel:
            try:
                excel_result = self.excel_exporter.export_comprehensive(
                    licenses=licenses,
                    usage_data=usage_data if usage_data else None,
                    costs=costs if costs else None,
                    transfers=transfers if transfers else None,
                    output_filename=f"license_report_{timestamp}.xlsx"
                )
                
                if not excel_result.success:
                    errors.append(f"Excel export failed: {excel_result.errors}")
                else:
                    logger.info(f"Excel exported to: {excel_result.output_path}")
                    
            except Exception as e:
                errors.append(f"Excel export error: {e}")
        
        return errors
    
    def _calculate_statistics(
        self,
        licenses: List[LicenseData],
        usage_data: List[UsageData],
        costs: List[CostCalculation],
        transfers: List[TransferCandidate]
    ) -> Dict[str, Any]:
        """Calculate summary statistics."""
        stats = {}
        
        # Cluster breakdown
        clusters = {}
        for lic in licenses:
            clusters[lic.cluster] = clusters.get(lic.cluster, 0) + 1
        stats['clusters'] = clusters
        
        # Total costs
        if costs:
            stats['total_cost'] = sum(c.total_cost for c in costs)
            stats['avg_cost_per_license'] = stats['total_cost'] / len(licenses)
        
        # Transfer opportunities
        if transfers:
            stats['high_priority_transfers'] = sum(
                1 for t in transfers if t.priority == "HIGH"
            )
            stats['total_transfer_value'] = sum(t.excess_value for t in transfers)
        
        # Usage statistics
        if usage_data:
            stats['total_usage_records'] = len(usage_data)
            stats['avg_utilization'] = sum(
                u.used_quantity for u in usage_data
            ) / len(usage_data) if usage_data else 0
        
        return stats
