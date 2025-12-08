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

5. Common Playwright pytest options:
--headed / --headless: Run in headed/headless mode
--browser chromium|firefox|webkit: Specify browser(s)
--slowmo <ms>: Slow down operations
--tracing on|off|retain-on-failure: Enable tracing
--video on|off|retain-on-failure: Record videos
--screenshot on|off|only-on-failure: Take screenshots
-n <workers>: Number of parallel workers (requires pytest-xdist)

6.
