"""
test_contact.py — Contact form E2E tests including negative/validation scenarios
"""

import pytest
import allure
from pages.contact_page import ContactPage


@allure.epic("Apex Motors")
@allure.feature("Contact / Lead Generation")
class TestContact:

    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.contact = ContactPage(page, config.BASE_URL)
        self.contact.open()

    @allure.story("Form Submission")
    @pytest.mark.contact
    @pytest.mark.smoke
    def test_successful_form_submission(self, test_data):
        """TC-019: Valid form submission shows success message."""
        data = test_data["contact_form_valid"][0]
        self.contact.fill_form(
            data["first_name"], data["last_name"],
            data["email"], data["interest"], data["message"]
        )
        self.contact.submit()
        self.contact.verify_success()

    @allure.story("Form Submission")
    @pytest.mark.contact
    def test_send_another_resets_form(self, test_data):
        """TC-020: 'Send Another' returns to empty form."""
        data = test_data["contact_form_valid"][0]
        self.contact.fill_form(
            data["first_name"], data["last_name"],
            data["email"], data["interest"], data["message"]
        )
        self.contact.submit()
        self.contact.verify_success()
        self.contact.click_send_another()
        self.contact.verify_form_visible()

    @allure.story("Negative Testing")
    @pytest.mark.contact
    @pytest.mark.negative
    def test_empty_form_prevented_by_html_validation(self, page):
        """TC-021: Submitting empty form triggers HTML5 required validation."""
        self.contact.try_submit_empty()
        # Form should NOT show success — HTML5 validation prevents submission
        assert not page.get_by_text("Message Sent!").is_visible()

    @allure.story("Contact Info")
    @pytest.mark.contact
    def test_contact_info_displayed(self):
        """TC-022: Phone, email, and showroom info are visible."""
        self.contact.verify_contact_info()

    @allure.story("Form Submission")
    @pytest.mark.contact
    @pytest.mark.parametrize("interest", [
        "General Inquiry", "Schedule Test Drive",
        "Vehicle Availability", "Financing Options",
    ])
    def test_all_interest_options_selectable(self, page, interest):
        """TC-023: All interest dropdown options are selectable."""
        page.locator("form >> select").select_option(label=interest)
        selected = page.locator("form >> select").input_value()
        assert selected == interest
