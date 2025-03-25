

from src.model.rentalcompany import RentalCompany

def test_rental_company():
    company = RentalCompany("Test Company")
    assert company.name == "Test Company"
    assert isinstance(company, RentalCompany)

    assert False, "This was just an example. Add more tests here"