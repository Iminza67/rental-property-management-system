import pytest
from datetime import datetime, date
from src.model.maintenance import Event, EventLog, MaintenanceRequest, Renovation
from src.model.property import Property
from src.model import (
    Owner, PropertyManager, Renter, Resident, LeaseAgreement,
    RentalContract, Complaint
)

# ----------- Maintenance & EventLog Tests -----------

def test_event_log():
    log = EventLog(events=[])
    event = Event(opened=True, text="Test event")
    log.record_event(event)
    
    assert "Test event" in log.read_new_messages()
    assert "Test event" in log.read_all_messages()

def test_maintenance_request():
    prop = Property(1, "Test Prop", "Test Location", 1000)
    request = MaintenanceRequest(1, prop, date.today(), "Pending")
    
    event = request.approve_request("Pending")
    assert request.status == "Approved"
    assert "approved" in event.text.lower()

    resolved_event = request.resolve_request()
    assert request.status == "Resolved"
    assert "resolved" in resolved_event.text.lower()

def test_renovation_cost():
    prop = Property(2, "Another Property", "Another Location", 1200)
    renovation = Renovation(1, prop, date.today(), 5000.0, "Paint and plumbing")
    
    assert renovation.get_total_cost() == 5000.0

# ----------- User, Lease, and Contract Tests -----------

def test_owner_get_properties():
    prop1 = Property(1, "A", "Loc", 1000)
    prop2 = Property(2, "B", "Loc", 1500)
    owner = Owner(10, "John Doe", "john@example.com", [prop1, prop2])
    
    assert prop1 in owner.get_properties()
    assert prop2 in owner.get_properties()

def test_renter_view_lease_details():
    renter = Renter(5, "RenterUser", "hash", "renter")
    lease = LeaseAgreement(1, Property(1, "A", "Loc", 1000), renter, "2025-01-01", 12, 1200)
    details = renter.view_lease_details(lease)
    
    assert "Lease Details" in details

def test_lease_agreement_active_status():
    resident = Resident(1, "Resident1", "hash", "resident", 101, "Name", "contact", [])
    lease = LeaseAgreement(1, Property(3, "X", "Y", 999), resident, datetime.now(), 12, 1000)
    
    assert lease.is_active()

def test_rental_contract_commission():
    prop = Property(10, "Nice Place", "City", 2000)
    owner = Owner(99, "Owner1", "owner@example.com", [prop])
    contract = RentalContract(1, owner, prop, "2025-01-01", "2025-12-31", 10.0)
    
    assert contract.calculate_commission() == 200.0  # 10% of 2000

def test_complaint_resolve():
    prop = Property(11, "Prop", "Nowhere", 1200)
    resident = Resident(2, "ResUser", "hash", "resident", 10, "Name", "Contact", [])
    complaint = Complaint(1, prop, resident, "Leaking pipe", False)

    event = complaint.resolve()
    assert complaint.status is True
    assert isinstance(event, Event)
    assert "resolved" in event.text.lower()
