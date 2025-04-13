from datetime import date

from src.model.property import Property


class Event:
    def __init__(self, opened: bool, text: str):
        self.opened = opened
        self.text = text

    pass


class EventLog:
    def __init__(self, events: list[Event]):
        self.events = events

    def record_event(self, event: Event):
        self.events.append(event)

    def read_new_messages(self):
        new_messages = [event.text for event in self.events if event.opened]
        return new_messages

    def read_all_messages(self):
        all_messages = [event.text for event in self.events]
        return all_messages


class MaintenanceRequest:
    def __init__(self, request_id: int, property: Property, request_date: date, status: str):
        self.request_id = request_id
        self.property = property
        self.request_date = request_date
        self.status = status

    def approve_request(self, status: str):
        self.status = status
        if self.status == "Pending":
            self.status = "Approved"
            return Event(True, status + "Request approved successfully.")
        else:
            raise Exception("Request cannot be approved. Current status: " + self.status)

    def resolve_request(self):
        if self.status == "Approved":
            self.status = "Resolved"
        return Event(True, self.status + "Request resolved successfully.")


class Renovation:
    def __init__(self, renovation_id: int, property: Property, dates: date, cost: float, description: str):
        self.renovation_id = renovation_id
        self.property = property
        self.date = dates
        self.cost = cost
        self.description = description

    def get_total_cost(self):
        return self.cost


