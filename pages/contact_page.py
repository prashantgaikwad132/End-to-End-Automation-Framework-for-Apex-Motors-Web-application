"""
ContactPage — POM for /contact
"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ContactPage(BasePage):
    HEADING = "h1:has-text('Contact Us')"
    FORM = "form"
    FIRST_NAME = "form >> input >> nth=0"
    LAST_NAME = "form >> input >> nth=1"
    EMAIL = "form >> input[type='email']"
    INTEREST_SELECT = "form >> select"
    MESSAGE = "form >> textarea"
    SUBMIT_BTN = "button[type='submit']:has-text('Send Message')"
    SUCCESS_MSG = "text=Message Sent!"
    SEND_ANOTHER_BTN = "button:has-text('Send Another')"
    CALL_US = "text=Call Us"
    EMAIL_INFO = "text=concierge@apexmotors.com"
    SHOWROOM_HOURS = "text=Showroom Hours"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)

    @allure.step("Open Contact page")
    def open(self):
        self.navigate("/contact")
        self.page.wait_for_selector("h1")
        return self

    @allure.step("Fill contact form")
    def fill_form(self, first_name: str, last_name: str, email: str, interest: str, message: str):
        self.page.locator(self.FIRST_NAME).fill(first_name)
        self.page.locator(self.LAST_NAME).fill(last_name)
        self.page.locator(self.EMAIL).fill(email)
        self.page.locator(self.INTEREST_SELECT).select_option(label=interest)
        self.page.locator(self.MESSAGE).fill(message)
        return self

    @allure.step("Submit form")
    def submit(self):
        self.page.locator(self.SUBMIT_BTN).click()
        self.page.wait_for_timeout(300)
        return self

    @allure.step("Verify success state")
    def verify_success(self):
        expect(self.page.get_by_text("Message Sent!")).to_be_visible()
        expect(self.page.get_by_text("Our team will get back to you within 24 hours.")).to_be_visible()
        return self

    @allure.step("Click 'Send Another'")
    def click_send_another(self):
        self.page.locator(self.SEND_ANOTHER_BTN).click()
        self.page.wait_for_timeout(300)
        return self

    @allure.step("Verify form is displayed")
    def verify_form_visible(self):
        expect(self.page.locator(self.FORM)).to_be_visible()
        return self

    @allure.step("Verify contact info section")
    def verify_contact_info(self):
        expect(self.page.get_by_text("Call Us")).to_be_visible()
        expect(self.page.get_by_text("concierge@apexmotors.com")).to_be_visible()
        expect(self.page.get_by_text("Showroom Hours")).to_be_visible()
        return self

    @allure.step("Try submitting empty form")
    def try_submit_empty(self):
        self.page.locator(self.SUBMIT_BTN).click()
        return self
