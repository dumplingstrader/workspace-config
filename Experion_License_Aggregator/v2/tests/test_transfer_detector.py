"""
Tests for Transfer Detector - License transfer candidate identification.

Tests cover:
- Transfer candidate detection using criteria
- Absolute excess threshold (e.g., ≥500 points)
- Percentage excess threshold (e.g., ≥25%)
- Value threshold (e.g., ≥$1,000)
- Priority calculation (HIGH/MEDIUM/LOW)
- Filtering by priority, cluster, license type
- Report generation
- Edge cases (no excess, no usage, no criteria)
"""

import pytest
from pathlib import Path
from v2.pipeline.transformers.transfer_detector import (
    TransferDetector,
    TransferDetectionResult
)
from v2.models.transfer import TransferCandidate


@pytest.fixture
def transfer_config():
    """Create test config with transfer rules."""
    class MockConfig:
        def __init__(self):
            self.transfer_rules = {
                'criteria': {
                    'PROCESSPOINTS': [
                        {
                            'name': 'Absolute Excess',
                            'type': 'absolute',
                            'threshold': 500,
                            'enabled': True
                        },
                        {
                            'name': 'Percentage Excess',
                            'type': 'percentage',
                            'threshold': 25,
                            'enabled': True
                        },
                        {
                            'name': 'Minimum Value',
                            'type': 'value',
                            'threshold': 1000.00,
                            'enabled': True
                        }
                    ],
                    'DIRECTSTATIONS': [
                        {
                            'name': 'Absolute Excess',
                            'type': 'absolute',
                            'threshold': 2,
                            'enabled': True
                        }
                    ]
                }
            }
    
    return MockConfig()


@pytest.fixture
def sample_enriched_licenses():
    """Sample enriched license data."""
    return [
        {
            'msid': 'M0614',
            'system_number': '60806',
            'cluster': 'Carson',
            'licensed': {
                'PROCESSPOINTS': 4750,
                'DIRECTSTATIONS': 8
            },
            'usage': {
                'PROCESSPOINTS': 108,
                'DIRECTSTATIONS': 6
            },
            'costs': {
                'PROCESSPOINTS': {'unit_cost': 45.00},
                'DIRECTSTATIONS': {'unit_cost': 6.55}
            }
        },
        {
            'msid': 'M0615',
            'system_number': '60807',
            'cluster': 'Anacortes',
            'licensed': {
                'PROCESSPOINTS': 2000
            },
            'usage': {
                'PROCESSPOINTS': 1950
            },
            'costs': {
                'PROCESSPOINTS': {'unit_cost': 45.00}
            }
        },
        {
            'msid': 'M0616',
            'system_number': '60808',
            'cluster': 'Carson',
            'licensed': {
                'PROCESSPOINTS': 1000
            },
            'usage': {
                'PROCESSPOINTS': 500
            },
            'costs': {
                'PROCESSPOINTS': {'unit_cost': 45.00}
            }
        }
    ]


class TestTransferDetectorInitialization:
    """Test transfer detector initialization."""
    
    def test_initialization_success(self, transfer_config):
        """Test successful initialization with valid config."""
        detector = TransferDetector(transfer_config)
        
        assert detector.config == transfer_config
        assert 'PROCESSPOINTS' in detector.criteria
        assert len(detector.criteria['PROCESSPOINTS']) == 3
    
    def test_initialization_missing_transfer_rules(self):
        """Test initialization fails without transfer_rules in config."""
        class MockConfig:
            pass
        
        config = MockConfig()
        
        with pytest.raises(KeyError, match="transfer_rules"):
            TransferDetector(config)


class TestAbsoluteExcessCriterion:
    """Test absolute excess threshold detection."""
    
    def test_detects_large_absolute_excess(self, transfer_config, sample_enriched_licenses):
        """Test detection of large absolute excess (≥500 points)."""
        detector = TransferDetector(transfer_config)
        
        # M0614: 4750 licensed - 108 used = 4642 excess (≥500)
        result = detector.detect([sample_enriched_licenses[0]])
        
        assert len(result.candidates) >= 1
        processpoints_candidate = next(
            c for c in result.candidates if c.license_type == 'PROCESSPOINTS'
        )
        assert processpoints_candidate.excess_quantity == 4642
        assert processpoints_candidate.priority == 'HIGH'
    
    def test_ignores_small_absolute_excess(self, transfer_config):
        """Test ignores excess below absolute threshold when other criteria also fail."""
        detector = TransferDetector(transfer_config)
        
        # Only 10 excess (< 500 threshold)
        # 10/550 = 1.8% excess (< 25% threshold)
        # 10 * $45 = $450 value (< $1000 threshold)
        # Should not qualify on ANY criterion
        enriched = [{
            'msid': 'M0617',
            'system_number': '60809',
            'cluster': 'Carson',
            'licensed': {'PROCESSPOINTS': 550},
            'usage': {'PROCESSPOINTS': 540},
            'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
        }]
        
        result = detector.detect(enriched)
        
        # Should not qualify (10 < 500, <25% excess, $450 < $1000)
        assert len(result.candidates) == 0
    
    def test_detects_directstations_threshold(self, transfer_config, sample_enriched_licenses):
        """Test different threshold for DIRECTSTATIONS (≥2)."""
        detector = TransferDetector(transfer_config)
        
        # M0614: 8 licensed - 6 used = 2 excess (≥2 threshold)
        result = detector.detect([sample_enriched_licenses[0]])
        
        directstations_candidates = [
            c for c in result.candidates if c.license_type == 'DIRECTSTATIONS'
        ]
        assert len(directstations_candidates) == 1
        assert directstations_candidates[0].excess_quantity == 2


class TestPercentageExcessCriterion:
    """Test percentage excess threshold detection."""
    
    def test_detects_low_utilization(self, transfer_config, sample_enriched_licenses):
        """Test detection of low utilization (≤75%, i.e., ≥25% excess)."""
        detector = TransferDetector(transfer_config)
        
        # M0616: 1000 licensed - 500 used = 50% utilization (50% excess ≥ 25%)
        result = detector.detect([sample_enriched_licenses[2]])
        
        assert len(result.candidates) >= 1
        candidate = result.candidates[0]
        assert candidate.utilization_percentage() == 50.0
        assert candidate.excess_percentage == 50.0
    
    def test_ignores_high_utilization(self, transfer_config, sample_enriched_licenses):
        """Test ignores high utilization when all criteria fail."""
        detector = TransferDetector(transfer_config)
        
        # Create record that fails ALL criteria:
        # - 10 excess (< 500 absolute threshold)
        # - 10/2000 = 0.5% excess (< 25% percentage threshold)
        # - 10 * $45 = $450 (< $1000 value threshold)
        enriched = [{
            'msid': 'M0615',
            'system_number': '60807',
            'cluster': 'Anacortes',
            'licensed': {'PROCESSPOINTS': 2000},
            'usage': {'PROCESSPOINTS': 1990},
            'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
        }]
        
        result = detector.detect(enriched)
        
        # Should not qualify (fails all three criteria)
        assert len(result.candidates) == 0


class TestValueThresholdCriterion:
    """Test minimum value threshold detection."""
    
    def test_detects_high_value_excess(self, transfer_config):
        """Test detection of high-value excess (≥$1,000)."""
        detector = TransferDetector(transfer_config)
        
        # 100 excess * $45 = $4,500 (≥$1,000)
        enriched = [{
            'msid': 'M0618',
            'system_number': '60810',
            'cluster': 'Carson',
            'licensed': {'PROCESSPOINTS': 600},
            'usage': {'PROCESSPOINTS': 500},
            'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
        }]
        
        result = detector.detect(enriched)
        
        assert len(result.candidates) == 1
        assert result.candidates[0].excess_value == 4500.00
    
    def test_ignores_low_value_excess(self, transfer_config):
        """Test ignores excess below value threshold."""
        detector = TransferDetector(transfer_config)
        
        # Only 10 excess * $45 = $450 (< $1,000)
        enriched = [{
            'msid': 'M0619',
            'system_number': '60811',
            'cluster': 'Carson',
            'licensed': {'PROCESSPOINTS': 510},
            'usage': {'PROCESSPOINTS': 500},
            'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
        }]
        
        result = detector.detect(enriched)
        
        # Should not qualify (10 < 500, <25% excess, $450 < $1000)
        assert len(result.candidates) == 0


class TestPriorityCalculation:
    """Test priority level calculation."""
    
    def test_high_priority_threshold(self, transfer_config):
        """Test HIGH priority for excess ≥$10,000."""
        detector = TransferDetector(transfer_config)
        
        # 4642 excess * $45 = $208,890 (≥$10,000)
        enriched = [{
            'msid': 'M0614',
            'system_number': '60806',
            'cluster': 'Carson',
            'licensed': {'PROCESSPOINTS': 4750},
            'usage': {'PROCESSPOINTS': 108},
            'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
        }]
        
        result = detector.detect(enriched)
        
        assert len(result.candidates) == 1
        assert result.candidates[0].priority == 'HIGH'
        assert result.high_priority_count == 1
    
    def test_medium_priority_threshold(self, transfer_config):
        """Test MEDIUM priority for $1,000 ≤ excess < $10,000."""
        detector = TransferDetector(transfer_config)
        
        # 100 excess * $45 = $4,500 (≥$1,000 but <$10,000)
        enriched = [{
            'msid': 'M0620',
            'system_number': '60812',
            'cluster': 'Carson',
            'licensed': {'PROCESSPOINTS': 600},
            'usage': {'PROCESSPOINTS': 500},
            'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
        }]
        
        result = detector.detect(enriched)
        
        assert len(result.candidates) == 1
        assert result.candidates[0].priority == 'MEDIUM'
    
    def test_low_priority_threshold(self, transfer_config):
        """Test LOW priority for excess < $1,000."""
        detector = TransferDetector(transfer_config)
        
        # 10 excess * $6.55 = $65.50 (< $1,000)
        # But meets absolute threshold for DIRECTSTATIONS (10 ≥ 2)
        enriched = [{
            'msid': 'M0621',
            'system_number': '60813',
            'cluster': 'Carson',
            'licensed': {'DIRECTSTATIONS': 15},
            'usage': {'DIRECTSTATIONS': 5},
            'costs': {'DIRECTSTATIONS': {'unit_cost': 6.55}}
        }]
        
        result = detector.detect(enriched)
        
        assert len(result.candidates) == 1
        assert result.candidates[0].priority == 'LOW'


class TestMultipleLicenseTypes:
    """Test handling multiple license types per system."""
    
    def test_detects_multiple_types_per_system(self, transfer_config, sample_enriched_licenses):
        """Test detects multiple qualifying license types in one system."""
        detector = TransferDetector(transfer_config)
        
        # M0614 has both PROCESSPOINTS and DIRECTSTATIONS with excess
        result = detector.detect([sample_enriched_licenses[0]])
        
        m0614_candidates = [c for c in result.candidates if c.msid == 'M0614']
        assert len(m0614_candidates) == 2  # PROCESSPOINTS + DIRECTSTATIONS
        
        license_types = {c.license_type for c in m0614_candidates}
        assert 'PROCESSPOINTS' in license_types
        assert 'DIRECTSTATIONS' in license_types
    
    def test_ignores_types_without_excess(self, transfer_config):
        """Test ignores license types with no excess."""
        detector = TransferDetector(transfer_config)
        
        enriched = [{
            'msid': 'M0622',
            'system_number': '60814',
            'cluster': 'Carson',
            'licensed': {
                'PROCESSPOINTS': 4750,  # Qualifies
                'SCADAPOINTS': 100      # No excess (100 - 100)
            },
            'usage': {
                'PROCESSPOINTS': 108,
                'SCADAPOINTS': 100
            },
            'costs': {
                'PROCESSPOINTS': {'unit_cost': 45.00},
                'SCADAPOINTS': {'unit_cost': 48.00}
            }
        }]
        
        result = detector.detect(enriched)
        
        # Only PROCESSPOINTS should qualify
        assert len(result.candidates) == 1
        assert result.candidates[0].license_type == 'PROCESSPOINTS'


class TestStatisticsCalculation:
    """Test aggregate statistics calculation."""
    
    def test_calculates_total_excess_value(self, transfer_config, sample_enriched_licenses):
        """Test calculates total excess value across all candidates."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        
        # Calculate expected total
        expected_total = sum(c.excess_value for c in result.candidates)
        assert result.total_excess_value == expected_total
        assert result.total_excess_value > 0
    
    def test_tracks_systems_analyzed(self, transfer_config, sample_enriched_licenses):
        """Test tracks number of systems analyzed."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        
        assert result.systems_analyzed == 3
    
    def test_license_type_stats(self, transfer_config, sample_enriched_licenses):
        """Test tracks candidates by license type."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        
        assert 'PROCESSPOINTS' in result.stats
        assert result.stats['PROCESSPOINTS'] >= 1


class TestFilteringMethods:
    """Test candidate filtering methods."""
    
    def test_filter_by_priority(self, transfer_config, sample_enriched_licenses):
        """Test get_candidates_by_priority()."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        high_priority = detector.get_candidates_by_priority(result, 'HIGH')
        
        assert all(c.priority == 'HIGH' for c in high_priority)
        assert len(high_priority) > 0
    
    def test_filter_by_cluster(self, transfer_config, sample_enriched_licenses):
        """Test get_candidates_by_cluster()."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        carson_candidates = detector.get_candidates_by_cluster(result, 'Carson')
        
        assert all(c.cluster == 'Carson' for c in carson_candidates)
        assert len(carson_candidates) > 0
    
    def test_filter_by_license_type(self, transfer_config, sample_enriched_licenses):
        """Test get_candidates_by_license_type()."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        processpoints = detector.get_candidates_by_license_type(result, 'PROCESSPOINTS')
        
        assert all(c.license_type == 'PROCESSPOINTS' for c in processpoints)
        assert len(processpoints) > 0


class TestReportGeneration:
    """Test transfer candidate report generation."""
    
    def test_generate_report(self, transfer_config, sample_enriched_licenses):
        """Test generate_transfer_report()."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        report = detector.generate_transfer_report(result)
        
        assert "Transfer Candidate Report" in report
        assert "Total Candidates:" in report
        assert "Total Excess Value:" in report
        assert "High Priority:" in report
    
    def test_report_includes_candidate_details(self, transfer_config, sample_enriched_licenses):
        """Test report includes candidate details."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        report = detector.generate_transfer_report(result)
        
        # Should include MSID
        assert "M0614" in report or "M0616" in report
        
        # Should include license type
        assert "PROCESSPOINTS" in report
    
    def test_report_groups_by_priority(self, transfer_config, sample_enriched_licenses):
        """Test report groups candidates by priority."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect(sample_enriched_licenses)
        report = detector.generate_transfer_report(result)
        
        # Check priority sections exist
        if result.high_priority_count > 0:
            assert "HIGH PRIORITY CANDIDATES:" in report


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_licensed_dict(self, transfer_config):
        """Test handles systems with no licenses."""
        detector = TransferDetector(transfer_config)
        
        enriched = [{
            'msid': 'M0623',
            'system_number': '60815',
            'cluster': 'Carson',
            'licensed': {},
            'usage': {},
            'costs': {}
        }]
        
        result = detector.detect(enriched)
        
        assert len(result.candidates) == 0
        assert result.total_excess_value == 0.0
    
    def test_no_usage_data(self, transfer_config):
        """Test handles missing usage data."""
        detector = TransferDetector(transfer_config)
        
        enriched = [{
            'msid': 'M0624',
            'system_number': '60816',
            'cluster': 'Carson',
            'licensed': {'PROCESSPOINTS': 4750},
            'usage': {},  # No usage data
            'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
        }]
        
        result = detector.detect(enriched)
        
        # Should detect as excess (0 used)
        assert len(result.candidates) == 1
        assert result.candidates[0].used_quantity == 0
        assert result.candidates[0].excess_quantity == 4750
    
    def test_no_cost_data(self, transfer_config):
        """Test handles missing cost data."""
        detector = TransferDetector(transfer_config)
        
        enriched = [{
            'msid': 'M0625',
            'system_number': '60817',
            'cluster': 'Carson',
            'licensed': {'PROCESSPOINTS': 4750},
            'usage': {'PROCESSPOINTS': 108},
            'costs': {}  # No cost data
        }]
        
        result = detector.detect(enriched)
        
        # Should still detect based on absolute/percentage, value will be 0
        assert len(result.candidates) >= 1
        assert result.candidates[0].unit_price == 0.0
        assert result.candidates[0].excess_value == 0.0
    
    def test_default_criteria_when_none_defined(self, transfer_config):
        """Test uses default criteria for license types without rules."""
        detector = TransferDetector(transfer_config)
        
        # SCADAPOINTS not in criteria
        enriched = [{
            'msid': 'M0626',
            'system_number': '60818',
            'cluster': 'Carson',
            'licensed': {'SCADAPOINTS': 2000},
            'usage': {'SCADAPOINTS': 500},
            'costs': {'SCADAPOINTS': {'unit_cost': 48.00}}
        }]
        
        result = detector.detect(enriched)
        
        # Should qualify on default criteria (1500 ≥ 500, 75% excess ≥ 25%, $72,000 ≥ $1000)
        assert len(result.candidates) == 1
    
    def test_empty_enriched_list(self, transfer_config):
        """Test handles empty input list."""
        detector = TransferDetector(transfer_config)
        
        result = detector.detect([])
        
        assert len(result.candidates) == 0
        assert result.total_excess_value == 0.0
        assert result.systems_analyzed == 0
    
    def test_sorting_by_priority_and_value(self, transfer_config):
        """Test candidates sorted by priority then value."""
        detector = TransferDetector(transfer_config)
        
        enriched = [
            {
                'msid': 'M0627',
                'system_number': '60819',
                'cluster': 'Carson',
                'licensed': {'PROCESSPOINTS': 600},
                'usage': {'PROCESSPOINTS': 500},
                'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
            },
            {
                'msid': 'M0628',
                'system_number': '60820',
                'cluster': 'Carson',
                'licensed': {'PROCESSPOINTS': 4750},
                'usage': {'PROCESSPOINTS': 108},
                'costs': {'PROCESSPOINTS': {'unit_cost': 45.00}}
            }
        ]
        
        result = detector.detect(enriched)
        
        # HIGH priority should come before MEDIUM
        assert result.candidates[0].priority == 'HIGH'
        assert result.candidates[1].priority == 'MEDIUM'
