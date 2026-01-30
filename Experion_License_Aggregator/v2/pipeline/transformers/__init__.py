"""
Transformers package - Data transformation and enrichment operations.

This package contains modules for transforming validated license and usage data
into enriched, deduplicated, and matched records for export.

Modules:
    deduplicator: Version-based duplicate removal
    field_mapper: License type normalization and field mapping
    usage_matcher: XML-to-CSV matching with fuzzy logic
    cost_calculator: Multi-source cost calculation with cascade
    transfer_detector: License transfer identification
"""

from v2.pipeline.transformers.deduplicator import (
    Deduplicator,
    DeduplicationResult
)
from v2.pipeline.transformers.field_mapper import (
    FieldMapper,
    MappingResult
)
from v2.pipeline.transformers.usage_matcher import (
    UsageMatcher,
    MatchRecord,
    MatchingResult
)
from v2.pipeline.transformers.cost_calculator import (
    CostCalculator,
    CostResult,
    LicenseCostSummary
)
from v2.pipeline.transformers.transfer_detector import (
    TransferDetector,
    TransferDetectionResult
)

__all__ = [
    'Deduplicator',
    'DeduplicationResult',
    'FieldMapper',
    'MappingResult',
    'UsageMatcher',
    'MatchRecord',
    'MatchingResult',
    'CostCalculator',
    'CostResult',
    'LicenseCostSummary',
    'TransferDetector',
    'TransferDetectionResult',
]
