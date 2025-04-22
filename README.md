
# Rental Property Management System

## Overview

This project is a Python-based implementation of a **Rental Property Management System** for a rental company. The system tracks rental properties, rental contracts, payments, residents, and various maintenance requests. It provides analytics, search functionalities, and notifications to improve the overall management of rental properties.

The system was built using Object-Oriented Programming (OOP) principles to ensure scalability, reusability, and efficient management of rental properties.

## Features

- **Basic Class Structure**: Defines rental properties, leases, and manages residents and payments.
- **Payment System**: Tracks rent payments, handles late payments with penalties, and generates transaction histories.
- **Property Maintenance & Renovations**: Manages maintenance requests and renovation history for properties.
- **Analytics & Reports**: Generates vacancy rates, rental income, turnover rates, and financial loss from vacancies.
- **Property Search**: Allows users to search for properties based on location, price, and availability.
- **Event Logging & Notifications**: Tracks system events (lease signed, rent paid) and sends notifications to renters (e.g., late payments).
- **Reviews & Complaints**: Enables residents to submit reviews and complaints about properties.

## Requirements

- Python 3.x
- `pytest` for testing

You can install `pytest` using pip:

```bash
pip install pytest
```

## Project Structure

```
rental-property-management/
│
├── src/                     # Source code
│   ├── __init__.py           # Initialization file
│   ├── rental_system.py      # Main classes (RentalCompany, Property, LeaseAgreement, etc.)
│   ├── maintenance.py        # MaintenanceRequest and Renovation classes
│   ├── analytics.py          # RentalAnalytics and MonthlyReport classes
│   ├── search.py             # PropertySearch class
│   ├── event_log.py          # EventLog and Notification classes
│   └── review_complaint.py   # Review and Complaint classes
│
├── tests/                    # Test cases for all functionalities
│   ├── test_rental_system.py # Tests for rental system functionality
│   ├── test_payment.py       # Tests for payment-related features
│   ├── test_maintenance.py   # Tests for maintenance and renovation features
│   ├── test_analytics.py     # Tests for analytics and report generation
│   ├── test_search.py        # Tests for property search functionality
│   ├── test_event_log.py     # Tests for event logging and notifications
│   └── test_review_complaint.py # Tests for reviews and complaints
│
├── scripts/                  # Example scripts to demonstrate system usage
│   └── rental_management_demo.py # Sample script simulating the rental management workflow
│
└── README.md                 # Project documentation
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Iminza67/rental-property-management.git
```

2. Navigate to the project directory:

```bash
cd rental-property-management
```

3. Install any necessary dependencies:

```bash
pip install -r requirements.txt
```

4. Run the project demo:

```bash
python scripts/rental_management_demo.py
```

5. Run tests to ensure functionality:

```bash
pytest
```

## Usage

### 1. **Rental System Management**

The system allows the creation, renewal, and termination of leases, tracking rent payments, and managing overdue payments. Properties can be added with attributes such as address, size, price, and facilities.

### 2. **Payment System**

Rent payments are tracked, with late payments handled separately, including penalties. A `TransactionHistory` class stores all payment transactions.

### 3. **Property Maintenance**

Property managers can approve or reject maintenance requests. The system tracks renovation history and costs for each property.

### 4. **Analytics & Reports**

The system generates various reports, including vacancy rates, total rental income per month, tenant turnover rates, and loss due to vacancy.

### 5. **Search Functionality**

Users can search for properties by location, price, and availability. The system also helps navigate to the nearest available property.

### 6. **Event Logging & Notifications**

Important system events (e.g., lease signing, rent payment) are logged, and notifications are sent to renters for lease expirations or late payments.

### 7. **Reviews & Complaints**

Residents can leave reviews and file complaints about the properties they are renting. This feedback is useful for property managers.

## Testing

This project uses `pytest` to automate tests for various functionalities. To run the tests, execute the following command:

```bash
pytest
```

Tests include:

- Lease management functionalities
- Payment system (including overdue payments)
- Property maintenance and renovation handling
- Analytics and report generation
- Property search
- Event logging and notifications
- Review and complaint submission

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspiration from Object-Oriented Design principles for developing scalable systems.

---

Feel free to modify and improve the system to meet additional requirements or handle edge cases.

Happy coding! 🎉
```
