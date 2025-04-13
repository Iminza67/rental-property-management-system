import pytest
from datetime import timedelta

from src.model import *

@pytest.fixture
def sample_property():
    return Property("P001", "Downtown", 100.0, 1200.0, "Nice Owner")

@pytest.fixture
def sample_resident():
    return Resident(user_id=101, username="jane", password_hash="secret", resident_id=1, name="Jane", contact_info="jane@email.com", lease_agreements=[])

def test_user_authentication():
    user = User(1, "user", "pass123", "renter")
    assert user.authenticate("pass123")
    assert not user.authenticate("wrong")

def test_owner_get_properties(sample_property):
    owner = Owner(1, "owner", "contact", [sample_property])
    assert sample_property in owner.get_properties()

def test_admin_property_management(sample_property):
    admin = Admin(2, "admin", "hash")
    admin.add_property(sample_property)
    assert sample_property in admin.properties
    admin.remove_property(sample_property)
    assert sample_property not in admin.properties

def test_property_manager_assignment(sample_property):
    manager = PropertyManager(3, "manager", "hash")
    manager.assign_property(sample_property)
    assert sample_property in manager.properties

def test_renter_view_lease_details(sample_property, sample_resident):
    lease = LeaseAgreement(1, sample_property, sample_resident, datetime.now(), 12, 1000.0)
    renter = Renter(4, "renter", "hash")
    assert "Lease Details:" in renter.view_lease_details(lease)

def test_resident_get_active_lease(sample_property, sample_resident):
    lease = LeaseAgreement(2, sample_property, sample_resident, datetime.now(), 12, 1000.0)
    sample_resident.lease_agreements.append(lease)
    assert lease in sample_resident.get_active_lease()

def test_resident_pay_rent(sample_property, sample_resident):
    lease = LeaseAgreement(3, sample_property, sample_resident, datetime.now(), 12, 1000.0)
    sample_resident.current_lease = lease
    sample_resident.pay_rent(500.0)  # No assert; just making sure no exception is raised

def test_rental_application_approval(sample_property, sample_resident):
    app = RentalApplication(1, sample_property, sample_resident, "Pending")
    app.approve()
    assert app.status == "Approved"
    assert sample_resident.current_lease is not None

def test_rental_application_rejection(sample_property, sample_resident):
    app = RentalApplication(2, sample_property, sample_resident, "Pending")
    app.reject()
    assert app.status == "Rejected"

def test_complaint_resolve(sample_property, sample_resident):
    complaint = Complaint(1, sample_property, sample_resident, "Leaky pipe")
    event = complaint.resolve()
    assert complaint.status is True
    assert isinstance(event, Event)
    assert "resolved successfully" in event.text

def test_lease_renewal(sample_property, sample_resident):
    lease = LeaseAgreement(4, sample_property, sample_resident, datetime.now(), 6, 800.0)
    old_end_date = lease.end_date
    lease.renew(6)
    assert lease.duration_months == 12
    assert lease.end_date > old_end_date

def test_lease_termination(sample_property, sample_resident):
    lease = LeaseAgreement(5, sample_property, sample_resident, datetime.now(), 12, 1000.0)
    sample_resident.current_lease = lease
    lease.terminate()
    assert not lease._is_active
    assert sample_resident.current_lease is None

def test_rental_contract_commission(sample_property):
    owner = Owner(6, "Owner", "info", [sample_property])
    start = datetime.now() - timedelta(days=1)
    end = datetime.now() + timedelta(days=30)
    contract = RentalContract(1, owner, sample_property, "2024-03-23", '2025-04-15', 10.0)
    commission = contract.calculate_commission()
    assert commission == sample_property.price * 0.1
