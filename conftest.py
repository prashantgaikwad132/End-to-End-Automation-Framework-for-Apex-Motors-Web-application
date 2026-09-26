"""
Apex Motors E2E Automation Framework — Conftest (Pytest Fixtures & Hooks)
"""

import os
import re
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
    # Built-in options like --browser, --headed, --device are natively handled by pytest-playwright
    # and --base-url is natively handled by pytest-base-url.
    pass


# ── Report Hook for Test Status Inspection ───────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Store the execution report on the test item for teardown inspection
    setattr(item, f"rep_{report.when}", report)


# ── Session-scoped fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def config(request):
    cfg = Config()
    base_url_opt = request.config.getoption("--base-url", default=None)
    if base_url_opt:
        cfg.BASE_URL = base_url_opt
    return cfg


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance, request, config) -> Browser:
    browser_opt = request.config.getoption("--browser", default="chromium")
    browser_name = browser_opt[0] if isinstance(browser_opt, list) else browser_opt
    
    headed = request.config.getoption("--headed", default=False)
    slow_mo = request.config.getoption("--slowmo", default=0)
    
    launcher = getattr(playwright_instance, browser_name)
    browser = launcher.launch(headless=not headed, slow_mo=slow_mo)
    logger.info(f"Launched {browser_name} (headed={headed}, slow_mo={slow_mo})")
    yield browser
    browser.close()


# ── Per-test fixtures ────────────────────────────────────────────────────────

@pytest.fixture
def context(browser, request, config) -> BrowserContext:
    device_name = request.config.getoption("--device", default=None)
    video_dir = Path("reports/videos")
    video_dir.mkdir(parents=True, exist_ok=True)

    ctx_args = {
        "viewport": {"width": config.VIEWPORT_WIDTH, "height": config.VIEWPORT_HEIGHT},
        "base_url": config.BASE_URL,
        "record_video_dir": str(video_dir),
        "record_video_size": {"width": 1280, "height": 720},
    }
    if device_name:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            device = pw.devices.get(device_name, {})
        ctx_args.update(device)

    ctx = browser.new_context(**ctx_args)
    ctx.set_default_timeout(config.DEFAULT_TIMEOUT)

    # 1. Start tracing before test execution begins
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    # Capture any page references before closing context
    recorded_pages = list(ctx.pages)

    # 2. Check test execution result
    call_rep = getattr(request.node, "rep_call", None)
    is_failed = call_rep is not None and call_rep.failed

    # Prepare safe filesystem name for test artifacts
    safe_name = re.sub(r'[\\/*?:"<>|\[\]\s]', "_", request.node.name)

    # 3. Handle Trace Extraction on Failure
    trace_dir = Path("reports/traces")
    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_path = trace_dir / f"{safe_name}_trace.zip"

    if is_failed:
        ctx.tracing.stop(path=str(trace_path))
        if trace_path.exists():
            allure.attach.file(
                str(trace_path),
                name=f"Trace-{safe_name}",
                extension="zip"
            )
            logger.info(f"Trace saved and attached: {trace_path}")
    else:
        # Discard trace if test passed
        ctx.tracing.stop()

    # 4. Close context so Playwright finalizes writing .webm video files
    ctx.close()

    # 5. Handle Video Attachment to Allure on Failure
    if is_failed and recorded_pages:
        for p in recorded_pages:
            try:
                if p.video:
                    video_file = p.video.path()
                    if video_file and Path(video_file).exists():
                        allure.attach.file(
                            str(video_file),
                            name=f"Execution-Video-{safe_name}",
                            attachment_type=allure.attachment_type.WEBM
                        )
                        logger.info(f"Video attached to Allure: {video_file}")
            except Exception as e:
                logger.warning(f"Could not attach video for {safe_name}: {e}")


@pytest.fixture
def page(context, request) -> Page:
    page = context.new_page()
    yield page

    # Screenshot on failure while the page DOM is still alive
    call_rep = getattr(request.node, "rep_call", None)
    if call_rep and call_rep.failed:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[\\/*?:"<>|\[\]\s]', "_", request.node.name)
        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"FAIL_{safe_name}_{ts}.png"

        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            allure.attach.file(
                str(screenshot_path),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            logger.error(f"Test FAILED: {request.node.name} — screenshot saved to {screenshot_path}")
        except Exception as e:
            logger.warning(f"Could not capture screenshot for {safe_name}: {e}")

    page.close()


# ── Test data fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def test_data():
    data_path = Path(__file__).parent / "data" / "test_data.json"
    with open(data_path) as f:
        return json.load(f)