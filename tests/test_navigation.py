"""
test_navigation.py — Cross-page navigation and routing tests
"""

import pytest
import allure
from pages.home_page import HomePage
from pages.header_nav import HeaderNav


@allure.epic("Apex Motors")
@allure.feature("Navigation")
class TestNavigation:

    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.home = HomePage(page, config.BASE_URL)
        self.nav = HeaderNav(page, config.BASE_URL)
        self.home.open()

    @allure.story("Desktop Navigation")
    @pytest.mark.navigation
    @pytest.mark.parametrize("link,expected_path,expected_text", [
        ("Inventory", "/inventory", "Our Collection"),
        ("About", "/about", "About Apex Motors"),
        ("Contact", "/contact", "Contact Us"),
    ])
    def test_nav_links(self, page, link, expected_path, expected_text):
        """TC-024: Header nav links route to correct pages."""
        self.nav.go_to(link)
        self.home.assert_url_contains(expected_path)
        self.home.assert_text_visible(expected_text)

    @allure.story("Desktop Navigation")
    @pytest.mark.navigation
    def test_logo_navigates_home(self, page):
        """TC-025: Clicking APEX logo returns to home."""
        self.nav.go_to("About")
        page.get_by_text("APEX").first.click()
        page.wait_for_url("**/")
        assert page.url.rstrip("/").endswith(".app") or page.url.endswith("/")

    @allure.story("SEO")
    @pytest.mark.smoke
    @pytest.mark.parametrize("path,expected_title", [
        ("/", "Apex Motors"),
        ("/inventory", "Inventory"),
        ("/about", "About"),
        ("/contact", "Contact"),
    ])
    def test_page_titles(self, page, config, path, expected_title):
        """TC-026: Each page has correct <title> tag."""
        page.goto(f"{config.BASE_URL}{path}", wait_until="domcontentloaded")
        assert expected_title.lower() in page.title().lower()
