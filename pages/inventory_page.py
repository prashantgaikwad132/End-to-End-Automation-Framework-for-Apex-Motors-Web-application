"""
InventoryPage — POM for /inventory
"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class InventoryPage(BasePage):
    HEADING = "h1:has-text('Our Collection')"
    SEARCH_INPUT = "input[placeholder='Search vehicles...']"
    CATEGORY_BUTTONS = "button"
    VEHICLE_CARDS = ".group.cursor-pointer"
    NO_RESULTS_MSG = "text=No vehicles match"
    CARD_TITLE = "h3"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)

    @allure.step("Open Inventory page")
    def open(self):
        self.navigate("/inventory")
        self.page.wait_for_selector(self.HEADING)
        return self

    @allure.step("Search for: {query}")
    def search(self, query: str):
        self.page.locator(self.SEARCH_INPUT).fill(query)
        self.page.wait_for_timeout(400)
        return self

    @allure.step("Clear search")
    def clear_search(self):
        self.page.locator(self.SEARCH_INPUT).fill("")
        self.page.wait_for_timeout(400)
        return self

    @allure.step("Filter category: {category}")
    def filter_category(self, category: str):
        self.page.get_by_role("button", name=category, exact=True).click()
        self.page.wait_for_timeout(500)
        return self

    @allure.step("Get visible card count")
    def get_card_count(self) -> int:
        return self.page.locator(self.VEHICLE_CARDS).count()

    @allure.step("Get all card titles")
    def get_card_titles(self) -> list[str]:
        return self.page.locator(self.CARD_TITLE).all_inner_texts()

    @allure.step("Click vehicle: {name}")
    def click_vehicle(self, name: str):
        self.page.get_by_text(name, exact=True).first.click()
        self.page.wait_for_timeout(300)
        return self

    @allure.step("Assert no results shown")
    def assert_no_results(self):
        expect(self.page.locator(self.NO_RESULTS_MSG)).to_be_visible()
        return self

    @allure.step("Get vehicle spec from card: {name}")
    def get_vehicle_hp(self, name: str) -> str:
        card = self.page.locator(self.VEHICLE_CARDS).filter(has_text=name)
        return card.locator("text=/\\d+ HP/").inner_text()
