"""
HeaderNav — shared header / navigation component POM
"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HeaderNav(BasePage):
    LOGO = "text=APEX"
    NAV_HOME = "nav >> a:has-text('Home')"
    NAV_INVENTORY = "nav >> a:has-text('Inventory')"
    NAV_ABOUT = "nav >> a:has-text('About')"
    NAV_CONTACT = "nav >> a:has-text('Contact')"
    MOBILE_TOGGLE = "button[aria-label='Toggle menu']"

    NAV_MAP = {
        "Home": NAV_HOME,
        "Inventory": NAV_INVENTORY,
        "About": NAV_ABOUT,
        "Contact": NAV_CONTACT,
    }

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)

    @allure.step("Click nav link: {name}")
    def go_to(self, name: str):
        selector = self.NAV_MAP[name]
        self.page.locator(selector).first.click()
        self.page.wait_for_load_state("domcontentloaded")
        return self

    @allure.step("Open mobile menu")
    def open_mobile_menu(self):
        self.page.locator(self.MOBILE_TOGGLE).click()
        self.page.wait_for_timeout(400)
        return self

    @allure.step("Verify logo visible")
    def verify_logo(self):
        expect(self.page.get_by_text("APEX").first).to_be_visible()
        return self
