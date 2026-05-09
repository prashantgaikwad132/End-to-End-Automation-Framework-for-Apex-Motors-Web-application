"""
test_responsive.py — Cross-device / responsive layout tests
"""

import pytest
import allure
from playwright.sync_api import expect


@allure.epic("Apex Motors")
@allure.feature("Responsive Design")
class TestResponsive:

    @allure.story("Mobile Navigation")
    @pytest.mark.responsive
    def test_mobile_hamburger_menu(self, browser, config):
        """TC-027: Mobile viewport shows hamburger menu with working links."""
        ctx = browser.new_context(
            viewport={"width": 390, "height": 844},
            base_url=config.BASE_URL,
        )
        page = ctx.new_page()
        page.goto(config.BASE_URL, wait_until="domcontentloaded")

        # Desktop nav should be hidden, hamburger visible
        expect(page.locator("button[aria-label='Toggle menu']")).to_be_visible()

        # Open mobile menu
        page.locator("button[aria-label='Toggle menu']").click()
        page.wait_for_timeout(500)

        # Navigate via mobile menu
        page.get_by_text("Inventory").click()
        page.wait_for_url("**/inventory")
        assert "/inventory" in page.url

        ctx.close()

    @allure.story("Tablet Layout")
    @pytest.mark.responsive
    def test_tablet_inventory_grid(self, browser, config):
        """TC-028: Tablet viewport renders inventory grid properly."""
        ctx = browser.new_context(
            viewport={"width": 768, "height": 1024},
            base_url=config.BASE_URL,
        )
        page = ctx.new_page()
        page.goto(f"{config.BASE_URL}/inventory", wait_until="domcontentloaded")
        page.wait_for_selector("h1")
        cards = page.locator(".group.cursor-pointer")
        assert cards.count() == 6
        ctx.close()

    @allure.story("Device Emulation")
    @pytest.mark.responsive
    @pytest.mark.parametrize("width,height", [
        (390, 844),   # iPhone 13
        (768, 1024),  # iPad
        (1920, 1080), # Desktop
    ])
    def test_hero_section_renders_all_viewports(self, browser, config, width, height):
        """TC-029: Hero section renders across all viewport sizes."""
        ctx = browser.new_context(
            viewport={"width": width, "height": height},
            base_url=config.BASE_URL,
        )
        page = ctx.new_page()
        page.goto(config.BASE_URL, wait_until="domcontentloaded")
        expect(page.locator("h1").first).to_be_visible()
        expect(page.get_by_text("Extraordinary")).to_be_visible()
        ctx.close()

    @allure.story("Mobile Contact Form")
    @pytest.mark.responsive
    def test_mobile_contact_form_usable(self, browser, config):
        """TC-030: Contact form is fully functional on mobile."""
        ctx = browser.new_context(
            viewport={"width": 390, "height": 844},
            base_url=config.BASE_URL,
        )
        page = ctx.new_page()
        page.goto(f"{config.BASE_URL}/contact", wait_until="domcontentloaded")
        page.wait_for_selector("form")

        page.locator("form >> input >> nth=0").fill("Mobile")
        page.locator("form >> input >> nth=1").fill("User")
        page.locator("form >> input[type='email']").fill("mobile@test.com")
        page.locator("form >> textarea").fill("Testing from mobile viewport.")
        page.locator("button[type='submit']").click()
        page.wait_for_timeout(500)
        expect(page.get_by_text("Message Sent!")).to_be_visible()

        ctx.close()
