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
    def __init__(self, owner_id: int, name:str, contact_info:str, properties: list[Property]):
        super().__init__(name)
        self.owner_id = owner_id
        self.name = name
        self.contact_info = contact_info
        self.properties: list[Property] = properties
    def get_properties(self):
        return self.properties

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
    def __init__(self, property, resident, start_date, duration_months, monthly_rent):
        self.property = property
        self.resident = resident
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, '%Y-%m-%d')
        self.duration_months = duration_months
        self.end_date = self._calculate_end_date()
        self.monthly_rent = monthly_rent
        self.terms = []
        self.is_active = True
    
    def _calculate_end_date(self):
        year = self.start_date.year + (self.start_date.month + self.duration_months - 1) // 12
        month = (self.start_date.month + self.duration_months - 1) % 12 + 1
        day = min(self.start_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return datetime(year, month, day)
    
    def add_term(self, term):
        self.terms.append(term)
    
    def renew(self, additional_months):
        self.duration_months += additional_months
        self.end_date = self._calculate_end_date()
    
    def terminate(self):
        self.is_active = False
        self.end_date = datetime.now()
        self.property.terminate_lease()
        self.resident.current_lease = None
    
    def __str__(self):
        return f"Lease for {self.property} with {self.resident} ({self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')})"

class Contract(Owner,Property):
    def __init__(self, contract_id:int, owner:Owner, property: Property, start_date:datetime, end_date:datetime, commission_fee:float):
        self.contract_id = contract_id
        self.owner = owner
        self.property = property
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, '%Y-%m-%d')
        self.commission_fee = commission_fee
    def is_active(self):
        if self.start_date <= datetime.now() <= self.end_date:
            return True 
        return False
    def calculate_commission(self):
        if self.is_active():
            return self.property.price * (self.commission_fee / 100)
        return 0
    
    def terminate(self):
        self.is_active = False
    
    def __str__(self):
        return f"Rental Contract for {self.property} with {self.owner} ({self.management_fee}% fee, started {self.start_date.strftime('%Y-%m-%d')})"