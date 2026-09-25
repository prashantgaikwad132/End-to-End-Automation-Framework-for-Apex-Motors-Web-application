"""
AboutPage — POM for /about
"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AboutPage(BasePage):
    HEADING = "h1:has-text('About Apex Motors')"
    OUR_STORY_LABEL = "text=OUR STORY"
    VALUES = ["Trust & Transparency", "Uncompromising Quality", "Client-First Experience"]

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)

    @allure.step("Open About page")
    def open(self):
        self.navigate("/about")
        self.page.wait_for_selector("h1")
        return self

    @allure.step("Verify page content")
    def verify_content(self):
        expect(self.page.locator(self.HEADING)).to_be_visible()
        expect(self.page.get_by_text("OUR STORY")).to_be_visible()
        return self

    @allure.step("Verify core values displayed")
    def verify_values(self):
        for value in self.VALUES:
            expect(self.page.get_by_text(value)).to_be_visible()
        return self
