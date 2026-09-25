"""
BasePage — abstract layer for all page objects.
Wraps Playwright Page with reusable, logged interaction helpers.
"""

import allure
from playwright.sync_api import Page, Locator, expect
from utils.logger import get_logger

logger = get_logger("BasePage")


class BasePage:
    def __init__(self, page: Page, base_url: str = ""):
        self.page = page
        self.base_url = base_url

    # ── Navigation ───────────────────────────────────────────────────────

    @allure.step("Navigate to {path}")
    def navigate(self, path: str = "/"):
        url = f"{self.base_url}{path}" if self.base_url else path
        self.page.goto(url, wait_until="domcontentloaded")
        logger.info(f"Navigated to {url}")

    @allure.step("Get current URL")
    def current_url(self) -> str:
        return self.page.url

    # ── Waits & Visibility ───────────────────────────────────────────────

    @allure.step("Wait for selector: {selector}")
    def wait_for(self, selector: str, state: str = "visible", timeout: int = 15000):
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

    @allure.step("Element visible: {selector}")
    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    # ── Interaction helpers ──────────────────────────────────────────────

    @allure.step("Click: {selector}")
    def click(self, selector: str, **kwargs):
        self.page.locator(selector).click(**kwargs)
        logger.info(f"Clicked {selector}")

    @allure.step("Fill '{selector}' with value")
    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    @allure.step("Select option in '{selector}'")
    def select_option(self, selector: str, value: str):
        self.page.locator(selector).select_option(value)

    @allure.step("Get text: {selector}")
    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    @allure.step("Get element count: {selector}")
    def count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    # ── Assertions ───────────────────────────────────────────────────────

    @allure.step("Assert text visible: {text}")
    def assert_text_visible(self, text: str):
        expect(self.page.get_by_text(text, exact=False).first).to_be_visible()

    @allure.step("Assert title contains: {substring}")
    def assert_title_contains(self, substring: str):
        expect(self.page).to_have_title(f".*{substring}.*")

    @allure.step("Assert URL contains: {path}")
    def assert_url_contains(self, path: str):
        expect(self.page).to_have_url(f".*{path}.*")

    # ── Screenshots ──────────────────────────────────────────────────────

    @allure.step("Take screenshot")
    def screenshot(self, path: str = "reports/screenshots/manual.png"):
        self.page.screenshot(path=path, full_page=True)
