from datetime import datetime
class Property:
    def __init__(self, property_id: str, address: str,size: float, price: float):
        self.property_id = property_id
        self.address = address
        self.size = size
        self.facilities: list[str] = []
        self.price = price
        self.history: list[Lease] = []
        self.is_occupied: bool = False

    def __repr__(self):
        return f"Property(name={self.name}, value={self.value})"
    def get_status(self):
        return "Occupied" if self.is_occupied else "Available"
    def calculate_cost(self):
        return self.price 
    def add_lease(self, lease: 'Lease') -> None:
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
class User:
    def __init__(self, user_id: int, username: str, password_hash: str, role: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def __repr__(self):
        return f"User(name={self.name}, age={self.age})"
    
    def authenticate(self, password: str) -> bool:
        return self.password_hash == hash(password)
class Owner(User):
    def __init__(self, name: str, age: int, properties: list[Property]):
        super().__init__(name, age)
        self.properties = properties

    def __repr__(self):
        return f"Owner(name={self.name}, age={self.age}, properties={self.properties})"
class Admin(User):
    def __init__(self):
        super().__init__(user_id= "", username="")
        self.permissions = ["manage_properties", "manage_users"]
    
    def add_property(self, property: Property):
        self.properties.append(property)
    def remove_property(self, property: Property):
        if property in self.properties:
            self.properties.remove(property)
        else:
            print(f"Property {property} not found.")

    def __repr__(self):
        return f"Admin(name={self.name}, age={self.age})"
class PropertyManager(User):
    def __init__(self):
        super().__init__(user_id= "", username="")
    def assign_property(self, property: Property):
        self.properties.append(property)

class Renter(User):
    def __init__(self):
        super().__init__(user_id= "", username="")
    
    def view_lease_details(self, lease: 'Lease'):
        return f"Lease Details: {lease}"
    def __repr__(self):
        return f"Resident(name={self.name}, age={self.age}, apartment={self.apartment})"

class Lease:
    def __init__(self, owner: Owner, resident: Renter, property: Property, start_date: str, end_date: str):
        self.owner = owner
        self.resident = resident
        self.property = property
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"Lease(owner={self.owner}, resident={self.resident}, property={self.property}, start_date={self.start_date}, end_date={self.end_date})"

class RentalContract:
    def __init__(self, lease: Lease, monthly_rent: float):
        self.lease = lease
        self.monthly_rent = monthly_rent

    def __repr__(self):
        return f"RentalContract(lease={self.lease}, monthly_rent={self.monthly_rent})"