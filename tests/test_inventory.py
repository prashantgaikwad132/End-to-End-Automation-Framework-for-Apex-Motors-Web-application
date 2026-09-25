"""
test_inventory.py — Inventory page tests: filtering, search, specs validation
"""

import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.vehicle_modal_page import VehicleModalPage


@allure.epic("Apex Motors")
@allure.feature("Inventory")
class TestInventory:

    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.inventory = InventoryPage(page, config.BASE_URL)
        self.modal = VehicleModalPage(page, config.BASE_URL)
        self.inventory.open()

    @allure.story("Search")
    @pytest.mark.inventory
    @pytest.mark.parametrize("query,expected_count", [
        ("Veloce", 1),
        ("Atlas", 1),
        ("NonExistentBrand", 0),
    ])
    def test_search_filters_vehicles(self, query, expected_count):
        """TC-010: Search filters vehicles by name/brand."""
        self.inventory.search(query)
        count = self.inventory.get_card_count()
        assert count == expected_count, f"Search '{query}': expected {expected_count}, got {count}"

    @allure.story("Search")
    @pytest.mark.inventory
    def test_search_no_results_message(self):
        """TC-011: 'No vehicles match' shown for zero results."""
        self.inventory.search("ZZZZZZZZZ")
        self.inventory.assert_no_results()

    @allure.story("Category Filter")
    @pytest.mark.inventory
    @pytest.mark.parametrize("category,expected", [
        ("SUV", 1), ("Sports", 2), ("Sedan", 1), ("Coupe", 1), ("Convertible", 1), ("All", 6),
    ])
    def test_category_filtering(self, category, expected):
        """TC-012: Each category filter shows correct vehicle count."""
        self.inventory.filter_category(category)
        assert self.inventory.get_card_count() == expected

    @allure.story("Vehicle Modal")
    @pytest.mark.inventory
    def test_vehicle_modal_opens_with_correct_data(self, test_data):
        """TC-013: Clicking a vehicle opens modal with correct specs."""
        vehicle = test_data["vehicles"][0]  # Veloce GT-R
        self.inventory.click_vehicle(vehicle["name"])
        assert self.modal.is_open()
        assert self.modal.get_name() == vehicle["name"]
        self.modal.verify_spec_labels()

    @allure.story("Vehicle Modal")
    @pytest.mark.inventory
    def test_modal_close_button(self, test_data):
        """TC-014: Modal closes via close button."""
        self.inventory.click_vehicle(test_data["vehicles"][0]["name"])
        assert self.modal.is_open()
        self.modal.close()
        assert not self.modal.is_open()

    @allure.story("Vehicle Modal")
    @pytest.mark.inventory
    def test_modal_inquire_navigates_to_contact(self, page, test_data):
        """TC-015: 'Inquire Now' in modal navigates to /contact."""
        self.inventory.click_vehicle(test_data["vehicles"][0]["name"])
        self.modal.click_inquire()
        page.wait_for_url("**/contact")
        assert "/contact" in page.url

    @allure.story("Vehicle Modal")
    @pytest.mark.inventory
    def test_modal_book_test_drive_navigates(self, page, test_data):
        """TC-016: 'Book Test Drive' in modal navigates to /contact."""
        self.inventory.click_vehicle(test_data["vehicles"][1]["name"])
        self.modal.click_book_test_drive()
        page.wait_for_url("**/contact")
        assert "/contact" in page.url

    @allure.story("Data Integrity")
    @pytest.mark.regression
    def test_vehicle_hp_displayed_on_card(self, test_data):
        """TC-017: HP value on card matches expected data."""
        vehicle = test_data["vehicles"][4]  # Viper Evo, 740 HP
        hp_text = self.inventory.get_vehicle_hp(vehicle["name"])
        assert str(vehicle["horsepower"]) in hp_text

    @allure.story("Combined Filters")
    @pytest.mark.regression
    def test_search_combined_with_category(self):
        """TC-018: Search + category filter work together."""
        self.inventory.filter_category("Sports")
        self.inventory.search("Viper")
        assert self.inventory.get_card_count() == 1
        titles = self.inventory.get_card_titles()
        assert "Viper Evo" in titles
