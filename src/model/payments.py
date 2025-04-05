from datetime import datetime

from src.model import LeaseAgreement, User

class Payment:
    def __init__(self,lease: 'LeaseAgreement', amount: float, due_date: str):
        self.amount = amount
        self.lease = lease
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        self.payment_date = None
        self.status = "Pending"

    def process_payment(self, payment_date: str):
        self.payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()
        if self.payment_date <= self.due_date:
            self.status = "Paid"
        else:
            self.status = "Late"
    
    def __str__(self):
        return f"Payment of {self.amount} for lease {self.lease} on {self.due_date} - Status: {self.status}"
        
class LatePayment(Payment):
    def __init__(self, lease: 'LeaseAgreement', amount: float, due_date: str, days_late: float):
        super().__init__(lease, amount, due_date)
        self.days_late = days_late
        self.late_fee = self._calculate_late_fee()
        self.total_amount = self.amount + self.late_fee
        self.status = "Late"

    def _calculate_penalty(self):
        base_penalty = self.amount * 0.05  # 5% of the payment amount
        additional_penalty = (self.days_late - 1) * 0.02 * self.amount if self.days_late > 1 else 0
        return round(base_penalty + additional_penalty, 2)
    
    @classmethod
    def from_payment(cls, payment: Payment):
        days_late = (datetime.now().date() - payment.due_date).days
        return cls(payment.lease, payment.amount, payment.due_date.strftime("%Y-%m-%d"), days_late)
    def __str__(self):
        return f"Late Payment of {self.total_amount} for lease {self.lease} on {self.due_date} - Days Late: {self.days_late}, Late Fee: {self.late_fee}"

class PaymentHistory:
    def __init__(self):
        self.payments = []

    def add_payment(self, payment: Payment):
        self.payments.append(payment)
    
    def get_unpaid_payments(self):
        return [payment for payment in self.payments if payment.status == "Pending"]

    def get_payments(self):
        return self.payments
    
    def total_revenue(self, start_date: str, end_date: str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        return sum(
            t.amount if not isinstance(t, LatePayment) else t.total_amount
            for t in self.transactions
            if t.status == "Paid" and start_date <= t.payment_date <= end_date
        )

    def get_total_payments(self):
        return sum(payment.amount for payment in self.payments if payment.status == "Paid")
    
class Notification:
    def __init__(self,notification_id: int, message: str, recipient: User):
        self.notification_id = notification_id
        self.message = message
        self.recipient = recipient
        self.status = "Unread"
    
    def check_unpaid_payments(self):
        today = datetime.now().date()
        reminders = []
        for payment in self.recipient.payment_history.get_unpaid_payments():
            if payment.due_date < today:
                days_late = (today - payment.due_date).days
                reminders.append(LatePayment.from_payment(payment))(
                    f"Reminder: Payment of {payment.amount} for lease {payment.lease} is overdue by {days_late} days."
                    f"Please pay as soon as possible.{payment.lease.resident.name}")
        return reminders