"""
Tests for Deduplicator - Version-based duplicate removal.

Test Coverage:
- Basic deduplication (single duplicate)
- Multiple duplicates per system
- No duplicates (passthrough)
- Version conflict reporting
- Edge cases (empty input, single license)
- Statistics validation
"""

import pytest
from datetime import datetime

from v2.models.license import LicenseData
from v2.pipeline.transformers.deduplicator import Deduplicator, DeduplicationResult


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_license_v29():
    """Sample license with version 29"""
    return LicenseData(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        release='R520',
        file_version=29,
        file_path='M0614_R520_x_60806_29.xml',
        licensed={'PROCESSPOINTS': 4750}
    )


@pytest.fixture
def sample_license_v40():
    """Same system as v29 but version 40 (should win)"""
    return LicenseData(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        release='R520',
        file_version=40,
        file_path='M0614_R520_x_60806_40.xml',
        licensed={'PROCESSPOINTS': 4750}
    )


@pytest.fixture
def sample_license_v28():
    """Same system but oldest version"""
    return LicenseData(
        msid='M0614',
        system_number='60806',
        cluster='Carson',
        release='R520',
        file_version=28,
        file_path='M0614_R520_x_60806_28.xml',
        licensed={'PROCESSPOINTS': 4750}
    )


@pytest.fixture
def different_system():
    """Different system (no conflict)"""
    return LicenseData(
        msid='M0615',
        system_number='60807',
        cluster='Carson',
        release='R511.6',
        file_version=35,
        file_path='M0615_R511.6_x_60807_35.xml',
        licensed={'PROCESSPOINTS': 2000}
    )


# ============================================================================
# Test Deduplication - Basic Scenarios
# ============================================================================

class TestDeduplicatorBasic:
    """Test core deduplication functionality"""
    
    def test_single_duplicate_highest_version_wins(self, sample_license_v29, sample_license_v40):
        """Highest version should be kept when duplicates exist"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v29, sample_license_v40]
        
        result = deduplicator.deduplicate(licenses)
        
        # Assertions
        assert len(result.unique_licenses) == 1
        assert result.unique_licenses[0].file_version == 40
        assert len(result.duplicates_removed) == 1
        assert result.duplicates_removed[0].file_version == 29
    
    def test_multiple_duplicates_highest_wins(
        self, sample_license_v28, sample_license_v29, sample_license_v40
    ):
        """With 3 versions, highest version should win"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v28, sample_license_v40, sample_license_v29]  # Shuffled
        
        result = deduplicator.deduplicate(licenses)
        
        assert len(result.unique_licenses) == 1
        assert result.unique_licenses[0].file_version == 40
        assert len(result.duplicates_removed) == 2
        
        # Verify all removed versions are correct
        removed_versions = {lic.file_version for lic in result.duplicates_removed}
        assert removed_versions == {28, 29}
    
    def test_no_duplicates_returns_all(self, sample_license_v40, different_system):
        """When no duplicates, all licenses should be returned"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v40, different_system]
        
        result = deduplicator.deduplicate(licenses)
        
        assert len(result.unique_licenses) == 2
        assert len(result.duplicates_removed) == 0
        assert result.stats['systems_with_conflicts'] == 0
    
    def test_single_license_passthrough(self, sample_license_v40):
        """Single license should pass through unchanged"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v40]
        
        result = deduplicator.deduplicate(licenses)
        
        assert len(result.unique_licenses) == 1
        assert result.unique_licenses[0] == sample_license_v40
        assert len(result.duplicates_removed) == 0
    
    def test_empty_list_raises_error(self):
        """Empty license list should raise ValueError"""
        deduplicator = Deduplicator()
        
        with pytest.raises(ValueError, match="Cannot deduplicate empty"):
            deduplicator.deduplicate([])


# ============================================================================
# Test Statistics Reporting
# ============================================================================

class TestDeduplicatorStatistics:
    """Test statistics and reporting functionality"""
    
    def test_stats_with_conflicts(self, sample_license_v29, sample_license_v40):
        """Stats should correctly count conflicts"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v29, sample_license_v40]
        
        result = deduplicator.deduplicate(licenses)
        
        assert result.stats['total_input'] == 2
        assert result.stats['unique_systems'] == 1
        assert result.stats['duplicates_removed'] == 1
        assert result.stats['systems_with_conflicts'] == 1
    
    def test_stats_without_conflicts(self, sample_license_v40, different_system):
        """Stats should show no conflicts when systems are unique"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v40, different_system]
        
        result = deduplicator.deduplicate(licenses)
        
        assert result.stats['total_input'] == 2
        assert result.stats['unique_systems'] == 2
        assert result.stats['duplicates_removed'] == 0
        assert result.stats['systems_with_conflicts'] == 0
    
    def test_conflicts_dict_structure(
        self, sample_license_v28, sample_license_v29, sample_license_v40
    ):
        """Conflicts dict should map unique_key to sorted version list"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v28, sample_license_v29, sample_license_v40]
        
        result = deduplicator.deduplicate(licenses)
        
        # Check conflict structure
        assert len(result.conflicts) == 1
        key = ('Carson', 'M0614', '60806')
        assert key in result.conflicts
        assert result.conflicts[key] == [40, 29, 28]  # Sorted descending


# ============================================================================
# Test Version Conflict Detection
# ============================================================================

class TestVersionConflictDetection:
    """Test conflict detection without deduplication"""
    
    def test_get_version_conflicts_with_duplicates(
        self, sample_license_v29, sample_license_v40
    ):
        """Should identify systems with multiple versions"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v29, sample_license_v40]
        
        conflicts = deduplicator.get_version_conflicts(licenses)
        
        key = ('Carson', 'M0614', '60806')
        assert key in conflicts
        assert conflicts[key] == [40, 29]  # Sorted descending
    
    def test_get_version_conflicts_no_duplicates(
        self, sample_license_v40, different_system
    ):
        """Should return empty dict when no conflicts"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v40, different_system]
        
        conflicts = deduplicator.get_version_conflicts(licenses)
        
        assert len(conflicts) == 0
    
    def test_get_version_conflicts_three_versions(
        self, sample_license_v28, sample_license_v29, sample_license_v40
    ):
        """Should detect all version conflicts"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v28, sample_license_v29, sample_license_v40]
        
        conflicts = deduplicator.get_version_conflicts(licenses)
        
        key = ('Carson', 'M0614', '60806')
        assert conflicts[key] == [40, 29, 28]


# ============================================================================
# Test Conflict Report Generation
# ============================================================================

class TestConflictReporting:
    """Test human-readable conflict report generation"""
    
    def test_generate_conflict_report_with_conflicts(
        self, sample_license_v29, sample_license_v40
    ):
        """Report should list version conflicts"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v29, sample_license_v40]
        result = deduplicator.deduplicate(licenses)
        
        report = deduplicator.generate_conflict_report(result)
        
        # Check report structure
        assert "Version Conflicts Report" in report
        assert "Total systems: 1" in report
        assert "Systems with conflicts: 1" in report
        assert "Carson/M0614/60806" in report
        assert "kept v40" in report
    
    def test_generate_conflict_report_no_conflicts(
        self, sample_license_v40, different_system
    ):
        """Report should indicate no conflicts"""
        deduplicator = Deduplicator()
        licenses = [sample_license_v40, different_system]
        result = deduplicator.deduplicate(licenses)
        
        report = deduplicator.generate_conflict_report(result)
        
        assert "No version conflicts detected" in report
        assert "Total systems: 2" in report
        assert "Systems with conflicts: 0" in report
    
    def test_conflict_report_multiple_systems(
        self, sample_license_v29, sample_license_v40
    ):
        """Report should handle multiple conflicting systems"""
        # Create second system with conflict
        lic1 = LicenseData(
            msid='M0615',
            system_number='60807',
            cluster='Wilmington',
            release='R511.6',
            file_version=30,
            licensed={'PROCESSPOINTS': 2000}
        )
        lic2 = LicenseData(
            msid='M0615',
            system_number='60807',
            cluster='Wilmington',
            release='R511.6',
            file_version=35,
            licensed={'PROCESSPOINTS': 2000}
        )
        
        deduplicator = Deduplicator()
        licenses = [sample_license_v29, sample_license_v40, lic1, lic2]
        result = deduplicator.deduplicate(licenses)
        
        report = deduplicator.generate_conflict_report(result)
        
        # Both systems should be in report
        assert "Carson/M0614/60806" in report
        assert "Wilmington/M0615/60807" in report
        assert "Systems with conflicts: 2" in report


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestDeduplicatorEdgeCases:
    """Test edge cases and error handling"""
    
    def test_same_version_twice_keeps_one(self, sample_license_v40):
        """Duplicate of same version should deduplicate to one"""
        deduplicator = Deduplicator()
        # Create exact duplicate
        lic_copy = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            file_version=40,
            file_path='duplicate.xml',
            licensed={'PROCESSPOINTS': 4750}
        )
        licenses = [sample_license_v40, lic_copy]
        
        result = deduplicator.deduplicate(licenses)
        
        # Should keep one, remove one
        assert len(result.unique_licenses) == 1
        assert result.unique_licenses[0].file_version == 40
        assert len(result.duplicates_removed) == 1
    
    def test_different_clusters_not_duplicates(self, sample_license_v40):
        """Same MSID/system_number but different cluster = different systems"""
        wilmington_license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Wilmington',  # Different cluster
            release='R520',
            file_version=40,
            licensed={'PROCESSPOINTS': 4750}
        )
        
        deduplicator = Deduplicator()
        licenses = [sample_license_v40, wilmington_license]
        result = deduplicator.deduplicate(licenses)
        
        # Different clusters = different systems
        assert len(result.unique_licenses) == 2
        assert len(result.duplicates_removed) == 0
    
    def test_large_batch_deduplication(self):
        """Test performance with large number of licenses"""
        deduplicator = Deduplicator()
        
        # Create 100 licenses (10 systems x 10 versions each)
        licenses = []
        for system_num in range(10):
            for version in range(10):
                lic = LicenseData(
                    msid=f'M{system_num:04d}',
                    system_number=f'6080{system_num}',
                    cluster='Carson',
                    release='R520',
                    file_version=version,
                    licensed={'PROCESSPOINTS': 1000}
                )
                licenses.append(lic)
        
        result = deduplicator.deduplicate(licenses)
        
        # Should have 10 unique systems (highest version of each)
        assert len(result.unique_licenses) == 10
        assert len(result.duplicates_removed) == 90
        assert result.stats['systems_with_conflicts'] == 10
        
        # All kept versions should be 9 (highest)
        for lic in result.unique_licenses:
            assert lic.file_version == 9
