"""
Test suite for data models.

Tests follow TDD approach:
1. Test creation first (validates interface)
2. Test validation rules
3. Test business logic methods
4. Test serialization/deserialization

Coverage target: 100% (critical data layer)
"""

import pytest
from datetime import datetime
from v2.models.license import LicenseData, LicenseType, ValidationError
from v2.models.usage import UsageData
from v2.models.cost import CostCalculation
from v2.models.transfer import TransferCandidate


# ============================================================================
# LicenseData Tests
# ============================================================================

class TestLicenseDataCreation:
    """Test valid license creation scenarios"""
    
    def test_minimal_license_creation(self):
        """Test creating license with minimum required fields"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520'
        )
        
        assert license.msid == 'M0614'
        assert license.system_number == '60806'
        assert license.cluster == 'Carson'
        assert license.release == 'R520'
        assert license.product == 'PKS'  # Default value
        assert license.file_version == 0  # Default value
        assert license.licensed == {}  # Empty dict
    
    def test_full_license_creation(self):
        """Test creating license with all fields populated"""
        license_date = datetime(2024, 1, 15)
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            product='PKS',
            license_date=license_date,
            customer='Marathon Petroleum Company',
            file_version=40,
            file_path='data/raw/Carson/M0614_60806_v40.xml',
            licensed={
                'PROCESSPOINTS': 4750,
                'SCADAPOINTS': 5750,
                'DIRECTSTATIONS': 8
            }
        )
        
        assert license.msid == 'M0614'
        assert license.license_date == license_date
        assert license.customer == 'Marathon Petroleum Company'
        assert license.file_version == 40
        assert len(license.licensed) == 3


class TestLicenseDataValidation:
    """Test validation rules catch invalid data"""
    
    def test_rejects_empty_msid(self):
        """Empty MSID should raise ValidationError"""
        with pytest.raises(ValidationError, match="Invalid MSID"):
            LicenseData(
                msid='',
                system_number='60806',
                cluster='Carson',
                release='R520'
            )
    
    def test_rejects_unknown_msid(self):
        """'Unknown' MSID should raise ValidationError"""
        with pytest.raises(ValidationError, match="Invalid MSID"):
            LicenseData(
                msid='Unknown',
                system_number='60806',
                cluster='Carson',
                release='R520'
            )
    
    def test_rejects_non_numeric_system_number(self):
        """System number must be numeric"""
        with pytest.raises(ValidationError, match="must be numeric"):
            LicenseData(
                msid='M0614',
                system_number='ABC123',
                cluster='Carson',
                release='R520'
            )
    
    def test_rejects_empty_cluster(self):
        """Cluster is required"""
        with pytest.raises(ValidationError, match="Cluster required"):
            LicenseData(
                msid='M0614',
                system_number='60806',
                cluster='',
                release='R520'
            )
    
    def test_rejects_negative_version(self):
        """File version cannot be negative"""
        with pytest.raises(ValidationError, match="cannot be negative"):
            LicenseData(
                msid='M0614',
                system_number='60806',
                cluster='Carson',
                release='R520',
                file_version=-1
            )


class TestLicenseDataProperties:
    """Test computed properties and methods"""
    
    def test_unique_key(self):
        """Unique key combines cluster, MSID, system number"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520'
        )
        
        assert license.unique_key == ('Carson', 'M0614', '60806')
    
    def test_display_name(self):
        """Display name formats for human readability"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520'
        )
        
        assert license.display_name == 'M0614/60806 (Carson)'
    
    def test_get_licensed_quantity_existing(self):
        """Get quantity for existing license type"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        assert license.get_licensed_quantity('PROCESSPOINTS') == 4750
    
    def test_get_licensed_quantity_missing(self):
        """Get quantity returns 0 for missing types"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={}
        )
        
        assert license.get_licensed_quantity('PROCESSPOINTS') == 0
    
    def test_has_license_type_true(self):
        """Check if system has license type (present and >0)"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        assert license.has_license_type('PROCESSPOINTS') == True
    
    def test_has_license_type_false_missing(self):
        """Check returns False for missing types"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={}
        )
        
        assert license.has_license_type('PROCESSPOINTS') == False
    
    def test_has_license_type_false_zero(self):
        """Check returns False for zero quantities"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 0}
        )
        
        assert license.has_license_type('PROCESSPOINTS') == False


class TestLicenseDataSerialization:
    """Test to_dict and from_dict methods"""
    
    def test_to_dict(self):
        """Serialize license to dictionary"""
        license_date = datetime(2024, 1, 15)
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            license_date=license_date,
            licensed={'PROCESSPOINTS': 4750}
        )
        
        data = license.to_dict()
        
        assert data['msid'] == 'M0614'
        assert data['system_number'] == '60806'
        assert data['cluster'] == 'Carson'
        assert data['license_date'] == '2024-01-15T00:00:00'
        assert data['licensed'] == {'PROCESSPOINTS': 4750}
    
    def test_to_dict_none_date(self):
        """Serialize handles None date"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            license_date=None
        )
        
        data = license.to_dict()
        assert data['license_date'] is None
    
    def test_from_dict(self):
        """Deserialize license from dictionary"""
        data = {
            'msid': 'M0614',
            'system_number': '60806',
            'cluster': 'Carson',
            'release': 'R520',
            'product': 'PKS',
            'license_date': '2024-01-15T00:00:00',
            'customer': 'Marathon',
            'file_version': 40,
            'file_path': 'test.xml',
            'licensed': {'PROCESSPOINTS': 4750}
        }
        
        license = LicenseData.from_dict(data)
        
        assert license.msid == 'M0614'
        assert license.license_date == datetime(2024, 1, 15)
        assert license.licensed == {'PROCESSPOINTS': 4750}
    
    def test_round_trip_serialization(self):
        """Serialize and deserialize preserves data"""
        original = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            license_date=datetime(2024, 1, 15),
            licensed={'PROCESSPOINTS': 4750}
        )
        
        data = original.to_dict()
        restored = LicenseData.from_dict(data)
        
        assert restored.unique_key == original.unique_key
        assert restored.licensed == original.licensed
        assert restored.license_date == original.license_date


class TestLicenseDataImmutability:
    """Test that LicenseData is immutable (frozen=True)"""
    
    def test_cannot_modify_msid(self):
        """Cannot modify MSID after creation"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520'
        )
        
        with pytest.raises(AttributeError):
            license.msid = 'M0615'
    
    def test_cannot_modify_licensed_dict(self):
        """Cannot modify licensed quantities after creation"""
        license = LicenseData(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            release='R520',
            licensed={'PROCESSPOINTS': 4750}
        )
        
        # Cannot reassign licensed dict
        with pytest.raises(AttributeError):
            license.licensed = {}


# ============================================================================
# UsageData Tests
# ============================================================================

class TestUsageDataCreation:
    """Test usage data creation"""
    
    def test_minimal_usage_creation(self):
        """Create usage with minimum fields"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        
        assert usage.msid == 'M0614'
        assert usage.license_type == 'PROCESSPOINTS'
        assert usage.used_quantity == 108
    
    def test_full_usage_creation(self):
        """Create usage with all fields"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=108,
            cluster='Carson',
            file_path='data/raw/Usage/BC-LAR-008.csv'
        )
        
        assert usage.cluster == 'Carson'
        assert usage.file_path == 'data/raw/Usage/BC-LAR-008.csv'


class TestUsageDataValidation:
    """Test usage validation"""
    
    def test_rejects_empty_msid(self):
        """MSID required"""
        with pytest.raises(ValidationError, match="MSID required"):
            UsageData(
                msid='',
                license_type='PROCESSPOINTS',
                used_quantity=108
            )
    
    def test_rejects_empty_license_type(self):
        """License type required"""
        with pytest.raises(ValidationError, match="License type required"):
            UsageData(
                msid='M0614',
                license_type='',
                used_quantity=108
            )
    
    def test_rejects_negative_quantity(self):
        """Quantity must be non-negative"""
        with pytest.raises(ValidationError, match="cannot be negative"):
            UsageData(
                msid='M0614',
                license_type='PROCESSPOINTS',
                used_quantity=-10
            )


# ============================================================================
# CostCalculation Tests
# ============================================================================

class TestCostCalculationCreation:
    """Test cost calculation creation"""
    
    def test_cost_creation(self):
        """Create cost calculation"""
        cost = CostCalculation(
            msid='M0614',
            system_number='60806',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            unit_price=45.00,
            total_cost=213750.00,
            price_source='MPC 2026 Confirmed'
        )
        
        assert cost.msid == 'M0614'
        assert cost.total_cost == 213750.00
        assert cost.price_source == 'MPC 2026 Confirmed'


class TestCostCalculationMethods:
    """Test cost calculation business logic"""
    
    def test_calculate_total(self):
        """Calculate total cost from quantity and price"""
        cost = CostCalculation(
            msid='M0614',
            system_number='60806',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            unit_price=45.00,
            total_cost=0,  # Will be calculated
            price_source='MPC 2026 Confirmed'
        )
        
        expected = 4750 * 45.00
        assert cost.calculate_total() == expected
    
    def test_is_confirmed_price(self):
        """Test detection of confirmed MPC prices"""
        cost = CostCalculation(
            msid='M0614',
            system_number='60806',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            unit_price=45.00,
            total_cost=213750.00,
            price_source='MPC 2026 Confirmed'
        )
        assert cost.is_confirmed_price == True
    
    def test_is_placeholder(self):
        """Test detection of placeholder prices"""
        cost = CostCalculation(
            msid='M0614',
            system_number='60806',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            unit_price=100.00,
            total_cost=475000.00,
            price_source='Placeholder $100'
        )
        assert cost.is_placeholder == True
    
    def test_to_dict(self):
        """Test serialization"""
        cost = CostCalculation(
            msid='M0614',
            system_number='60806',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            unit_price=45.00,
            total_cost=213750.00,
            price_source='MPC 2026 Confirmed'
        )
        data = cost.to_dict()
        assert data['msid'] == 'M0614'
        assert data['total_cost'] == 213750.00
    
    def test_from_dict(self):
        """Test deserialization"""
        data = {
            'msid': 'M0614',
            'system_number': '60806',
            'license_type': 'PROCESSPOINTS',
            'licensed_quantity': 4750,
            'unit_price': 45.00,
            'total_cost': 213750.00,
            'price_source': 'MPC 2026 Confirmed'
        }
        cost = CostCalculation.from_dict(data)
        assert cost.msid == 'M0614'
        assert cost.total_cost == 213750.00


# ============================================================================
# TransferCandidate Tests
# ============================================================================

class TestTransferCandidateCreation:
    """Test transfer candidate creation"""
    
    def test_transfer_creation(self):
        """Create transfer candidate"""
        transfer = TransferCandidate(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            used_quantity=108,
            excess_quantity=4642,
            excess_value=208890.00,
            unit_price=45.00,
            priority='HIGH'
        )
        
        assert transfer.excess_quantity == 4642
        assert transfer.excess_value == 208890.00
        assert transfer.priority == 'HIGH'
    
    def test_utilization_percentage(self):
        """Calculate utilization percentage"""
        transfer = TransferCandidate(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            used_quantity=108,
            excess_quantity=4642,
            excess_value=208890.00,
            unit_price=45.00,
            priority='HIGH'
        )
        
        # 108 / 4750 = 2.27%
        assert abs(transfer.utilization_percentage() - 2.27) < 0.01
    
    def test_utilization_percentage_zero_licensed(self):
        """Handle zero licensed quantity"""
        transfer = TransferCandidate(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            licensed_quantity=0,
            used_quantity=0,
            excess_quantity=0,
            excess_value=0.00,
            unit_price=45.00,
            priority='LOW'
        )
        assert transfer.utilization_percentage() == 0.0
    
    def test_excess_percentage(self):
        """Calculate excess percentage"""
        transfer = TransferCandidate(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            used_quantity=108,
            excess_quantity=4642,
            excess_value=208890.00,
            unit_price=45.00,
            priority='HIGH'
        )
        # 100 - 2.27 = 97.73%
        assert abs(transfer.excess_percentage - 97.73) < 0.01
    
    def test_is_high_value(self):
        """Test high value detection"""
        transfer = TransferCandidate(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            used_quantity=108,
            excess_quantity=4642,
            excess_value=208890.00,
            unit_price=45.00,
            priority='HIGH'
        )
        assert transfer.is_high_value == True
    
    def test_to_dict(self):
        """Test serialization with computed fields"""
        transfer = TransferCandidate(
            msid='M0614',
            system_number='60806',
            cluster='Carson',
            license_type='PROCESSPOINTS',
            licensed_quantity=4750,
            used_quantity=108,
            excess_quantity=4642,
            excess_value=208890.00,
            unit_price=45.00,
            priority='HIGH'
        )
        data = transfer.to_dict()
        assert data['msid'] == 'M0614'
        assert 'utilization_percentage' in data
        assert 'excess_percentage' in data
    
    def test_from_dict(self):
        """Test deserialization filters computed fields"""
        data = {
            'msid': 'M0614',
            'system_number': '60806',
            'cluster': 'Carson',
            'license_type': 'PROCESSPOINTS',
            'licensed_quantity': 4750,
            'used_quantity': 108,
            'excess_quantity': 4642,
            'excess_value': 208890.00,
            'unit_price': 45.00,
            'priority': 'HIGH',
            'utilization_percentage': 2.27,  # Should be filtered
            'excess_percentage': 97.73       # Should be filtered
        }
        transfer = TransferCandidate.from_dict(data)
        assert transfer.msid == 'M0614'
        assert transfer.excess_value == 208890.00


class TestUsageDataSerialization:
    """Test usage serialization"""
    
    def test_usage_to_dict(self):
        """Test usage serialization"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=108,
            cluster='Carson',
            file_path='test.csv'
        )
        data = usage.to_dict()
        assert data['msid'] == 'M0614'
        assert data['used_quantity'] == 108
    
    def test_usage_from_dict(self):
        """Test usage deserialization"""
        data = {
            'msid': 'M0614',
            'license_type': 'PROCESSPOINTS',
            'used_quantity': 108,
            'cluster': 'Carson',
            'file_path': 'test.csv'
        }
        usage = UsageData.from_dict(data)
        assert usage.msid == 'M0614'
    
    def test_usage_match_key(self):
        """Test usage match key"""
        usage = UsageData(
            msid='M0614',
            license_type='PROCESSPOINTS',
            used_quantity=108
        )
        assert usage.match_key == ('M0614', 'PROCESSPOINTS')
