import pytest
from src.model.property import Property
from src.model.rentalcompany import (
    RentalCompany, PropertySearch, Navigation,
    RentalAnalytics, MonthlyReport
)

@pytest.fixture
def sample_property_1():
    return Property("P001", "City Center", 120.0, 1500.0, "Olivia Homes")

@pytest.fixture
def sample_property_2():
    return Property("P002", "Suburbs", 80.0, 1000.0, "Olivia Homes")

@pytest.fixture
def rental_company(sample_property_1, sample_property_2):
    company = RentalCompany("Olivia Homes")
    company.add_property(sample_property_1)
    company.add_property(sample_property_2)
    return company

def test_add_and_remove_property(rental_company, sample_property_1):
    rental_company.remove_property(sample_property_1)
    assert sample_property_1 not in rental_company.properties_list

def test_analyze_occupancy(rental_company, sample_property_1):
    assert rental_company.analyze_occupancy() == "Occupancy Rate: 0.00%"
    sample_property_1.is_occupied = True
    assert "Occupancy Rate: 50.00%" in rental_company.analyze_occupancy()

def test_search_by_location(rental_company):
    search = PropertySearch()
    results = search.search_by_location(rental_company, "City")
    assert len(results) == 1
    assert results[0].address == "City Center"

def test_search_by_price(rental_company):
    search = PropertySearch()
    results = search.search_by_price(rental_company, 900, 1100)
    assert len(results) == 1
    assert results[0].price == 1000.0

def test_search_by_availability(rental_company, sample_property_1):
    search = PropertySearch()
    sample_property_1.is_occupied = True
    results = search.search_by_availability(rental_company)
    assert len(results) == 1
    assert results[0].property_id == "P002"

def test_navigation_get_nearest_available(rental_company):
    nav = Navigation(rental_company)
    result = nav.get_nearest_available_property("Downtown")
    assert isinstance(result, Property)

def test_rental_analytics_metrics(rental_company, sample_property_1):
    analytics = RentalAnalytics()
    sample_property_1.is_occupied = True

    assert "Vacancy Rate" in analytics.vacancy_rate(rental_company)
    assert "Total Loss Due to Vacancy" in analytics.loss_due_to_vacancy(rental_company)
    assert "Average Rent" in analytics.average_rent(rental_company)
    assert "Total Revenue" in analytics.total_revenue(rental_company)
    assert isinstance(analytics.revenue_analysis(rental_company), dict)
    assert "Turnover Rate" in analytics.turnover_rate(rental_company)

def test_monthly_report_generation(rental_company, sample_property_1):
    report = MonthlyReport(report_id=1, month=4, year=2025)
    sample_property_1.is_occupied = True
    result = report.generate_report(rental_company.properties_list)

    assert isinstance(result, dict)
    assert result["Report ID"] == 1
    assert result["Month"] == 4
    assert "Vacancy Percentage" in result
