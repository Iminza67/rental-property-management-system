
from src.model.property import Property

class RentalCompany:
    def __init__(self, company_name: str):
        self.company_name: str = company_name
        self.properties_list: list[Property] = []
        self.contracts = []

    def add_property(self, property: Property):
        if property not in self.properties_list:
            self.properties_list.append(property)
            print(f"Property {property.property_id} added to {self.company_name}.")
        else:
            print(f"Property {property.property_id} already exists.")

    def remove_property(self, property: Property):
        if property in self.properties_list:
            self.properties_list.remove(property)
            print(f"Property {property.property_id} removed from {self.company_name}.")
        else:
            print(f"Property {property.property_id} not found.")

    def get_income(self):
        total_income = 0
        for contract in self.contracts:
            total_income += contract.get_total_income()
        return total_income

    def analyze_occupancy(self):
        if not self.properties_list:
            return "No properties available for occupancy analysis."
        occupied_properties = sum(1 for p in self.properties_list if p.get_status() == "Occupied")
        occupancy_rate = occupied_properties / len(self.properties_list) * 100
        return f"Occupancy Rate: {occupancy_rate:.2f}%"

class PropertySearch:
    def search_by_location(self, rental_company: RentalCompany, location: str):
        return [p for p in rental_company.properties_list if location.lower() in p.address.lower()]

    def search_by_price(self, rental_company: RentalCompany, min_price: float, max_price: float):
        return [p for p in rental_company.properties_list if min_price <= p.price <= max_price]

    def search_by_availability(self, rental_company: RentalCompany):
        return [p for p in rental_company.properties_list if p.get_status() == "Available"]

class Navigation:
    def __init__(self, rental_company: RentalCompany):
        self.rental_company = rental_company

    def calculate_distance(self, location1: str, location2: str) -> float:

        return abs(hash(location1) - hash(location2)) % 100

    def get_nearest_available_property(self, location: str):
        nearest_property = None
        min_distance = float('inf')
        for property in self.rental_company.properties_list:
            if property.get_status() == "Available":
                distance = self.calculate_distance(location, property.address)
                if distance < min_distance:
                    min_distance = distance
                    nearest_property = property
        return nearest_property

class RentalAnalytics:
    def vacancy_rate(self, rental_company: RentalCompany):
        if not rental_company.properties_list:
            return "No properties available for occupancy analysis."
        occupied = sum(1 for p in rental_company.properties_list if p.get_status() == "Occupied")
        vacancy_rate = (len(rental_company.properties_list) - occupied) / len(rental_company.properties_list) * 100
        return f"Vacancy Rate: {vacancy_rate:.2f}%"

    def loss_due_to_vacancy(self, rental_company: RentalCompany):
        total_loss = sum(p.calculate_cost() for p in rental_company.properties_list if p.get_status() == "Available")
        return f"Total Loss Due to Vacancy: {total_loss:.2f}"

    def average_rent(self, rental_company: RentalCompany):
        if not rental_company.properties_list:
            return "No properties available for rent analysis."
        total_rent = sum(p.price for p in rental_company.properties_list)
        average_rent = total_rent / len(rental_company.properties_list)
        return f"Average Rent: {average_rent:.2f}"

    def total_revenue(self, rental_company: RentalCompany):
        total_revenue = sum(p.calculate_cost() for p in rental_company.properties_list)
        return f"Total Revenue: {total_revenue:.2f}"

    def revenue_analysis(self, rental_company: RentalCompany):
        revenue_analysis = {p.property_id: p.calculate_cost() for p in rental_company.properties_list}
        return revenue_analysis

    def turnover_rate(self, rental_company: RentalCompany):
        if not rental_company.properties_list:
            return "No properties available for turnover analysis."
        turnover = sum(1 for p in rental_company.properties_list if p.get_status() == "Available")
        turnover_rate = turnover / len(rental_company.properties_list) * 100
        return f"Turnover Rate: {turnover_rate:.2f}%"

class MonthlyReport:
    def __init__(self, report_id: int, month: int, year: int, vacancy_percentage: float = 0.0, income: float = 0.0, loss_due_to_vacancy: float = 0.0):
        self.report_id = report_id
        self.month = month
        self.year = year
        self.vacancy_percentage = vacancy_percentage
        self.income = income
        self.loss_due_to_vacancy = loss_due_to_vacancy

    def generate_report(self, properties: list[Property]):
        if not properties:
            return {"error": "No properties available."}

        total_unoccupied = sum(1 for p in properties if p.get_status() == "Available")
        self.vacancy_percentage = (total_unoccupied / len(properties)) * 100
        self.income = sum(p.calculate_cost() for p in properties if p.get_status() == "Occupied")
        self.loss_due_to_vacancy = sum(p.calculate_cost() for p in properties if p.get_status() == "Available")

        return {
            "Report ID": self.report_id,
            "Month": self.month,
            "Year": self.year,
            "Vacancy Percentage": self.vacancy_percentage,
            "Income": self.income,
            "Loss Due to Vacancy": self.loss_due_to_vacancy
        }
