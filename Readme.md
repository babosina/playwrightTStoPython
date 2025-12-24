Based on: https://github.com/babosina/playwrightTS

1. Install pytest-playwright
2. Install browsers: `playwright install`
3. For UV-based project configuration is put to the project.toml file
   Example:
   [tool.pytest.ini_options]
   base_url = "https://example.com"
   addopts = [
   "--headed",
   "--browser", "chromium",
   "--browser", "firefox",
   "--browser", "webkit",
   "--slowmo", "100",
   "--tracing", "on",
   "-n", "4"
   ]
   testpaths = ["tests"]
   python_files = ["test_*.py"]
4. For the common pytest.ini option:
   [pytest]

# Base URL for tests

base_url = https://example.com

# Number of parallel workers

addopts =
--headed
--browser chromium
--browser firefox
--browser webkit
--slowmo 100
--tracing on
-n 4

# Test discovery patterns

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

5. Advanced conftest.py file
   import pytest
   from playwright.sync_api import Browser, BrowserContext

# Configure base URL

@pytest.fixture(scope="session")
def base_url():
return "https://example.com"

# Browser context configuration (similar to TS projects)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
return {
**browser_context_args,
"viewport": {"width": 1920, "height": 1080},
"ignore_https_errors": True,
"user_agent": "Custom User Agent",
}

# Configure different browser projects

@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser_name(request):
return request.param

# Storage state for authenticated tests

@pytest.fixture(scope="session")
def context_with_auth(browser: Browser):
context = browser.new_context(storage_state="auth.json")
yield context
context.close()

6. Common Playwright pytest options:
   --headed / --headless: Run in headed/headless mode
   --browser chromium|firefox|webkit: Specify browser(s)
   --slowmo <ms>: Slow down operations
   --tracing on|off|retain-on-failure: Enable tracing
   --video on|off|retain-on-failure: Record videos
   --screenshot on|off|only-on-failure: Take screenshots
   -n <workers>: Number of parallel workers (requires pytest-xdist)

7. Report
   uv pip install pytest-html
   and add to toml
   "--html=report.html", "--self-contained-html"

8. Allure report
   allure generate allure-results -o allure-report --clean
