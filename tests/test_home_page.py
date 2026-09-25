"""
test_home_page.py — Home page smoke & functional tests
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.header_nav import HeaderNav


@allure.epic("Apex Motors")
@allure.feature("Home Page")
class TestHomePage:

    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.home = HomePage(page, config.BASE_URL)
        self.nav = HeaderNav(page, config.BASE_URL)
        self.home.open()

    @allure.story("Hero Section")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_hero_section_renders(self):
        """TC-001: Hero section displays heading and CTA buttons."""
        self.home.verify_hero_section()
        assert self.home.is_visible("a:has-text('Explore Collection')")
        assert self.home.is_visible("a:has-text('Book a Test Drive')")

    @allure.story("Hero Section")
    @pytest.mark.smoke
    def test_explore_collection_navigates_to_inventory(self, page):
        """TC-002: 'Explore Collection' CTA navigates to /inventory."""
        self.home.click_explore_collection()
        page.wait_for_url("**/inventory")
        self.home.assert_url_contains("/inventory")

    @allure.story("Hero Section")
    @pytest.mark.smoke
    def test_book_test_drive_navigates_to_contact(self, page):
        """TC-003: 'Book a Test Drive' CTA navigates to /contact."""
        self.home.click_book_test_drive()
        page.wait_for_url("**/contact")
        self.home.assert_url_contains("/contact")

    @allure.story("Featured Vehicles")
    @pytest.mark.inventory
    def test_all_vehicles_displayed_by_default(self):
        """TC-004: All 6 vehicles shown when 'All' filter active."""
        count = self.home.get_vehicle_card_count()
        assert count == 6, f"Expected 6 cards, got {count}"

    @allure.story("Featured Vehicles")
    @pytest.mark.inventory
    def test_filter_suv_category(self, test_data):
        """TC-005: SUV filter shows only SUV vehicles."""
        self.home.filter_by_category("SUV")
        count = self.home.get_vehicle_card_count()
        assert count == test_data["category_counts"]["SUV"]

    @allure.story("Featured Vehicles")
    @pytest.mark.inventory
    def test_filter_sports_category(self, test_data):
        """TC-006: Sports filter shows correct count."""
        self.home.filter_by_category("Sports")
        count = self.home.get_vehicle_card_count()
        assert count == test_data["category_counts"]["Sports"]

    @allure.story("Featured Vehicles")
    @pytest.mark.inventory
    def test_filter_reset_to_all(self):
        """TC-007: Switching back to 'All' restores full inventory."""
        self.home.filter_by_category("SUV")
        self.home.filter_by_category("All")
        assert self.home.get_vehicle_card_count() == 6

    @allure.story("Stats Section")
    @pytest.mark.smoke
    def test_stats_section_visible(self):
        """TC-008: Stats section with KPIs is visible."""
        self.home.verify_stats_section()

    @allure.story("Branding")
    @pytest.mark.smoke
    def test_logo_and_brand(self):
        """TC-009: APEX MOTORS logo renders in header."""
        self.nav.verify_logo()
