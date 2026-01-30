"""
Match validator for XML-to-CSV matching quality.

Validates matching between LicenseData (XML) and UsageData (CSV).
"""

from typing import Optional
from dataclasses import dataclass

from v2.pipeline.validators.base_validator import BaseValidator, ValidationResult
from v2.models.license import LicenseData
from v2.models.usage import UsageData
from v2.core.config import Config


@dataclass
class MatchResult:
    """Result of a match validation"""
    matched: bool
    confidence: float
    match_type: str  # 'exact', 'fuzzy', 'none'
    issues: list[str]


class MatchValidator(BaseValidator):
    """
    Validates XML-to-CSV matching quality.
    
    Checks:
    - Exact match requirements (cluster, msid, system_number)
    - Fuzzy match thresholds (Levenshtein distance)
    - Match confidence reporting
    - Low confidence flagging
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize match validator.
        
        Args:
            config: Configuration object (creates default if None)
        """
        super().__init__()
        self.config = config or Config()
        self.match_rules = self.config.validation_rules.get('matching', {})
    
    def validate(self, data) -> ValidationResult:
        """
        Validate match quality between license and usage data.
        
        Args:
            data: Tuple of (LicenseData, UsageData) to validate matching
        
        Returns:
            ValidationResult with match quality assessment
        """
        self.reset()
        
        # Validate input type
        if not isinstance(data, tuple) or len(data) != 2:
            self._add_error("MatchValidator requires tuple of (LicenseData, UsageData)")
            return self._create_result(passed=False)
        
        license_data, usage_data = data
        
        if not isinstance(license_data, LicenseData):
            self._add_error("First element must be LicenseData")
            return self._create_result(passed=False)
        
        if not isinstance(usage_data, UsageData):
            self._add_error("Second element must be UsageData")
            return self._create_result(passed=False)
        
        # Perform match validation
        match_result = self._validate_match(license_data, usage_data)
        
        # Add match result to validation
        if not match_result.matched:
            self._add_error(f"No valid match found between license and usage data")
            for issue in match_result.issues:
                self._add_warning(issue)
        elif match_result.confidence < 1.0:
            self._add_warning(f"Match confidence {match_result.confidence:.1%} - below 100%")
            self._add_info(f"Match type: {match_result.match_type}")
            for issue in match_result.issues:
                self._add_info(issue)
        else:
            self._add_info(f"Exact match (100% confidence)")
        
        # Check confidence threshold
        confidence_threshold = self.match_rules.get('reporting', {}).get('confidence_threshold', 0.9)
        if match_result.matched and match_result.confidence < confidence_threshold:
            self._add_warning(
                f"Match confidence {match_result.confidence:.1%} below threshold {confidence_threshold:.1%}"
            )
        
        return self._create_result(passed=match_result.matched)
    
    def _validate_match(self, license: LicenseData, usage: UsageData) -> MatchResult:
        """
        Validate match between license and usage data.
        
        Args:
            license: LicenseData from XML
            usage: UsageData from CSV
        
        Returns:
            MatchResult with match quality assessment
        """
        issues = []
        
        # Get exact match requirements
        exact_match_config = self.match_rules.get('exact_match', {})
        required_fields = exact_match_config.get('required_fields', ['cluster', 'msid', 'system_number'])
        case_sensitive = exact_match_config.get('case_sensitive', False)
        
        # Filter required fields to only those available in both models
        # UsageData has: msid, cluster (no system_number)
        # LicenseData has: msid, cluster, system_number
        available_fields = ['msid', 'cluster']
        required_fields = [f for f in required_fields if f in available_fields]
        
        # Check exact matches
        exact_matches = []
        
        # MSID check
        if 'msid' in required_fields:
            msid_match = self._compare_field(
                license.msid, usage.msid, 'msid', case_sensitive
            )
            if msid_match:
                exact_matches.append('msid')
            else:
                issues.append(f"MSID mismatch: license={license.msid}, usage={usage.msid}")
        
        # Cluster check
        if 'cluster' in required_fields:
            cluster_match = self._compare_field(
                license.cluster, usage.cluster, 'cluster', case_sensitive
            )
            if cluster_match:
                exact_matches.append('cluster')
            else:
                issues.append(f"Cluster mismatch: license={license.cluster}, usage={usage.cluster}")
        
        # Calculate confidence based on exact matches
        total_fields = len(required_fields)
        matched_fields = len(exact_matches)
        
        if matched_fields == total_fields:
            # Perfect match
            return MatchResult(
                matched=True,
                confidence=1.0,
                match_type='exact',
                issues=[]
            )
        
        # Try fuzzy matching if MSID didn't match exactly
        if 'msid' in required_fields and 'msid' not in exact_matches:
            fuzzy_result = self._fuzzy_match_msid(license.msid, usage.msid)
            if fuzzy_result['matched']:
                matched_fields += 1
                exact_matches.append('msid (fuzzy)')
                issues.remove(next(i for i in issues if 'MSID mismatch' in i))
                issues.append(
                    f"MSID fuzzy match: license={license.msid}, usage={usage.msid}, "
                    f"confidence={fuzzy_result['confidence']:.1%}"
                )
                
                confidence = fuzzy_result['confidence'] * (matched_fields / total_fields)
                return MatchResult(
                    matched=True,
                    confidence=confidence,
                    match_type='fuzzy',
                    issues=issues
                )
        
        # Calculate partial match confidence
        confidence = matched_fields / total_fields if total_fields > 0 else 0.0
        
        # Consider it matched if at least 1 out of 2 fields match (MSID is most important)
        matched = matched_fields >= 1 and 'msid' in exact_matches
        match_type = 'partial' if matched else 'none'
        
        return MatchResult(
            matched=matched,
            confidence=confidence,
            match_type=match_type,
            issues=issues
        )
    
    def _compare_field(
        self, 
        license_value: Optional[str], 
        usage_value: Optional[str],
        field_name: str,
        case_sensitive: bool
    ) -> bool:
        """
        Compare field values from license and usage data.
        
        Args:
            license_value: Value from license data
            usage_value: Value from usage data
            field_name: Name of field being compared
            case_sensitive: Whether comparison is case sensitive
        
        Returns:
            True if values match
        """
        # Handle None/empty values
        if license_value is None and usage_value is None:
            return True
        if license_value is None or usage_value is None:
            return False
        
        # Convert to strings
        lic_str = str(license_value).strip()
        usage_str = str(usage_value).strip()
        
        if not case_sensitive:
            lic_str = lic_str.lower()
            usage_str = usage_str.lower()
        
        return lic_str == usage_str
    
    def _fuzzy_match_msid(self, msid1: str, msid2: str) -> dict:
        """
        Perform fuzzy matching on MSID using Levenshtein distance.
        
        Args:
            msid1: First MSID
            msid2: Second MSID
        
        Returns:
            Dict with 'matched' (bool) and 'confidence' (float)
        """
        fuzzy_config = self.match_rules.get('fuzzy_match', {}).get('msid_similarity', {})
        min_confidence = fuzzy_config.get('min_confidence', 0.8)
        max_distance = fuzzy_config.get('max_distance', 2)
        
        # Calculate Levenshtein distance
        distance = self._levenshtein_distance(msid1, msid2)
        
        # Calculate confidence (normalized inverse distance)
        max_len = max(len(msid1), len(msid2))
        if max_len == 0:
            confidence = 1.0
        else:
            confidence = 1.0 - (distance / max_len)
        
        # Check thresholds
        matched = distance <= max_distance and confidence >= min_confidence
        
        return {
            'matched': matched,
            'confidence': confidence,
            'distance': distance
        }
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance between two strings.
        
        Args:
            s1: First string
            s2: Second string
        
        Returns:
            Edit distance (number of character changes)
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
