"""
Apex Motors E2E Automation Framework — Conftest (Pytest Fixtures & Hooks)
"""

import os
import json
import pytest
import allure
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


# ── CLI Options ──────────────────────────────────────────────────────────────

def pytest_addoption(parser):
    parser.addoption("--browser-name", default="chromium", choices=["chromium", "firefox", "webkit"])
    parser.addoption("--headed", action="store_true", default=False)
    parser.addoption("--device", default=None, help="Playwright device descriptor e.g. 'iPhone 13'")
    parser.addoption("--base-url", default=None, help="Override base URL from .env")
    parser.addoption("--slow-mo", default=0, type=int, help="Slow‑motion delay in ms")


# ── Session-scoped fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def config(request):
    cfg = Config()
    if request.config.getoption("--base-url"):
        cfg.BASE_URL = request.config.getoption("--base-url")
    return cfg


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance, request, config) -> Browser:
    browser_name = request.config.getoption("--browser-name")
    headed = request.config.getoption("--headed")
    slow_mo = request.config.getoption("--slow-mo")
    launcher = getattr(playwright_instance, browser_name)
    browser = launcher.launch(headless=not headed, slow_mo=slow_mo)
    logger.info(f"Launched {browser_name} (headed={headed}, slow_mo={slow_mo})")
    yield browser
    browser.close()


# ── Per-test fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def context(browser, request, config) -> BrowserContext:
    device_name = request.config.getoption("--device")
    ctx_args = {
        "viewport": {"width": config.VIEWPORT_WIDTH, "height": config.VIEWPORT_HEIGHT},
        "base_url": config.BASE_URL,
        "record_video_dir": str(Path("reports/videos")),
    }
    if device_name:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            device = pw.devices.get(device_name, {})
        ctx_args.update(device)

    ctx = browser.new_context(**ctx_args)
    ctx.set_default_timeout(config.DEFAULT_TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context) -> Page:
    page = context.new_page()
    yield page
    page.close()


# ── Test data fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def test_data():
    data_path = Path(__file__).parent / "data" / "test_data.json"
    with open(data_path) as f:
        return json.load(f)


# ── Allure hooks ─────────────────────────────────────────────────────────────

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"reports/screenshots/FAIL_{item.name}_{ts}.png"
            Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            logger.error(f"Test FAILED: {item.name} — screenshot saved to {screenshot_path}")

    if report.when == "call":
        context = item.funcargs.get("context")
        if context:
            for v in context.pages:
                video = v.video
                if video:
                    try:
                        video_path = video.path()
                        allure.attach.file(str(video_path), name="Test Video", attachment_type=allure.attachment_type.WEBM)
                    except Exception:
                        pass
