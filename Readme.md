# Playwright Python API Testing Framework

API testing framework migrated from TypeScript to Python. Based on: https://github.com/babosina/playwrightTS

## Prerequisites

- Python 3.13+
- uv (recommended) or pip

## Project Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd playwrightTStoPython
   ```

2. **Install dependencies**
   ```bash
   uv pip install -e .
   ```
   Or with pip:
   ```bash
   pip install -e .
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:
   ```
   EMAIL=your-email@example.com
   PASSWORD=your-password
   ```

4. **Update base URL (if needed)**

   The project is configured for `localhost:8000`. To change it, update `conftest.py:17`:
   ```python
   base_url = "http://localhost:8000/api/"
   ```

## Running Tests

**Run all tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest tests/test_smoke.py
```

**Run with parallel execution:**
```bash
pytest -n 4
```

## Project Structure

```
├── tests/              # Test suites
│   ├── test_smoke.py
│   ├── test_crud_operations.py
│   └── test_example.py
├── utils/              # Utilities and helpers
│   ├── apilogger.py           # Request/response logging
│   ├── custom_expect.py       # Custom assertions (Expect class)
│   ├── request_handler.py     # API request wrapper
├── conftest.py         # Pytest fixtures (api_request, get_token)
├── pyproject.toml      # Project configuration
└── .env               # Environment variables (not in git)
```

## Key Features

- **Custom Request Handler**: Fluent API for building requests (`RequestHandler` class)
- **Custom Assertions**: `Expect` class with chainable assertions
- **Request/Response Logging**: Automatic logging with custom status code validation
- **Token Authentication**: Reusable `get_token` fixture
- **HTML Reports**: Generated in `report.html`
- **Allure Reports**: Results stored in `allure-results/`

## Generating Reports

**HTML Report:**
Generated automatically after test run in `report.html`

**Allure Report:**
```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Configuration

Test configuration is in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
base_url = ""
addopts = [
    "--html=report.html", "--self-contained-html",
    "--alluredir=allure-results",
    "--tracing=retain-on-failure",
    "--video=retain-on-failure",
    "--screenshot=only-on-failure"
]
```

## Notes

- This project focuses on **API testing only** (no browser UI testing)
- Custom `Expect` class provides JavaScript-like assertion syntax
- See `Differences.md` for details on TS to Python migration differences

## Parallel execution (workers concept)
- Run with: `pytest -n 4` (4 parallel workers)

## Test Data Management (avoiding hardcoded payloads)
To keep tests clean and maintainable, store request/response payloads outside the test functions and import/load them when needed.
### Recommended approach (most “pythonic” for tests): Python modules
Place test payloads in a dedicated Python file (e.g., ) and import constants in tests. `request_data/POST_article.py`
**Pros**
- No file I/O or parsing
- Easy refactoring and reuse across tests
- Payloads can be composed/extended in Python

### Alternative: JSON files (closest to JS workflow)
Store payloads as and load them in tests via + . `.json``json``pathlib`
**Pros**
- Tool/language-agnostic
- Easy to share with non-Python tooling

### Built-in config-style option: TOML
Python 3.11+ includes , so TOML can be used without extra dependencies. `tomllib`
**Pros**
- Very human-editable
- No third-party packages required

### Tip: avoid shared mutable payloads
If a test modifies a payload, create a copy (e.g., deep copy) to prevent leaking changes into other tests.