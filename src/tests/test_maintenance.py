import pytest
from datetime import date
from src.model.property import Property
from src.model.maintenance import Event, EventLog, MaintenanceRequest, Renovation

# Fixtures
@pytest.fixture
def sample_property():
    return Property("P001", "City Center", 120.0, 1500.0, "Olivia Homes")

@pytest.fixture
def sample_event():
    return Event(True, "New maintenance request logged.")

@pytest.fixture
def event_log(sample_event):
    return EventLog([sample_event])

@pytest.fixture
def maintenance_request(sample_property):
    return MaintenanceRequest(request_id=1, property= sample_property, request_date=date.today(), status="Pending")

@pytest.fixture
def renovation(sample_property):
    return Renovation(renovation_id=1, property=sample_property, dates=date.today(), cost=2500.0, description="Bathroom upgrade")

# Tests for Event and EventLog
def test_event_log_record_and_read(event_log):
    new_event = Event(True, "Property inspection complete.")
    event_log.record_event(new_event)

    assert "Property inspection complete." in event_log.read_new_messages()
    assert len(event_log.read_all_messages()) == 2

def test_event_log_only_reads_opened():
    log = EventLog([
        Event(True, "Message 1"),
        Event(False, "Message 2")
    ])
    new_messages = log.read_new_messages()
    assert "Message 1" in new_messages
    assert "Message 2" not in new_messages

# Tests for MaintenanceRequest
def test_approve_request_success(maintenance_request):
    event = maintenance_request.approve_request("Pending")
    assert maintenance_request.status == "Approved"
    assert isinstance(event, Event)
    assert "approved successfully" in event.text

def test_approve_request_failure(maintenance_request):
    maintenance_request.status = "Resolved"
    with pytest.raises(Exception) as exc_info:
        maintenance_request.approve_request("Resolved")
    assert "cannot be approved" in str(exc_info.value)

def test_resolve_request_success(maintenance_request):
    maintenance_request.status = "Approved"
    event = maintenance_request.resolve_request()
    assert maintenance_request.status == "Resolved"
    assert isinstance(event, Event)
    assert "resolved successfully" in event.text

# Tests for Renovation
def test_renovation_total_cost(renovation):
    assert renovation.get_total_cost() == 2500.0
