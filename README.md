# 🏎️ Apex Motors — Senior E2E Automation Framework

Production-grade Playwright + Pytest automation ecosystem for the [Apex Motors](https://driveway-dashboard-buddy.lovable.app) premium automotive web application.

---

## 📐 Architecture

```
apex-motors-automation/
├── conftest.py                  # Session & per-test fixtures, Allure hooks
├── pytest.ini                   # Pytest configuration & markers
├── requirements.txt             # Python dependencies
├── .env                         # Environment config (BASE_URL, viewport, timeout)
├── Jenkinsfile                  # Declarative CI/CD pipeline
├── .github/workflows/ci.yml    # GitHub Actions alternative pipeline
│
├── pages/                       # Page Object Model (POM)
│   ├── base_page.py             #   └─ Abstract base with reusable helpers
│   ├── home_page.py             #   └─ Home / landing page
│   ├── inventory_page.py        #   └─ Inventory listing + filters
│   ├── vehicle_modal_page.py    #   └─ Vehicle detail modal overlay
│   ├── contact_page.py          #   └─ Contact form
│   ├── about_page.py            #   └─ About page
│   └── header_nav.py            #   └─ Shared header navigation
│
├── tests/                       # Test suites (30+ test cases)
│   ├── test_home_page.py        #   └─ 9 tests — hero, filters, stats, branding
│   ├── test_inventory.py        #   └─ 9 tests — search, categories, modal, data integrity
│   ├── test_contact.py          #   └─ 5 tests — form submission, validation, negative
│   ├── test_navigation.py       #   └─ 3 tests — routing, SEO titles, logo nav
│   └── test_responsive.py       #   └─ 4 tests — mobile, tablet, multi-viewport
│
├── utils/                       # Utility layer
│   ├── config.py                #   └─ Env-based configuration class
│   ├── logger.py                #   └─ Custom file + console logger
│   └── data_provider.py         #   └─ DDT loaders (JSON & Excel)
│
└── data/
    └── test_data.json           # Centralized test data (vehicles, forms, viewports)
```

## 🎯 Design Patterns

| Pattern | Implementation |
|---------|---------------|
| **Page Object Model** | Every page/component has a dedicated class in `pages/` |
| **Base Page Abstraction** | `BasePage` wraps Playwright's `Page` with logged, Allure-stepped helpers |
| **Data-Driven Testing** | `data_provider.py` loads JSON/Excel; `@pytest.mark.parametrize` drives tests |
| **Fixture Management** | Session-scoped browser, per-test page isolation, auto-teardown |
| **Allure Integration** | `@allure.step`, `@allure.story`, auto-screenshot on failure, video attachment |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### Setup

```bash
git clone <your-repo-url>
cd apex-motors-automation

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install browser engines
playwright install --with-deps chromium
```

### Run Tests

```bash
# Full suite
pytest

# Smoke tests only
pytest -m smoke

# Specific feature
pytest -m inventory
pytest -m contact

# Headed mode (watch browser)
pytest --headed

# Different browser
pytest --browser-name=firefox

# With slow motion for debugging
pytest --headed --slow-mo=500

# Generate Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Custom Base URL

```bash
pytest --base-url=http://localhost:5173
```

Or edit `.env`:
```
BASE_URL=http://localhost:5173
```

## 🧪 Test Coverage (30+ Scenarios)

| ID | Area | Scenario | Marker |
|----|------|----------|--------|
| TC-001 | Home | Hero section renders with CTAs | `smoke` |
| TC-002 | Home | Explore Collection → /inventory | `smoke` |
| TC-003 | Home | Book Test Drive → /contact | `smoke` |
| TC-004 | Home | All 6 vehicles displayed by default | `inventory` |
| TC-005 | Home | SUV filter isolates correct vehicles | `inventory` |
| TC-006 | Home | Sports filter shows 2 vehicles | `inventory` |
| TC-007 | Home | Reset to 'All' restores full grid | `inventory` |
| TC-008 | Home | Stats KPIs visible | `smoke` |
| TC-009 | Home | APEX logo renders | `smoke` |
| TC-010 | Inventory | Search filters by name/brand (3 params) | `inventory` |
| TC-011 | Inventory | No results message for empty search | `inventory` |
| TC-012 | Inventory | Category filter counts (6 params) | `inventory` |
| TC-013 | Inventory | Modal opens with correct specs | `inventory` |
| TC-014 | Inventory | Modal close button works | `inventory` |
| TC-015 | Inventory | Inquire Now → /contact | `inventory` |
| TC-016 | Inventory | Book Test Drive → /contact | `inventory` |
| TC-017 | Inventory | HP value matches expected data | `regression` |
| TC-018 | Inventory | Search + category combo filter | `regression` |
| TC-019 | Contact | Valid form submission → success | `contact, smoke` |
| TC-020 | Contact | Send Another resets form | `contact` |
| TC-021 | Contact | Empty form blocked by validation | `contact, negative` |
| TC-022 | Contact | Contact info section visible | `contact` |
| TC-023 | Contact | All interest options selectable (4 params) | `contact` |
| TC-024 | Navigation | Nav links route correctly (3 params) | `navigation` |
| TC-025 | Navigation | Logo click returns home | `navigation` |
| TC-026 | Navigation | Page titles for SEO (4 params) | `smoke` |
| TC-027 | Responsive | Mobile hamburger menu | `responsive` |
| TC-028 | Responsive | Tablet inventory grid | `responsive` |
| TC-029 | Responsive | Hero across viewports (3 params) | `responsive` |
| TC-030 | Responsive | Mobile contact form E2E | `responsive` |

## 🔧 CI/CD

### Jenkins
The `Jenkinsfile` provides a 3-stage pipeline:
1. **Setup** — virtualenv, pip install, browser install
2. **Execute** — parameterized test run (browser, headed, markers)
3. **Report** — Allure report generation and artifact archival

### GitHub Actions
`.github/workflows/ci.yml` provides the same pipeline for GitHub-hosted runners with artifact upload.

## 📊 Allure Reporting

```bash
# After test run
allure serve reports/allure-results

# Or generate static report
allure generate reports/allure-results -o reports/allure-report --clean
```

Features:
- Step-by-step execution traces via `@allure.step`
- Automatic failure screenshots attached to failed tests
- Video recordings for full test replay
- Organized by Epic → Feature → Story hierarchy

## 🛠️ Extending the Framework

### Add a new page object
1. Create `pages/new_page.py` extending `BasePage`
2. Define selectors and Allure-stepped methods
3. Import in your test file

### Add test data
Edit `data/test_data.json` or create an Excel file and use `data_provider.load_excel()`.

### Add a new test
Create `tests/test_feature.py`, register markers in `pytest.ini`.

---

**Author:** Prashant Gaikwad | Senior Automation Engineer | Python · Playwright · Pytest · Jenkins · Allure  
**Target App:** [Apex Motors](https://driveway-dashboard-buddy.lovable.app)
