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
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator(self.HEADING)).to_be_visible(timeout=15000)
        expect(self.page.locator(self.VEHICLE_CARDS)).to_have_count(6, timeout=15000)
        return self

    @allure.step("Search for: {query}")
    def search(self, query: str):
        search_box = self.page.locator(self.SEARCH_INPUT)
        expect(search_box).to_be_visible()
        search_box.click()
        search_box.fill(query)
        expect(search_box).to_have_value(query)
        # Self-heal if React swallowed the synthetic onChange during Docker CPU spike
        if query and self.page.locator(self.VEHICLE_CARDS).count() == 6:
            try:
                expect(self.page.locator(self.VEHICLE_CARDS)).not_to_have_count(6, timeout=1500)
            except AssertionError:
                search_box.clear()
                search_box.press_sequentially(query, delay=30)
        return self

    @allure.step("Clear search")
    def clear_search(self):
        search_box = self.page.locator(self.SEARCH_INPUT)
        search_box.fill("")
        expect(search_box).to_have_value("")
        expect(self.page.locator(self.VEHICLE_CARDS)).to_have_count(6)
        return self

    @allure.step("Filter category: {category}")
    def filter_by_category(self, category: str):
        btn = self.page.get_by_role("button", name=category, exact=True)
        expect(btn).to_be_visible()
        btn.scroll_into_view_if_needed()
        initial_class = btn.get_attribute("class") or ""
        btn.click()
        # Self-heal if React missed the click before hydration settled
        if category != "All":
            try:
                expect(btn).not_to_have_attribute("class", initial_class, timeout=1500)
            except AssertionError:
                btn.click()
        return self

    @allure.step("Verify filtered vehicle card count is {expected}")
    def assert_card_count(self, expected: int):
        """Auto-retries polling the DOM until the count matches expected."""
        expect(self.page.locator(self.VEHICLE_CARDS)).to_have_count(expected, timeout=10000)
        return self

    @allure.step("Get visible card count")
    def get_card_count(self) -> int:
        return self.page.locator(self.VEHICLE_CARDS).count()

    @allure.step("Get all card titles")
    def get_card_titles(self) -> list[str]:
        return self.page.locator(self.CARD_TITLE).all_inner_texts()

    @allure.step("Click vehicle: {name}")
    def click_vehicle(self, name: str):
        card = self.page.locator(self.VEHICLE_CARDS).filter(has_text=name).first
        expect(card).to_be_visible()
        card.scroll_into_view_if_needed()
        card.click()
        modal = self.page.locator(".fixed.inset-0.z-50")
        if not modal.is_visible():
            try:
                modal.wait_for(state="visible", timeout=2000)
            except Exception:
                card.click()
        return self

    @allure.step("Assert no results shown")
    def assert_no_results(self):
        expect(self.page.locator(self.NO_RESULTS_MSG)).to_be_visible(timeout=10000)
        return self

    @allure.step("Get vehicle spec from card: {name}")
    def get_vehicle_hp(self, name: str) -> str:
        card = self.page.locator(self.VEHICLE_CARDS).filter(has_text=name)
        return card.locator("text=/\\d+ HP/").inner_text()