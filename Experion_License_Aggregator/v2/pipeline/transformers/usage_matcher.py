"""
Usage Matcher - Match XML licenses to CSV usage data.

This module coordinates the matching of license records (from XML) to
usage records (from CSV), using the MatchValidator for quality assessment
and FieldMapper for field name normalization.

Matching Strategies:
1. Exact match: MSID + Cluster match exactly
2. Fuzzy match: Levenshtein distance on MSID (within threshold)
3. Cluster-only: Same cluster, MSID variations

Results track match confidence, unmatched records, and low-confidence matches
for quality reporting.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

from v2.models.license import LicenseData
from v2.models.usage import UsageData
from v2.pipeline.validators.match_validator import MatchValidator
from v2.pipeline.transformers.field_mapper import FieldMapper


@dataclass
class MatchRecord:
    """
    Single license-to-usage match with quality metrics.
    
    Attributes:
        license: The license record from XML
        usage: The matched usage record from CSV (None if unmatched)
        confidence: Match confidence score (0.0 - 1.0)
        match_type: How the match was found ('exact', 'fuzzy', 'none')
        issues: List of quality issues or warnings
    
    Examples:
        >>> match = MatchRecord(license, usage, confidence=1.0, match_type='exact')
        >>> if match.confidence >= 0.9:
        ...     print("High quality match")
    """
    license: LicenseData
    usage: Optional[UsageData] = None
    confidence: float = 0.0
    match_type: str = 'none'
    issues: List[str] = field(default_factory=list)


@dataclass
class MatchingResult:
    """
    Complete result of license-to-usage matching operation.
    
    Attributes:
        matches: List of all MatchRecord instances
        matched_count: Number of licenses with usage data matched
        unmatched_licenses: Number of licenses without usage matches
        low_confidence_count: Number of matches below confidence threshold
        duplicate_matches: Dict of usage records matched to multiple licenses
        stats: Summary statistics for reporting
    
    Examples:
        >>> result = matcher.match(licenses, usage_list)
        >>> print(f"Matched: {result.matched_count}/{len(licenses)}")
        >>> print(f"Low confidence: {result.low_confidence_count}")
    """
    matches: List[MatchRecord]
    matched_count: int
    unmatched_licenses: int
    low_confidence_count: int
    duplicate_matches: Dict[str, List[str]]
    stats: Dict[str, int]


class UsageMatcher:
    """
    Matches XML licenses to CSV usage data with quality assessment.
    
    Uses MatchValidator for quality scoring and FieldMapper for field
    name normalization. Tracks match confidence and identifies issues
    like unmatched records and low-confidence matches.
    
    The matcher attempts multiple strategies:
    1. Exact MSID + cluster match (highest confidence)
    2. Fuzzy MSID match within same cluster
    3. Reports unmatched licenses for investigation
    
    Examples:
        >>> matcher = UsageMatcher(field_mapper, match_validator)
        >>> result = matcher.match(licenses, usage_data_list)
        >>> assert result.matched_count == 20
        >>> for match in result.matches:
        ...     if match.usage:
        ...         print(f"{match.license.msid} → {match.usage.msid}")
    """
    
    def __init__(
        self, 
        field_mapper: FieldMapper,
        match_validator: MatchValidator,
        min_confidence: float = 0.8
    ):
        """
        Initialize usage matcher with dependencies.
        
        Args:
            field_mapper: FieldMapper for normalizing field names
            match_validator: MatchValidator for assessing match quality
            min_confidence: Minimum confidence for acceptable match (default 0.8)
        """
        self.field_mapper = field_mapper
        self.match_validator = match_validator
        self.min_confidence = min_confidence
    
    def match(
        self,
        licenses: List[LicenseData],
        usage_data_list: List[UsageData]
    ) -> MatchingResult:
        """
        Match licenses to usage data with quality tracking.
        
        Args:
            licenses: List of LicenseData from XML files
            usage_data_list: List of UsageData from CSV files
        
        Returns:
            MatchingResult with all matches and statistics
        
        Algorithm:
        1. Group usage data by MSID for fast lookup
        2. For each license, find best matching usage record
        3. Use MatchValidator to assess match quality
        4. Track match confidence and issues
        5. Identify unmatched and low-confidence cases
        
        Raises:
            ValueError: If input lists are empty
        """
        if not licenses:
            raise ValueError("Cannot match empty license list")
        if not usage_data_list:
            raise ValueError("Cannot match empty usage data list")
        
        # Group usage data by MSID for efficient lookup
        usage_by_msid = self._group_usage_by_msid(usage_data_list)
        
        matches = []
        used_usage_ids = set()
        duplicate_matches = defaultdict(list)
        
        # Match each license
        for license_obj in licenses:
            match_record = self._find_best_match(
                license_obj, 
                usage_by_msid,
                used_usage_ids
            )
            matches.append(match_record)
            
            # Track usage record usage
            if match_record.usage:
                usage_key = (match_record.usage.msid, match_record.usage.cluster)
                if usage_key in used_usage_ids:
                    # Duplicate match detected
                    duplicate_matches[f"{match_record.usage.msid}/{match_record.usage.cluster}"].append(
                        f"{license_obj.msid}/{license_obj.cluster}"
                    )
                used_usage_ids.add(usage_key)
        
        # Calculate statistics
        matched_count = sum(1 for m in matches if m.usage is not None)
        unmatched_count = len(matches) - matched_count
        low_confidence_count = sum(
            1 for m in matches 
            if m.usage and m.confidence < self.min_confidence
        )
        
        stats = {
            'total_licenses': len(licenses),
            'total_usage_records': len(usage_data_list),
            'matched': matched_count,
            'unmatched': unmatched_count,
            'low_confidence': low_confidence_count,
            'duplicate_matches': len(duplicate_matches),
            'exact_matches': sum(1 for m in matches if m.match_type == 'exact'),
            'fuzzy_matches': sum(1 for m in matches if m.match_type == 'fuzzy'),
        }
        
        return MatchingResult(
            matches=matches,
            matched_count=matched_count,
            unmatched_licenses=unmatched_count,
            low_confidence_count=low_confidence_count,
            duplicate_matches=dict(duplicate_matches),
            stats=stats
        )
    
    def _group_usage_by_msid(
        self, 
        usage_data_list: List[UsageData]
    ) -> Dict[str, List[UsageData]]:
        """
        Group usage records by MSID for efficient lookup.
        
        Args:
            usage_data_list: List of UsageData records
        
        Returns:
            Dict mapping MSID to list of UsageData records
        """
        grouped = defaultdict(list)
        for usage in usage_data_list:
            grouped[usage.msid].append(usage)
        return dict(grouped)
    
    def _find_best_match(
        self,
        license_obj: LicenseData,
        usage_by_msid: Dict[str, List[UsageData]],
        used_usage_ids: set
    ) -> MatchRecord:
        """
        Find best matching usage record for a license.
        
        Args:
            license_obj: License to find match for
            usage_by_msid: Dict of MSID -> UsageData list
            used_usage_ids: Set of already-matched usage IDs
        
        Returns:
            MatchRecord with best match or unmatched record
        
        Strategy:
        1. Try exact MSID match in same cluster
        2. Try fuzzy MSID match (Levenshtein distance)
        3. Return unmatched if no suitable match found
        """
        # Try exact MSID match first
        if license_obj.msid in usage_by_msid:
            candidates = usage_by_msid[license_obj.msid]
            
            # Filter by cluster if available
            cluster_matches = [
                u for u in candidates 
                if u.cluster and u.cluster.lower() == license_obj.cluster.lower()
            ]
            
            if cluster_matches:
                # Use first cluster match (should be only one)
                best_usage = cluster_matches[0]
                return self._create_match_record(
                    license_obj, 
                    best_usage,
                    match_type='exact'
                )
        
        # Try fuzzy matching across all usage records
        best_match = self._try_fuzzy_match(
            license_obj,
            usage_by_msid,
            used_usage_ids
        )
        
        if best_match:
            return best_match
        
        # No match found
        return MatchRecord(
            license=license_obj,
            usage=None,
            confidence=0.0,
            match_type='none',
            issues=[f"No usage data found for {license_obj.msid}/{license_obj.cluster}"]
        )
    
    def _try_fuzzy_match(
        self,
        license_obj: LicenseData,
        usage_by_msid: Dict[str, List[UsageData]],
        used_usage_ids: set
    ) -> Optional[MatchRecord]:
        """
        Attempt fuzzy matching using MatchValidator.
        
        Args:
            license_obj: License to match
            usage_by_msid: Dict of MSID -> UsageData list
            used_usage_ids: Set of already-matched usage IDs
        
        Returns:
            MatchRecord if fuzzy match found, None otherwise
        """
        # Collect all usage candidates from same cluster
        candidates = []
        for usage_list in usage_by_msid.values():
            for usage in usage_list:
                if usage.cluster and usage.cluster.lower() == license_obj.cluster.lower():
                    candidates.append(usage)
        
        if not candidates:
            return None
        
        # Try each candidate with MatchValidator
        best_confidence = 0.0
        best_usage = None
        best_validation = None
        
        for usage in candidates:
            validation = self.match_validator.validate((license_obj, usage))
            
            # Extract confidence from validation result
            # MatchValidator returns matched bool and issues
            # We need to infer confidence from match quality
            if validation.passed:
                # Check if this is a fuzzy match
                confidence = self._extract_confidence(validation, license_obj, usage)
                
                if confidence > best_confidence and confidence >= self.min_confidence:
                    best_confidence = confidence
                    best_usage = usage
                    best_validation = validation
        
        if best_usage:
            return self._create_match_record(
                license_obj,
                best_usage,
                match_type='fuzzy',
                validation_result=best_validation
            )
        
        return None
    
    def _extract_confidence(
        self,
        validation_result,
        license_obj: LicenseData,
        usage: UsageData
    ) -> float:
        """
        Extract confidence score from validation result.
        
        Args:
            validation_result: ValidationResult from MatchValidator
            license_obj: License being matched
            usage: Usage record being matched
        
        Returns:
            Confidence score (0.0 - 1.0)
        """
        # Perfect match: both MSID and cluster match exactly
        if (license_obj.msid.lower() == usage.msid.lower() and
            license_obj.cluster.lower() == usage.cluster.lower()):
            return 1.0
        
        # MSID match only (cluster might differ)
        if license_obj.msid.lower() == usage.msid.lower():
            return 0.5
        
        # Fuzzy match - check for info about fuzzy matching
        if any('fuzzy' in str(i).lower() for i in validation_result.info):
            # Extract confidence from info messages if available
            for info in validation_result.info:
                if 'confidence' in str(info).lower():
                    # Try to extract numeric confidence
                    import re
                    match = re.search(r'(\d+)%', str(info))
                    if match:
                        return float(match.group(1)) / 100.0
            return 0.8  # Default fuzzy confidence
        
        return 0.5  # Partial match
    
    def _create_match_record(
        self,
        license_obj: LicenseData,
        usage: UsageData,
        match_type: str,
        validation_result=None
    ) -> MatchRecord:
        """
        Create MatchRecord with validation assessment.
        
        Args:
            license_obj: License record
            usage: Matched usage record
            match_type: Type of match ('exact', 'fuzzy')
            validation_result: Optional ValidationResult from MatchValidator
        
        Returns:
            MatchRecord with confidence and issues
        """
        # Get validation if not provided
        if validation_result is None:
            validation_result = self.match_validator.validate((license_obj, usage))
        
        # Calculate confidence
        confidence = self._extract_confidence(validation_result, license_obj, usage)
        
        # Collect issues
        issues = []
        issues.extend(validation_result.warnings)
        if not validation_result.passed:
            issues.extend(validation_result.errors)
        
        # Add low confidence warning
        if confidence < self.min_confidence:
            issues.append(f"Low confidence match: {confidence:.0%}")
        
        return MatchRecord(
            license=license_obj,
            usage=usage,
            confidence=confidence,
            match_type=match_type,
            issues=issues
        )
    
    def generate_match_report(self, result: MatchingResult) -> str:
        """
        Generate human-readable matching report.
        
        Args:
            result: MatchingResult from match()
        
        Returns:
            Multi-line string report
        
        Example Output:
            License-Usage Matching Report
            =============================
            Total licenses: 36
            Matched: 20 (55.6%)
            Unmatched: 16 (44.4%)
            Low confidence: 3
            
            Match Quality:
            - Exact matches: 18
            - Fuzzy matches: 2
        """
        lines = [
            "License-Usage Matching Report",
            "=" * 29,
            f"Total licenses: {result.stats['total_licenses']}",
            f"Matched: {result.matched_count} ({result.matched_count/result.stats['total_licenses']*100:.1f}%)",
            f"Unmatched: {result.unmatched_licenses} ({result.unmatched_licenses/result.stats['total_licenses']*100:.1f}%)",
            f"Low confidence: {result.low_confidence_count}",
            "",
            "Match Quality:",
            f"- Exact matches: {result.stats['exact_matches']}",
            f"- Fuzzy matches: {result.stats['fuzzy_matches']}",
        ]
        
        if result.duplicate_matches:
            lines.append("")
            lines.append("Duplicate Matches (usage matched to multiple licenses):")
            for usage_key, license_keys in result.duplicate_matches.items():
                lines.append(f"- {usage_key}: {', '.join(license_keys)}")
        
        if result.unmatched_licenses > 0:
            lines.append("")
            lines.append("Unmatched Licenses:")
            unmatched = [m for m in result.matches if m.usage is None]
            for match in unmatched[:10]:  # Show first 10
                lines.append(f"- {match.license.msid}/{match.license.cluster}")
            if len(unmatched) > 10:
                lines.append(f"  ... and {len(unmatched) - 10} more")
        
        return "\n".join(lines)
