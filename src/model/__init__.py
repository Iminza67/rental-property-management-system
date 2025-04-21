from datetime import datetime
from src.model.property import Property
from src.model.maintenance import Event

class User:
    def __init__(self, user_id: int, username: str, password_hash: str, role: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def __repr__(self):
        return f"User(name={self.username}, user_id={self.user_id}, role={self.role})"

    def authenticate(self, password: str) -> bool:
        return self.password_hash == password


class Owner(User):
    def __init__(self, owner_id: int, name: str, contact_info: str, properties: list[Property]):
        super().__init__(user_id=owner_id, username=name, password_hash="dummy", role="owner")
        self.contact_info = contact_info
        self.properties = properties

    def get_properties(self):
        return self.properties


class Admin(User):
    def __init__(self, user_id: int, username: str, password_hash: str):
        super().__init__(user_id, username, password_hash, role="admin")
        self.permissions = ["manage_properties", "manage_users"]
        self.properties = []

    def add_property(self, property: Property):
        self.properties.append(property)

    def remove_property(self, property: Property):
        if property in self.properties:
            self.properties.remove(property)
        else:
            print(f"Property {property} not found.")


class PropertyManager(User):
    def __init__(self, user_id: int, username: str, password_hash: str):
        super().__init__(user_id, username, password_hash, role="manager")
        self.properties: list[Property] = []

    def assign_property(self, property: Property):
        self.properties.append(property)


class Renter(User):
    def __init__(self, user_id: int, username: str, password_hash: str):
        super().__init__(user_id, username, password_hash, role="renter")

    def view_lease_details(self, lease: 'LeaseAgreement'):
        return f"Lease Details: {lease}"


class Resident(User):
    def __init__(self, user_id: int, username: str, password_hash: str, resident_id: int, name: str, contact_info: str, lease_agreements: list['LeaseAgreement']):
        super().__init__(user_id, username, password_hash, role="resident")
        self.resident_id = resident_id
        self.name = name
        self.contact_info = contact_info
        self.lease_agreements = lease_agreements
        self.current_lease: 'LeaseAgreement' = None

    def get_active_lease(self):
        return [lease for lease in self.lease_agreements if lease.is_active()]

    def pay_rent(self, amount: float):
        if self.current_lease:
            self.current_lease.pay_rent(amount)
        else:
            print("No active lease found.")


class RentalApplication:
    def __init__(self, application_id: int, property: Property, applicant: Resident, status: str):
        self.application_id = application_id
        self.property = property
        self.applicant = applicant
        self.status = status

    def approve(self):
        self.status = "Approved"
        lease = LeaseAgreement(1, self.property, self.applicant, datetime.now(), 12, 1000)
        self.property.add_lease(lease)
        self.applicant.lease_agreements.append(lease)
        self.applicant.current_lease = lease

    def reject(self):
        self.status = "Rejected"


class Complaint:
    def __init__(self, complaint_id: int, property: Property, resident: Resident, description: str, status: bool = False):
        self.complaint_id = complaint_id
        self.property = property
        self.resident = resident
        self.description = description
        self.status = status

    def resolve(self):
        if not self.status:
            self.status = True
            return Event(opened=False, text="Complaint resolved successfully.")


class LeaseAgreement:
    def __init__(self, lease_id: int, property: Property, resident: Resident, start_date, duration_months: int, monthly_rent: float):
        self.lease_id = lease_id
        self.property = property
        self.resident = resident
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, '%Y-%m-%d')
        self.duration_months = duration_months
        self.monthly_rent = monthly_rent
        self._is_active = True
        self.end_date = self._calculate_end_date()

    def is_active(self) -> bool:
        return self._is_active and datetime.now() < self.end_date

    def _calculate_end_date(self):
        year = self.start_date.year + (self.start_date.month + self.duration_months - 1) // 12
        month = (self.start_date.month + self.duration_months - 1) % 12 + 1
        day = min(self.start_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return datetime(year, month, day)

    def renew(self, additional_months):
        self.duration_months += additional_months
        self.end_date = self._calculate_end_date()

    def terminate(self):
        self._is_active = False
        self.end_date = datetime.now()
        self.property.terminate_lease()
        self.resident.current_lease = None

    def pay_rent(self, amount: float):
        print(f"Payment of {amount} received for lease {self.lease_id}.")

    def __str__(self):
        return f"Lease for {self.property} with {self.resident.name} ({self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')})"


class RentalContract:
    def __init__(self, contract_id: int, owner: Owner, property: Property, start_date: str, end_date: str, commission_fee: float):
        self.contract_id = contract_id
        self.owner = owner
        self.property = property
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, '%Y-%m-%d')
        self.commission_fee = commission_fee
        self._is_active = self.is_active()

    def is_active(self):
        return self.start_date <= datetime.now() <= self.end_date

    def calculate_commission(self):
        commission_percentage= self.commission_fee / 100
        return self.property.price * commission_percentage


    def terminate(self):
        self._is_active = False

    def __str__(self):
        return f"Rental Contract for {self.property} with {self.owner.name} ({self.commission_fee}% fee, started {self.start_date.strftime('%Y-%m-%d')})"
