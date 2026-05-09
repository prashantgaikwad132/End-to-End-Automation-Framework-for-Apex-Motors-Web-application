"""
Centralized environment configuration loaded from .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://driveway-dashboard-buddy.lovable.app")
    VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER: str = os.getenv("BROWSER", "chromium")
