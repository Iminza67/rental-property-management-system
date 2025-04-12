from src.model.property import Property

class RentalCompany:
    def __init__(self, company_name: str):
        self.company_name: str = company_name
        self.properties_list = []
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
        else:
            print(f"Property {property} not found.")

    def get_income(self):
        total_income = 0
        for contract in self.contracts:
            total_income += contract.get_total_income()
        return total_income

    def analyze_occupancy(self):
        if not self.properties_list:
            return "No properties available for occupancy analysis."
        else:
            occupied_properties = 0
            for property in self.properties_list:
                if property.get_status() == "Occupied":
                    occupied_properties += 1
            occupancy_rate = occupied_properties / len(self.properties_list) * 100
            return f"Occupancy Rate: {occupancy_rate:.2f}%"
                
class PropertySearch:
    def search_by_location(self, rental_company: RentalCompany, location: str):
        results = []
        for property in rental_company.properties_list:
            if property.address == location:
                results.append(property)
        return results
    def search_by_price(self, rental_company: RentalCompany, min_price: float, max_price: float):
        results = []
        for property in rental_company.properties_list:
            if min_price <= property.price <= max_price:
                results.append(property)
        return results
    def search_by_availability(self, rental_company: RentalCompany):
        results = []
        for property in rental_company.properties_list:
            if property.get_status() == "Available":
                results.append(property)
        return results
    
class Navigation:
    def __init__(self, rental_company: RentalCompany):
        self.rental_company = rental_company

    def get_neareat_available_property(self, location: str):
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
        else:
            occupied_properties = 0
            for property in rental_company.properties_list:
                if property.get_status() == "Occupied":
                    occupied_properties += 1
            vacancy_rate = (len(rental_company.properties_list) - occupied_properties) / len(rental_company.properties_list) * 100
            return f"Vacancy Rate: {vacancy_rate:.2f}%"
        
    def average_rent(self, rental_company: RentalCompany):
        if not rental_company.properties_list:
            return "No properties available for rent analysis."
        else:
            total_rent = 0
            for property in rental_company.properties_list:
                total_rent += property.price
            average_rent = total_rent / len(rental_company.properties_list)
            return f"Average Rent: {average_rent:.2f}"
        
    def revenue_analysis(self, rental_company: RentalCompany):
        reveue_analysis = {}
        for property in rental_company.properties_list:
            reveue_analysis[property.property_id] = property.calculate_cost()
        return reveue_analysis
    
class MonthlyReport:
    def __init__(self, report_id: int, month: int, year: int, vacancy_percentage: float, income: float, loss_due_to_vacancy: float):
        self.report_id = report_id
        self.month = month
        self.year = year
        self.vacancy_percentage = vacancy_percentage
        self.income = income
        self.loss_due_to_vacancy = loss_due_to_vacancy
    
    def generate_report(self):
        self.loss_due_to_vacancy = self.property.is_occupied == False
        total_unoccupied = 0
        for property in self.property:
            if property.is_occupied == False:
                total_unoccupied += 1
        self.vacancy_percentage = (self.property.is_occupied == False)/total_unoccupied * 100
        self.income = self.property.calculate_cost()
        return {
            "Report ID": self.report_id,
            "Month": self.month,
            "Year": self.year,
            "Vacancy Percentage": self.vacancy_percentage,
            "Income": self.income,
            "Loss Due to Vacancy": self.loss_due_to_vacancy
        }
    
