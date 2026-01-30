"""
Tests for Cost Calculator - Multi-source pricing cascade.

Tests cover:
- Pricing cascade (MPC 2026 → Honeywell → Placeholder)
- Cost calculation formula: (quantity / per) * unit_cost
- Rounding to cents
- Minimum charge enforcement
- Pricing source tracking
- Unknown license types
- Multiple license types in single system
- Edge cases (zero quantities, missing catalogs)
"""

import pytest
import json
from pathlib import Path
from v2.pipeline.transformers.cost_calculator import (
    CostCalculator,
    CostResult,
    LicenseCostSummary
)
from v2.core.config import Config


@pytest.fixture
def cost_config(tmp_path):
    """Create test config with cost catalogs."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Create MPC 2026 catalog (priority 1)
    mpc_catalog = {
        "PROCESSPOINTS": {
            "unit_cost": 45.00,
            "per": 50,
            "category": "Control Points",
            "description": "MPC 2026 confirmed pricing"
        },
        "SCADAPOINTS": {
            "unit_cost": 48.00,
            "per": 100,
            "category": "SCADA Points",
            "description": "MPC 2026 SCADA pricing"
        }
    }
    with open(config_dir / "cost_catalog_mpc_2026.json", 'w') as f:
        json.dump(mpc_catalog, f)
    
    # Create Honeywell Baseline catalog (priority 2)
    honeywell_catalog = {
        "DIRECTSTATIONS": {
            "unit_cost": 6.55,
            "per": 1,
            "category": "Operator Stations",
            "description": "Honeywell baseline station pricing"
        },
        "PROCESSPOINTS": {
            "unit_cost": 42.50,
            "per": 50,
            "category": "Control Points",
            "description": "Honeywell fallback pricing (should not be used)"
        }
    }
    with open(config_dir / "cost_catalog.json", 'w') as f:
        json.dump(honeywell_catalog, f)
    
    # Create cost rules
    cost_rules = {
        "pricing_strategy": [
            {
                "name": "MPC 2026 Confirmed",
                "priority": 1,
                "source": "cost_catalog_mpc_2026.json"
            },
            {
                "name": "Honeywell Baseline",
                "priority": 2,
                "source": "cost_catalog.json"
            },
            {
                "name": "Placeholder",
                "priority": 3,
                "value": 100.00,
                "description": "Default for unknown types"
            }
        ],
        "calculation": {
            "round_to_cents": True,
            "minimum_charge": 0.01,
            "include_zero_costs": False
        }
    }
    with open(config_dir / "cost_rules.yaml", 'w') as f:
        import yaml
        yaml.safe_dump(cost_rules, f)
    
    # Create minimal config object without full Config initialization
    class MockConfig:
        def __init__(self, config_dir, cost_rules):
            self.config_dir = config_dir
            self.cost_rules = cost_rules
    
    return MockConfig(config_dir, cost_rules)


class TestCostCalculatorInitialization:
    """Test cost calculator initialization and catalog loading."""
    
    def test_initialization_success(self, cost_config):
        """Test successful initialization with valid config."""
        calculator = CostCalculator(cost_config)
        
        assert calculator.config == cost_config
        assert len(calculator.catalogs) == 2  # MPC 2026 + Honeywell
        assert "MPC 2026 Confirmed" in calculator.catalogs
        assert "Honeywell Baseline" in calculator.catalogs
    
    def test_initialization_missing_cost_rules(self):
        """Test initialization fails without cost_rules in config."""
        class MockConfig:
            pass
        
        config = MockConfig()
        
        with pytest.raises(KeyError, match="cost_rules"):
            CostCalculator(config)
    
    def test_missing_catalog_file_creates_empty(self, cost_config, tmp_path):
        """Test missing catalog file results in empty catalog dict."""
        # Remove one catalog file
        (tmp_path / "config" / "cost_catalog_mpc_2026.json").unlink()
        
        calculator = CostCalculator(cost_config)
        
        # Should have empty dict for missing catalog
        assert "MPC 2026 Confirmed" in calculator.catalogs
        assert calculator.catalogs["MPC 2026 Confirmed"] == {}


class TestPricingCascade:
    """Test multi-source pricing cascade logic."""
    
    def test_priority_1_mpc_2026_used(self, cost_config):
        """Test MPC 2026 catalog used when available (priority 1)."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"PROCESSPOINTS": 4750}
        summary = calculator.calculate_license_cost(licensed, "M0614")
        
        assert len(summary.costs) == 1
        cost = summary.costs[0]
        assert cost.pricing_source == "MPC 2026 Confirmed"
        assert cost.unit_cost == 45.00
        assert cost.per == 50
    
    def test_priority_2_honeywell_fallback(self, cost_config):
        """Test Honeywell used when not in MPC 2026."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"DIRECTSTATIONS": 8}
        summary = calculator.calculate_license_cost(licensed, "M0615")
        
        assert len(summary.costs) == 1
        cost = summary.costs[0]
        assert cost.pricing_source == "Honeywell Baseline"
        assert cost.unit_cost == 6.55
        assert cost.per == 1
    
    def test_priority_3_placeholder_used(self, cost_config):
        """Test placeholder used for unknown license types."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"UNKNOWN_TYPE": 100}
        summary = calculator.calculate_license_cost(licensed, "M0616")
        
        assert len(summary.costs) == 1
        cost = summary.costs[0]
        assert cost.pricing_source == "Placeholder"
        assert cost.unit_cost == 100.00
        assert cost.per == 1
    
    def test_mpc_overrides_honeywell_when_both_present(self, cost_config):
        """Test MPC 2026 takes precedence over Honeywell for PROCESSPOINTS."""
        calculator = CostCalculator(cost_config)
        
        # PROCESSPOINTS exists in both catalogs
        licensed = {"PROCESSPOINTS": 4750}
        summary = calculator.calculate_license_cost(licensed, "M0617")
        
        cost = summary.costs[0]
        # Should use MPC 2026 pricing ($45.00), not Honeywell ($42.50)
        assert cost.pricing_source == "MPC 2026 Confirmed"
        assert cost.unit_cost == 45.00


class TestCostCalculationFormula:
    """Test cost calculation formula: (quantity / per) * unit_cost."""
    
    def test_basic_formula_per_50(self, cost_config):
        """Test formula with per=50: (4750 / 50) * 45 = 4275."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"PROCESSPOINTS": 4750}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        expected = (4750 / 50) * 45.00
        assert cost.total_cost == expected
        assert cost.total_cost == 4275.00
    
    def test_basic_formula_per_1(self, cost_config):
        """Test formula with per=1: (8 / 1) * 6.55 = 52.40."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"DIRECTSTATIONS": 8}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        expected = (8 / 1) * 6.55
        assert cost.total_cost == expected
        assert cost.total_cost == 52.40
    
    def test_formula_with_decimal_result(self, cost_config):
        """Test formula with non-integer division result."""
        calculator = CostCalculator(cost_config)
        
        # 4753 / 50 = 95.06, * 45 = 4277.70
        licensed = {"PROCESSPOINTS": 4753}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        expected = round((4753 / 50) * 45.00, 2)
        assert cost.total_cost == expected
    
    def test_multiple_license_types_summed(self, cost_config):
        """Test multiple license types summed correctly."""
        calculator = CostCalculator(cost_config)
        
        licensed = {
            "PROCESSPOINTS": 4750,  # (4750/50)*45 = 4275
            "DIRECTSTATIONS": 8     # (8/1)*6.55 = 52.40
        }
        summary = calculator.calculate_license_cost(licensed)
        
        assert len(summary.costs) == 2
        assert summary.total_cost == 4275.00 + 52.40
        assert summary.total_cost == 4327.40


class TestRoundingAndMinimums:
    """Test rounding to cents and minimum charge enforcement."""
    
    def test_rounding_to_cents(self, cost_config):
        """Test cost rounded to 2 decimal places."""
        calculator = CostCalculator(cost_config)
        
        # Force decimal result: (17 / 50) * 45 = 15.3 → 15.30
        licensed = {"PROCESSPOINTS": 17}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        assert cost.total_cost == 15.30
    
    def test_minimum_charge_applied(self, cost_config):
        """Test minimum charge of $0.01 applied to very small costs."""
        calculator = CostCalculator(cost_config)
        
        # Very small quantity: (1 / 50) * 45 = 0.90
        licensed = {"PROCESSPOINTS": 1}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        # Should be 0.90 (above minimum)
        assert cost.total_cost == 0.90
        assert cost.total_cost >= 0.01
    
    def test_zero_quantity_excluded(self, cost_config):
        """Test zero quantities excluded from calculation."""
        calculator = CostCalculator(cost_config)
        
        licensed = {
            "PROCESSPOINTS": 4750,
            "DIRECTSTATIONS": 0  # Should be excluded
        }
        summary = calculator.calculate_license_cost(licensed)
        
        # Only PROCESSPOINTS should be in costs
        assert len(summary.costs) == 1
        assert summary.costs[0].license_type == "PROCESSPOINTS"


class TestPricingSourceTracking:
    """Test pricing source tracking for audit trail."""
    
    def test_pricing_source_in_result(self, cost_config):
        """Test pricing source included in CostResult."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"PROCESSPOINTS": 4750}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        assert cost.pricing_source == "MPC 2026 Confirmed"
    
    def test_get_pricing_source_method(self, cost_config):
        """Test get_pricing_source() method returns correct catalog."""
        calculator = CostCalculator(cost_config)
        
        # MPC 2026
        source = calculator.get_pricing_source("PROCESSPOINTS")
        assert source == "MPC 2026 Confirmed"
        
        # Honeywell
        source = calculator.get_pricing_source("DIRECTSTATIONS")
        assert source == "Honeywell Baseline"
        
        # Placeholder
        source = calculator.get_pricing_source("UNKNOWN_TYPE")
        assert source == "Placeholder"
    
    def test_calculation_details_included(self, cost_config):
        """Test calculation details string included in result."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"PROCESSPOINTS": 4750}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        assert cost.calculation_details
        assert "4750" in cost.calculation_details
        assert "45.00" in cost.calculation_details


class TestMissingPricesTracking:
    """Test tracking of license types with missing pricing."""
    
    def test_missing_prices_empty_when_all_found(self, cost_config):
        """Test missing_prices empty when all types have pricing."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"PROCESSPOINTS": 4750, "DIRECTSTATIONS": 8}
        summary = calculator.calculate_license_cost(licensed)
        
        assert len(summary.missing_prices) == 0
    
    def test_unknown_type_uses_placeholder_not_missing(self, cost_config):
        """Test unknown types use placeholder, not marked as missing."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"UNKNOWN_TYPE": 100}
        summary = calculator.calculate_license_cost(licensed)
        
        # Placeholder used, so not missing
        assert len(summary.missing_prices) == 0
        assert len(summary.costs) == 1


class TestUtilityMethods:
    """Test utility methods for reporting and introspection."""
    
    def test_get_all_available_license_types(self, cost_config):
        """Test get_all_available_license_types() returns all types."""
        calculator = CostCalculator(cost_config)
        
        types = calculator.get_all_available_license_types()
        
        # Should include types from both catalogs
        assert "PROCESSPOINTS" in types
        assert "SCADAPOINTS" in types
        assert "DIRECTSTATIONS" in types
        assert len(types) >= 3
    
    def test_generate_pricing_report(self, cost_config):
        """Test generate_pricing_report() creates readable output."""
        calculator = CostCalculator(cost_config)
        
        licensed = {
            "PROCESSPOINTS": 4750,
            "DIRECTSTATIONS": 8
        }
        summary = calculator.calculate_license_cost(
            licensed,
            msid="M0614",
            cluster="Carson",
            system_number="60806"
        )
        
        report = calculator.generate_pricing_report(summary)
        
        # Check report contains key information
        assert "M0614" in report
        assert "Carson" in report
        assert "PROCESSPOINTS" in report
        assert "DIRECTSTATIONS" in report
        assert "$4,327.40" in report
    
    def test_report_includes_missing_prices(self, cost_config, tmp_path):
        """Test report includes missing prices section when applicable."""
        # Create config without placeholder
        cost_rules = cost_config.cost_rules.copy()
        cost_rules['pricing_strategy'] = [
            s for s in cost_rules['pricing_strategy']
            if s['name'] != 'Placeholder'
        ]
        cost_config.cost_rules = cost_rules
        
        calculator = CostCalculator(cost_config)
        
        licensed = {
            "PROCESSPOINTS": 4750,
            "UNKNOWN_TYPE": 100  # No pricing, no placeholder
        }
        summary = calculator.calculate_license_cost(licensed, "M0614")
        
        report = calculator.generate_pricing_report(summary)
        
        # Should have missing prices section
        assert "Missing Pricing" in report
        assert "UNKNOWN_TYPE" in report


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_licensed_dict(self, cost_config):
        """Test empty licensed dict returns empty summary."""
        calculator = CostCalculator(cost_config)
        
        licensed = {}
        summary = calculator.calculate_license_cost(licensed, "M0614")
        
        assert len(summary.costs) == 0
        assert summary.total_cost == 0.0
        assert len(summary.missing_prices) == 0
    
    def test_very_large_quantity(self, cost_config):
        """Test very large quantity doesn't cause issues."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"PROCESSPOINTS": 1_000_000}
        summary = calculator.calculate_license_cost(licensed)
        
        cost = summary.costs[0]
        expected = (1_000_000 / 50) * 45.00
        assert cost.total_cost == expected
    
    def test_system_identifiers_stored(self, cost_config):
        """Test system identifiers stored in summary."""
        calculator = CostCalculator(cost_config)
        
        licensed = {"PROCESSPOINTS": 4750}
        summary = calculator.calculate_license_cost(
            licensed,
            msid="M0614",
            cluster="Carson",
            system_number="60806"
        )
        
        assert summary.msid == "M0614"
        assert summary.cluster == "Carson"
        assert summary.system_number == "60806"
