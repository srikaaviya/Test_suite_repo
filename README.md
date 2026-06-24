# restful-booker-test-suite

Production-grade test framework for the [Restful Booker API](https://restful-booker.herokuapp.com) — a hotel booking system. Zero application code. 100% testing.

## Test Layers

| Layer | Tool | Tests | What it covers |
|-------|------|-------|----------------|
| API Functional | Pytest + Requests | 40 | CRUD operations, auth flows, filters, edge cases |
| Contract (manual) | Pytest + Pydantic | 6 | Response schema validation, field types, data integrity |
| Contract (fuzz) | Schemathesis | 8 | Auto-generated tests from OpenAPI spec |
| Security | Pytest | 8 | SQL injection, XSS, IDOR, header injection, auth bypass |
| E2E UI | Playwright | 10 | Homepage, admin login/logout, room management, contact form |
| Load | Locust | 3 profiles | Baseline (10 users), Stress (100 users), Spike (10→100) |

**Total: 72 automated tests + 3 load test profiles**

## Architecture

```
restful-booker-test-suite/
├── src/                        # Core utilities
│   ├── config.py               # URLs, credentials, timeouts
│   ├── models.py               # Pydantic models + test data factory
│   ├── auth.py                 # Token authentication helper
│   └── api_client.py           # HTTP client wrapper
├── tests/
│   ├── api/                    # API functional tests (40 tests)
│   │   ├── test_auth.py        # Authentication endpoint tests
│   │   ├── test_booking_crud.py # Create, Read, Update, Delete
│   │   ├── test_booking_filters.py # Search and filter tests
│   │   ├── test_edge_cases.py  # Invalid input, missing auth, boundary values
│   │   └── test_healthy.py     # Health check
│   ├── contract/               # Contract tests (14 tests)
│   │   ├── test_schema.py      # Manual schema validation (6 tests)
│   │   ├── test_schemathesis.py # Auto-generated fuzz tests (8 tests)
│   │   └── openapi.yaml        # Hand-written OpenAPI 3.0 spec
│   ├── security/               # Security smoke tests (8 tests)
│   ├── e2e/                    # Playwright UI tests (10 tests)
│   └── load/                   # Locust load test profiles
├── .github/workflows/
│   ├── ci.yml                  # Push: API + Contract + Security + E2E
│   └── nightly.yml             # Scheduled: Load tests (3 profiles)
└── reports/                    # Generated test reports
```

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd restful-booker-test-suite
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[all]"
playwright install chromium

# Run all tests
pytest tests/ -v

# Run by layer
pytest tests/api/ -v              # API functional tests
pytest tests/security/ -v         # Security smoke tests
pytest tests/contract/ -v         # Contract tests
pytest tests/e2e/ -v              # E2E UI tests (requires Playwright)

# Run by marker
pytest -m smoke -v                # Quick smoke test (critical path only)
pytest -m "api or security" -v    # Multiple layers

# Run with Allure report
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results

# Load tests
locust -f tests/load/locustfile.py --headless -u 10 -r 1 -t 60s --html reports/load_report.html
```

## Load Test Results

Baseline profile (10 concurrent users, 60 seconds):

| Metric | Value |
|--------|-------|
| Total Requests | 86 |
| Failure Rate | 0% |
| Avg Response Time | 120ms |
| p50 (Median) | 74ms |
| p95 | 290ms |
| p99 | 310ms |

## Bugs Found

| # | Bug | Severity | Found by | Details |
|---|-----|----------|----------|---------|
| 1 | Health check returns 201 instead of 200 | Low | Manual | `GET /ping` returns 201 (Created) for a read-only health check |
| 2 | API accepts negative prices | Medium | Manual | `totalprice: -100` is accepted without validation |
| 3 | API accepts empty/missing required fields | Medium | Manual | `POST /booking` with `{}` returns 500 instead of 400 |
| 4 | API accepts checkout before checkin | Medium | Manual | Checkout date before checkin date is not validated |
| 5 | No input length validation | Low | Manual | 100,000 character names accepted without limit |
| 6 | XSS payloads stored without sanitization | High | Manual | `<script>` tags stored as-is in name fields |
| 7 | TRACE method returns 404 instead of 405 | Low | Schemathesis | Unsupported HTTP methods not properly rejected |
| 8 | Empty date string stores as `"0NaN-aN-aN"` | Medium | Schemathesis | Empty checkout date parsed into invalid NaN string |
| 9 | `totalprice` accepts objects, stores null | Medium | Schemathesis | Sending `{}` for totalprice saves `null` instead of rejecting |
| 10 | `additionalneeds` accepts non-string types | Low | Schemathesis | Objects accepted where only strings should be allowed |
| 11 | Empty query params cause 500 | Medium | Schemathesis | `GET /booking?checkout=` crashes the server |

## CI Pipeline

**On every push/PR:**
- API functional tests → Contract tests → Security tests → E2E tests
- Allure report generated and published to GitHub Pages

**Nightly schedule:**
- Load tests run all 3 profiles (baseline, stress, spike)
- HTML reports uploaded as artifacts

## Tech Stack

| Tool | Purpose |
|------|---------|
| Pytest | Test runner and framework |
| Requests | HTTP client for API tests |
| Pydantic | Data validation and test models |
| Schemathesis | OpenAPI-based fuzz testing |
| Playwright | Browser automation for E2E tests |
| Locust | Load and performance testing |
| Allure | Test reporting and dashboards |
| GitHub Actions | CI/CD pipeline |
