from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.scripts.task2 import LeaseAgreement

class Property:
    def __init__(self, property_id: str, address: str, size: float, price: float, company_name: str):
        super().__init__(company_name)
        self.property_id = property_id
        self.address = address
        self.size = size
        self.facilities: list[str] = []
        self.price = price
        self.history: list['LeaseAgreement'] = []
        self.is_occupied: bool = False
        self.current_lease = None

    def __repr__(self):
        return f"Property(name={self.property_id}, value={self.price})"
    def get_status(self):
        return "Occupied" if self.is_occupied else "Available"
    def calculate_cost(self):
        return self.price 
    def add_lease(self, lease: 'LeaseAgreement') -> None:
        if self.current_lease:
            self.history.append(self.current_lease)
        self.current_lease = lease
        self.is_occupied = True

    def terminate_lease(self) -> None:
        if self.current_lease:
            self.current_lease.end_date = datetime.now()
            self.history.append(self.current_lease)
            self.current_lease = None
            self.is_occupied = False

class Land(Property):
    def __init__(self, property_id: str, address: str, size: float, price: float, company_name: str, zoning_type: str, buildable_area: float):
        super().__init__(property_id, address, size, price, company_name)
        self.zoning_type = zoning_type
        self.buildable_area = buildable_area

class House(Property):
    def __init__(self, property_id: str, address: str, size: float, price: float, company_name: str,num_bedrooms: int, num_bathrooms:int):
        super().__init__(property_id, address, size, price, company_name)
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms
        self.has_garden: bool = False

    def __repr__(self):
        return f"House(bedrooms={self.num_bedrooms}, bathrooms={self.num_bathrooms})"
    
class Apartment(Property):
    def __init__(self, property_id: str, address: str, size: float, price: float,company_name: str,floor_number: int):
        super().__init__(property_id, address, size, price, company_name)
        self.floor_number = floor_number
        self.has_elevator: bool = False
        self.has_balcony: bool = False

    def __repr__(self):
        return f"Apartment(name={self.property_id}, value={self.price}, floor={self.floor_number})"
class Shop(Property):
    def __init__(self, property_id: str, address: str, size: float, price: float,company_name: str, business_type: str):
        super().__init__(property_id, address, size, price, company_name)
        self.business_type = business_type
        self.parking_available: bool = False

class UtilityProvider:
    def __init__(self, provider_id: int, name: str, service_type: str, monthly_cost: float):
        self.provider_id = provider_id
        self.name = name
        self.service_type = service_type
        self.monthly_cost = monthly_cost

    def calculate_utility_cost(self, months: int) -> float:
        return self.monthly_cost * months
class TaxRecord:
    def __init__(self, tax_id: int, property: Property, year: int, amount: float):
        self.tax_id = tax_id
        self.property = property
        self.year = year
        self.amount = amount

    def calculate_tax(self) -> float:
        return self.amount
    