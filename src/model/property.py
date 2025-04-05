from datetime import datetime
from src.model.payments import LeaseAgreement
from src.model.rentalcompany import RentalCompany

class Property(RentalCompany):
    def __init__(self, property_id: str, address: str,size: float, price: float):
        self.property_id = property_id
        self.address = address
        self.size = size
        self.facilities: list[str] = []
        self.price = price
        self.history: list[LeaseAgreement] = []
        self.is_occupied: bool = False

    def __repr__(self):
        return f"Property(name={self.name}, value={self.value})"
    def get_status(self):
        return "Occupied" if self.is_occupied else "Available"
    def calculate_cost(self):
        return self.price 
    def add_lease(self, lease: 'LeaseAgreement') -> None:
        if self.current_lease:
            self.lease_history.append(self.current_lease)
        self.current_lease = lease
        self.set_occupancy(True)
    
    def terminate_lease(self) -> None:
        if self.current_lease:
            self.current_lease.end_date = datetime.now()
            self.lease_history.append(self.current_lease)
            self.current_lease = None
            self.set_occupancy(False)
    
class Land(Property):
    def __init__(self, zoning_type: str, buildable_area: float):
        super().__init__(property_id="", size=0.0, address="", price=0.0, history=[], is_occupied=False)
        self.zoning_type = zoning_type
        self.buildable_area = buildable_area

class House(Property):
    def __init__(self, num_bedrooms: int, num_bathrooms: int):
        super().__init__(property_id="", size=0.0, address="", price=0.0, facilities=[], history=[], is_occupied=False)
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms
        self.has_garden: bool = False

    def __repr__(self):
        return f"House(name={self.name}, value={self.value}, bedrooms={self.bedrooms}, bathrooms={self.bathrooms})"
    
class Apartment(Property):
    def __init__(self, floor_number: int):
        super().__init__(property_id="", size=0.0, address="", price=0.0, facilities=[], history=[], is_occupied=False)
        self.floor_number = floor_number
        self.has_elevator: bool = False
        self.has_balcony: bool = False

    def __repr__(self):
        return f"Apartment(name={self.name}, value={self.value}, floor={self.floor})"
class Shop(Property):
    def __init__(self, business_type: str):
        super().__init__(property_id="", size=0.0, address="", price=0.0, facilities=[], history=[], is_occupied=False)
        self.business_type = business_type
        self.parking_available: bool = False

    def __repr__(self):
        return f"Shop(name={self.name}, value={self.value}, area={self.area})"