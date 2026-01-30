# Playwright Python API & UI Testing Framework

This project is a comprehensive testing framework for the "Conduit" RealWorld application, featuring both API and UI test suites. It was migrated from a TypeScript-based Playwright framework to Python ([repository](https://github.com/babosina/playwrightTS)).

The application under test is a Django + Angular implementation of the RealWorld spec: [realworld-django-rest-framework-angular](https://github.com/babosina/realworld-django-rest-framework-angular).

## 🚀 Key Elements

- **RequestHandler**: A fluent API wrapper around Playwright's `APIRequestContext` for building and sending requests with automatic logging.
- **Custom Expect**: An `Expect` class providing chainable, readable assertions (e.g., `expect(response).to_have_status_code(200)`).
- **Schema Validation**: Automated validation of API responses against JSON schemas located in `response_schemas/`.
- **UI Testing**: Comprehensive UI test suites using Playwright's Page Object model and functional testing patterns.
- **AI-Powered Testing**: Experimental test suites (in `ai_powered/`) demonstrating AI-assisted test generation and execution.
- **Article Generator**: Utility for generating dynamic test data for articles.
- **APILogger**: Centralized logging for all API interactions.

## 📋 Prerequisites

- **Python 3.13+**
- **uv** (recommended) or **pip**
- **Docker** (for running the application locally)

## 🛠️ Project Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd playwrightTStoPython
   ```

2. **Install dependencies**
   Using `uv` (recommended):
   ```bash
   uv sync
   ```
   Using `pip`:
   ```bash
   pip install -e .
   ```

3. **Install Playwright Browsers**
   ```bash
   playwright install
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   EMAIL=your-email@example.com
   PASSWORD=your-password
   ```

## 🖥️ Running the Application

To run the application locally using Docker (requires the app repository to be forked and cloned separately):

```bash
# Fork the application repository on GitHub:
# https://github.com/babosina/realworld-django-rest-framework-angular

# Clone your forked repository
git clone https://github.com/<your-username>/realworld-django-rest-framework-angular
cd realworld-django-rest-framework-angular

# Start the application using Docker Compose
docker-compose up -d

# Seed the database (if needed)
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py seed_db
```
The application Backend will be available at `http://localhost:8000`.

The application Frontend will be available at `http://localhost:4200`.

## 🧪 Running Tests

### API Tests
**Run all API tests:**
```bash
pytest tests/
```

**Run specific test file:**
```bash
pytest tests/test_smoke.py
```

### UI Tests
**Run UI tests:**
```bash
pytest ai_powered/ui_tests/
```

### General Pytest Commands
- **Parallel execution:** `pytest -n 4`
- **Headed mode:** `pytest --headed`
- **Generate HTML Report:** `pytest --html=report.html --self-contained-html`

## 📂 Project Structure

```
├── ai_powered/           # AI-assisted and UI test suites
│   ├── tests/            # AI-generated API tests
│   ├── ui_tests/         # UI test suite
│   └── ui_tests_mcp/     # UI tests using MCP
├── tests/                # Standard API test suites
├── utils/                # Core utilities (RequestHandler, Expect, etc.)
├── response_schemas/     # JSON schemas for API validation
├── request_data/         # Static/dynamic request payloads
├── conftest.py           # Global Pytest fixtures
├── pyproject.toml        # Project configuration & dependencies
└── .env                  # Environment variables (ignored by git)
```

## 📊 Reports

- **HTML Report**: Generated automatically in `report.html` (as configured in `pyproject.toml`).
- **Allure Report** (to be updated):
  ```bash
  # Generate and open report
  allure generate allure-results -o allure-report --clean
  allure open allure-report
  ```

## 💡 Notes & Best Practices

- **Test Data**: Prefer using `ArticleGenerator` or Python modules in `request_data/` instead of hardcoded strings.
- **Assertions**: Use the custom `Expect` class for API tests to maintain consistency with Playwright's UI assertion style.
- **Parallelism**: Use `pytest-xdist` (`-n` flag) for faster execution of independent tests.
- **Migration**: See `Differences.md` for details on the TypeScript to Python migration.