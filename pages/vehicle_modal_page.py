"""
VehicleModalPage — POM for the vehicle detail modal overlay
"""

import allure
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class VehicleModalPage(BasePage):
    MODAL_CONTAINER = ".fixed.inset-0.z-50"
    CLOSE_BTN = "button[aria-label='Close']"
    VEHICLE_NAME = "h2"
    VEHICLE_BRAND_YEAR = "text=/[A-Z]+.*·.*\\d{4}/"
    HP_SPEC = "text=/\\d+ HP/"
    ACCELERATION_SPEC = "text=/\\d+\\.\\d+s 0-60/"
    TRANSMISSION_SPEC = "text=Transmission"
    FUEL_SPEC = "text=Fuel Type"
    PRICE = "text=/\\$[\\d,]+/"
    INQUIRE_BTN = "a:has-text('Inquire Now')"
    BOOK_BTN = "a:has-text('Book Test Drive')"
    ENGINE_LABEL = "text=Engine"
    DRIVETRAIN_LABEL = "text=Drivetrain"
    TOP_SPEED_LABEL = "text=Top Speed"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)

    @allure.step("Verify modal is open")
    def is_open(self) -> bool:
        return self.page.locator(self.MODAL_CONTAINER).is_visible()

    @allure.step("Close modal")
    def close(self):
        self.page.locator(self.CLOSE_BTN).click()
        self.page.wait_for_timeout(400)
        return self

    @allure.step("Get vehicle name from modal")
    def get_name(self) -> str:
        return self.page.locator(f"{self.MODAL_CONTAINER} h2").inner_text()

    @allure.step("Get HP value")
    def get_horsepower(self) -> str:
        return self.page.locator(f"{self.MODAL_CONTAINER} >> text=/\\d+ HP/").first.inner_text()

    @allure.step("Get acceleration")
    def get_acceleration(self) -> str:
        return self.page.locator(f"{self.MODAL_CONTAINER} >> text=0-60 mph").locator("..").locator("p.font-semibold").inner_text()

    @allure.step("Get transmission")
    def get_transmission(self) -> str:
        return self.page.locator(f"{self.MODAL_CONTAINER} >> text=Transmission").locator("..").locator("p.font-semibold").inner_text()

    @allure.step("Get fuel type")
    def get_fuel_type(self) -> str:
        return self.page.locator(f"{self.MODAL_CONTAINER} >> text=Fuel Type").locator("..").locator("p.font-semibold").inner_text()

    @allure.step("Click 'Inquire Now'")
    def click_inquire(self):
        self.page.locator(f"{self.MODAL_CONTAINER} >> {self.INQUIRE_BTN}").click()
        return self

    @allure.step("Click 'Book Test Drive'")
    def click_book_test_drive(self):
        self.page.locator(f"{self.MODAL_CONTAINER} >> {self.BOOK_BTN}").click()
        return self

    @allure.step("Verify all spec labels present")
    def verify_spec_labels(self):
        modal = self.page.locator(self.MODAL_CONTAINER)
        for label in ["Horsepower", "0-60 mph", "Transmission", "Fuel Type", "Engine", "Drivetrain", "Top Speed"]:
            expect(modal.get_by_text(label, exact=True).first).to_be_visible()
        return self
