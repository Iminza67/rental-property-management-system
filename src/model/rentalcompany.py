from src.model.property import Property

class RentalCompany():

    def __init__(self, company_name: str):
        self.company_name = company_name
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
            print("No properties available for occupancy analysis.")
        else:
            occupied_properties = 0
            for property in self.properties_list:
                if property.get_status() == "Occupied":
                    occupied_properties += 1
            occupancy_rate = occupied_properties / len(self.properties_list) * 100
            print(f"Occupancy Rate: {occupancy_rate:.2f}%")
                
    # Your code goes here.


