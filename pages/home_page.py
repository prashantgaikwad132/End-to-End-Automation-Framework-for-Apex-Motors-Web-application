"""
HomePage — POM for the Apex Motors landing page (/)
"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    # Selectors
    HERO_HEADING = "h1"
    HERO_SUBTITLE = "text=PREMIUM COLLECTION 2026"
    EXPLORE_COLLECTION_BTN = "a:has-text('Explore Collection')"
    BOOK_TEST_DRIVE_BTN = "a:has-text('Book a Test Drive')"
    FEATURED_SECTION = "text=Featured Vehicles"
    CATEGORY_BUTTONS = "button"
    VEHICLE_CARDS = ".group.cursor-pointer"
    STATS_SECTION = "text=Years of Excellence"
    BRAND_LOGO = "text=APEX"
    NAV_LINKS = "nav >> a"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)

    @allure.step("Open Home page")
    def open(self):
        self.navigate("/")
        return self

    @allure.step("Verify hero section is displayed")
    def verify_hero_section(self):
        expect(self.page.locator(self.HERO_HEADING).first).to_be_visible()
        self.assert_text_visible("Drive the")
        self.assert_text_visible("Extraordinary")
        return self

    @allure.step("Click 'Explore Collection'")
    def click_explore_collection(self):
        self.page.locator(self.EXPLORE_COLLECTION_BTN).click()
        return self

    @allure.step("Click 'Book a Test Drive'")
    def click_book_test_drive(self):
        self.page.locator(self.BOOK_TEST_DRIVE_BTN).click()
        return self

    @allure.step("Filter by category: {category}")
    def filter_by_category(self, category: str):
        self.page.get_by_role("button", name=category, exact=True).click()
        self.page.wait_for_timeout(500)
        return self

    @allure.step("Get visible vehicle card count")
    def get_vehicle_card_count(self) -> int:
        return self.page.locator(self.VEHICLE_CARDS).count()

    @allure.step("Click vehicle card: {name}")
    def click_vehicle_by_name(self, name: str):
        self.page.get_by_text(name, exact=True).first.click()
        return self

    @allure.step("Verify stats section")
    def verify_stats_section(self):
        self.assert_text_visible("Years of Excellence")
        return self

    @allure.step("Get all visible vehicle names")
    def get_vehicle_names(self) -> list[str]:
        cards = self.page.locator("h3").all_inner_texts()
        return [c for c in cards if c.strip()]
