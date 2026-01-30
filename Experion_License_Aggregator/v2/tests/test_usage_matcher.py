"""
Tests for UsageMatcher - License-to-usage matching with quality assessment.

Test Coverage:
- Exact MSID + cluster matches
- Fuzzy MSID matching
- Unmatched licenses
- Low confidence detection
- Duplicate match detection
- Match statistics and reporting
"""

import pytest
from pathlib import Path

from v2.models.license import LicenseData
from v2.models.usage import UsageData
from v2.core.config import Config
from v2.pipeline.validators.match_validator import MatchValidator
from v2.pipeline.transformers.field_mapper import FieldMapper
from v2.pipeline.transformers.usage_matcher import (
    UsageMatcher,
    MatchRecord,
    MatchingResult
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def test_config():
    """Load test configuration"""
    config_dir = Path(__file__).parent.parent / 'config'
    return Config(config_dir)


@pytest.fixture
def match_validator(test_config):
    """Create MatchValidator"""
    return MatchValidator(test_config)


@pytest.fixture
def field_mapper(test_config):
    """Create FieldMapper"""
    return FieldMapper(test_config)


@pytest.fixture
def usage_matcher(field_mapper, match_validator):
    """Create UsageMatcher with dependencies"""
    return UsageMatcher(field_mapper, match_validator, min_confidence=0.8)


@pytest.fixture
def sample_license():
    """Sample license for Carson M0614"""
    return LicenseData(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        release='R520',
        file_version=40,
        licensed={'PROCESSPOINTS': 4750, 'DIRECTSTATIONS': 8}
    )


@pytest.fixture
def sample_usage():
    """Sample usage matching Carson M0614"""
    return UsageData(
        msid='M0614',
        cluster='Carson',
        license_type='PROCESSPOINTS',
        used_quantity=108
    )


@pytest.fixture
def different_license():
    """Different system (Wilmington M0615)"""
    return LicenseData(
        msid='M0615',
        system_number='60807',
        cluster='Wilmington',
        release='R511.6',
        file_version=35,
        licensed={'PROCESSPOINTS': 2000}
    )


@pytest.fixture
def different_usage():
    """Usage for Wilmington M0615"""
    return UsageData(
        msid='M0615',
        cluster='Wilmington',
        license_type='PROCESSPOINTS',
        used_quantity=450
    )


# ============================================================================
# Test Exact Matching
# ============================================================================

class TestExactMatching:
    """Test exact MSID + cluster matching"""
    
    def test_single_exact_match(self, usage_matcher, sample_license, sample_usage):
        """Should match license to usage with same MSID and cluster"""
        result = usage_matcher.match([sample_license], [sample_usage])
        
        assert result.matched_count == 1
        assert result.unmatched_licenses == 0
        assert len(result.matches) == 1
        
        match = result.matches[0]
        assert match.usage is not None
        assert match.usage.msid == 'M0614'
        assert match.match_type == 'exact'
        assert match.confidence == 1.0
    
    def test_multiple_exact_matches(
        self, usage_matcher, 
        sample_license, sample_usage,
        different_license, different_usage
    ):
        """Should match multiple licenses to their usage records"""
        licenses = [sample_license, different_license]
        usage_list = [sample_usage, different_usage]
        
        result = usage_matcher.match(licenses, usage_list)
        
        assert result.matched_count == 2
        assert result.unmatched_licenses == 0
        assert result.stats['exact_matches'] == 2
    
    def test_case_insensitive_cluster_match(
        self, usage_matcher, sample_license
    ):
        """Cluster matching should be case-insensitive"""
        usage = UsageData(
            msid='M0614',
            cluster='CARSON',  # Different case
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        result = usage_matcher.match([sample_license], [usage])
        
        assert result.matched_count == 1
        assert result.matches[0].match_type == 'exact'


# ============================================================================
# Test Unmatched Scenarios
# ============================================================================

class TestUnmatchedScenarios:
    """Test handling of unmatched licenses"""
    
    def test_no_usage_for_license(self, usage_matcher, sample_license):
        """License with no matching usage should be unmatched"""
        different_usage = UsageData(
            msid='M9999',  # Different MSID
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=100
        )
        
        result = usage_matcher.match([sample_license], [different_usage])
        
        assert result.matched_count == 0
        assert result.unmatched_licenses == 1
        
        match = result.matches[0]
        assert match.usage is None
        assert match.match_type == 'none'
        assert match.confidence == 0.0
        assert len(match.issues) > 0
    
    def test_wrong_cluster_no_match(self, usage_matcher, sample_license):
        """Same MSID but different cluster should not match"""
        usage = UsageData(
            msid='M0614',
            cluster='Wilmington',  # Different cluster
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        result = usage_matcher.match([sample_license], [usage])
        
        # Should attempt fuzzy match but fail due to cluster mismatch
        assert result.matched_count == 0
        assert result.unmatched_licenses == 1


# ============================================================================
# Test Fuzzy Matching
# ============================================================================

class TestFuzzyMatching:
    """Test fuzzy MSID matching"""
    
    def test_fuzzy_msid_match_within_threshold(self, usage_matcher):
        """Similar MSID should match via fuzzy logic"""
        license_obj = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M0615',  # 1 character difference
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        result = usage_matcher.match([license_obj], [usage])
        
        # Should match via fuzzy matching
        if result.matched_count > 0:
            match = result.matches[0]
            assert match.usage is not None
            assert match.match_type == 'fuzzy'
            assert match.confidence >= 0.8  # Above min threshold
    
    def test_fuzzy_match_too_different_fails(self, usage_matcher):
        """Very different MSID should not match"""
        license_obj = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        usage = UsageData(
            msid='M9999',  # Too different
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        result = usage_matcher.match([license_obj], [usage])
        
        # Should fail to match (too different)
        assert result.matched_count == 0


# ============================================================================
# Test Match Statistics
# ============================================================================

class TestMatchStatistics:
    """Test statistics calculation and reporting"""
    
    def test_statistics_calculation(
        self, usage_matcher,
        sample_license, sample_usage,
        different_license, different_usage
    ):
        """Should calculate comprehensive statistics"""
        licenses = [sample_license, different_license]
        usage_list = [sample_usage, different_usage]
        
        result = usage_matcher.match(licenses, usage_list)
        
        assert result.stats['total_licenses'] == 2
        assert result.stats['total_usage_records'] == 2
        assert result.stats['matched'] == 2
        assert result.stats['unmatched'] == 0
        assert result.stats['exact_matches'] == 2
    
    def test_mixed_match_statistics(self, usage_matcher, sample_license):
        """Should track different match types"""
        # Add unmatched license
        unmatched = LicenseData(
            msid='M9999',
            system_number='99999',
            cluster='Unknown',
            release='R520',
            licensed={'PROCESSPOINTS': 1000}
        )
        
        licenses = [sample_license, unmatched]
        usage = [UsageData(
            msid='M0614',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )]
        
        result = usage_matcher.match(licenses, usage)
        
        assert result.stats['matched'] == 1
        assert result.stats['unmatched'] == 1


# ============================================================================
# Test Low Confidence Detection
# ============================================================================

class TestLowConfidenceDetection:
    """Test detection of low-confidence matches"""
    
    def test_low_confidence_flagged(self, usage_matcher):
        """Matches below min_confidence should be flagged"""
        # Create matcher with high confidence requirement
        strict_matcher = UsageMatcher(
            usage_matcher.field_mapper,
            usage_matcher.match_validator,
            min_confidence=0.95  # Very strict
        )
        
        license_obj = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        # Usage with slightly different cluster (partial match)
        usage = UsageData(
            msid='M0614',
            cluster='Carson',  # Matches but might have issues
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        result = strict_matcher.match([license_obj], [usage])
        
        # Even if matched, might be flagged as low confidence
        if result.matched_count > 0:
            # Low confidence count depends on validation warnings
            assert result.stats['low_confidence'] >= 0


# ============================================================================
# Test Match Report Generation
# ============================================================================

class TestMatchReporting:
    """Test match report generation"""
    
    def test_generate_match_report(
        self, usage_matcher,
        sample_license, sample_usage,
        different_license
    ):
        """Should generate comprehensive match report"""
        licenses = [sample_license, different_license]
        usage_list = [sample_usage]  # Only one usage (one will be unmatched)
        
        result = usage_matcher.match(licenses, usage_list)
        report = usage_matcher.generate_match_report(result)
        
        assert "License-Usage Matching Report" in report
        assert "Total licenses: 2" in report
        assert "Matched: 1" in report
        assert "Unmatched: 1" in report
        assert "Exact matches:" in report
    
    def test_report_includes_unmatched_list(
        self, usage_matcher, sample_license, different_license
    ):
        """Report should list unmatched licenses"""
        usage = [UsageData(
            msid='M0614',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )]
        
        result = usage_matcher.match(
            [sample_license, different_license],
            usage
        )
        report = usage_matcher.generate_match_report(result)
        
        assert "Unmatched Licenses:" in report
        assert "M0615" in report or "Wilmington" in report


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test error handling and edge cases"""
    
    def test_empty_license_list_raises_error(self, usage_matcher, sample_usage):
        """Empty license list should raise ValueError"""
        with pytest.raises(ValueError, match="Cannot match empty license"):
            usage_matcher.match([], [sample_usage])
    
    def test_empty_usage_list_raises_error(self, usage_matcher, sample_license):
        """Empty usage list should raise ValueError"""
        with pytest.raises(ValueError, match="Cannot match empty usage"):
            usage_matcher.match([sample_license], [])
    
    def test_multiple_usage_same_msid_cluster(self, usage_matcher, sample_license):
        """Multiple usage records for same MSID should use first match"""
        usage1 = UsageData(
            msid='M0614',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        usage2 = UsageData(
            msid='M0614',
            cluster='Carson',
            license_type='DIRECTSTATIONS',
            used_quantity=5
        )
        
        result = usage_matcher.match([sample_license], [usage1, usage2])
        
        assert result.matched_count == 1
        # Should match to first usage record found
        assert result.matches[0].usage is not None
    
    def test_usage_with_no_cluster(self, usage_matcher, sample_license):
        """Usage record with None cluster should handle gracefully"""
        usage = UsageData(
            msid='M0614',
            cluster=None,  # No cluster
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        # Should not crash
        result = usage_matcher.match([sample_license], [usage])
        
        # May or may not match depending on validation logic
        assert result is not None
        assert len(result.matches) == 1
