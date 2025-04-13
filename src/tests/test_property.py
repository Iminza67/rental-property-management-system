import pytest
from src.model.property import Property, Land, House, Apartment, Shop, UtilityProvider, TaxRecord

class LeaseAgreement:
    def __init__(self):
        self.end_date = None

@pytest.fixture
def base_property():
    return Property("P001", "12 Green Street", 120.0, 1000.0, "DreamHomes Inc.")

def test_property_initialization(base_property):
    assert base_property.property_id == "P001"
    assert base_property.address == "12 Green Street"
    assert base_property.size == 120.0
    assert base_property.price == 1000.0
    assert base_property.get_status() == "Available"
    assert base_property.calculate_cost() == 1000.0

def test_add_lease_sets_occupied_status(base_property):
    lease = LeaseAgreement()
    base_property.add_lease(lease)
    assert base_property.is_occupied is True
    assert base_property.current_lease == lease
    assert lease not in base_property.history

def test_terminate_lease_moves_to_history(base_property):
    lease = LeaseAgreement()
    base_property.add_lease(lease)
    base_property.terminate_lease()
    assert base_property.current_lease is None
    assert lease in base_property.history
    assert base_property.is_occupied is False

def test_land_initialization():
    land = Land("L001", "Plot 7B", 1000.0, 25000.0, "AgroGroup", "Residential", 800.0)
    assert land.zoning_type == "Residential"
    assert land.buildable_area == 800.0

def test_house_attributes():
    house = House("H001", "45 Oak Drive", 200.0, 1500.0, "VillaWorld", 3, 2)
    assert house.num_bedrooms == 3
    assert house.num_bathrooms == 2
    assert house.has_garden is False
    assert repr(house) == "House(bedrooms=3, bathrooms=2)"

def test_apartment_attributes():
    apartment = Apartment("A001", "Block C, Apt 4", 85.0, 900.0, "UrbanStay", 4)
    assert apartment.floor_number == 4
    assert apartment.has_elevator is False
    assert apartment.has_balcony is False
    assert repr(apartment) == "Apartment(name=A001, value=900.0, floor=4)"

def test_shop_attributes():
    shop = Shop("S001", "Main Street 10", 60.0, 1200.0, "BizHub", "Retail")
    assert shop.business_type == "Retail"
    assert shop.parking_available is False

def test_utility_provider_cost():
    utility = UtilityProvider(1, "PowerCo", "Electricity", 50.0)
    assert utility.calculate_utility_cost(3) == 150.0

def test_tax_record_calculation(base_property):
    tax = TaxRecord(101, base_property, 2025, 400.0)
    assert tax.calculate_tax() == 400.0
