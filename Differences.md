# 📊 Key Differences: Playwright TypeScript vs Python

## 🛠 Language Syntax

### ⏳ Async/Await
- **TypeScript**: Uses `async/await` keywords
- **Python**: Uses `async/await` keywords (similar syntax)

### 🏷 Type Annotations
- **TypeScript**: Built-in type system with interfaces and types
- **Python**: Optional type hints using `typing` module

### ⌨️ Semicolons
- **TypeScript**: Semicolons optional but common
- **Python**: No semicolons needed

## 🎭 Playwright API Differences

### 📥 Importing
```typescript
// TypeScript
import { test, expect } from '@playwright/test';
```
```python
# Python
from playwright.sync_api import sync_playwright
# or
from playwright.async_api import async_playwright
import pytest
```

### 🌐 Browser Context
```typescript
// TypeScript - automatic with fixtures
test('example', async ({ page }) => {
  // page is provided
});
```
```python
# Python - manual setup or pytest fixtures
def test_example(page):
    # using pytest-playwright plugin
    pass
```

### 📝 Method Naming Convention
- **TypeScript**: camelCase (`goto`, `waitForSelector`, `innerHTML`)
- **Python**: snake_case (`goto`, `wait_for_selector`, `inner_html`)

### 🎯 Selectors
```typescript
// TypeScript
await page.locator('button').click();
await page.getByRole('button', { name: 'Submit' }).click();
```
```python
# Python
page.locator('button').click()
page.get_by_role('button', name='Submit').click()
```

### 🔍 Assertions
```typescript
// TypeScript
await expect(page).toHaveTitle(/Playwright/);
await expect(locator).toBeVisible();
```
```python
# Python
expect(page).to_have_title(re.compile("Playwright"))
expect(locator).to_be_visible()
```

## ⚙️ Configuration

### 📄 Config File
- **TypeScript**: `playwright.config.ts` (often uses `defineConfig`)
- **Python**: `pyproject.toml` (with `[tool.pytest.ini_options]`), `pytest.ini`, or `conftest.py`

### 📂 Test File Pattern
- **TypeScript**: `*.spec.ts` or `*.test.ts`
- **Python**: `test_*.py` or `*_test.py`

## 🏗 Project Structure and Naming

### 📁 Directory and File Naming
- **TypeScript**: camelCase is common for folders and files (e.g., `requestObjects`, `responseSchemas`, `smoke.spec.ts`)
- **Python**: snake_case is the standard for folders and files (e.g., `request_data`, `response_schemas`, `test_smoke.py`)

### 🗺 Folder Mapping
| Feature | Playwright TS Folder | Playwright Python Folder |
| --- | --- | --- |
| Test Files | `tests/` | `tests/` |
| Request Data | `requestObjects/` | `request_data/` |
| Response Schemas | `responseSchemas/` | `response_schemas/` |
| Utilities | `utils/` | `utils/` |
| Fixtures/Hooks | `utils/fixtures.ts` | `conftest.py` |

## 🧪 Test Implementation Patterns

### 🔗 API Testing Wrappers
Both repositories often use a custom wrapper (e.g., `RequestHandler`) to simplify API interactions.

### 🧩 Custom Assertions
Both versions implement custom matchers for schema validation:
- **TypeScript**: `await expect(response).shouldMatchSchema('folder', 'schema')`
- **Python**: `expect(response).should_match_schema("folder", "schema")`

## 🏗 Test Structure

### 📝 Test Definition
```typescript
// TypeScript
test.describe('Group', () => {
  test('test name', async ({ page }) => {
    // test code
  });
});
```
```python
# Python
class TestGroup:
    def test_name(self, page):
        # test code
        pass
```

### ⚓ Hooks/Fixtures
```typescript
// TypeScript
test.beforeEach(async ({ page }) => {
  await page.goto('/');
});
```
```python
# Python
@pytest.fixture(autouse=True)
def before_each(page):
    page.goto('/')
```

## ⚡ Synchronous vs Asynchronous

### 🟦 TypeScript
- Always async with Playwright
- Must use `await` for all Playwright operations

### 🟨 Python
- Two APIs: `sync_api` and `async_api`
- `sync_api`: No await needed (simpler for most cases)
- `async_api`: Similar to TypeScript, requires await

## 🚀 Running Tests

### 🟦 TypeScript
```bash
npx playwright test
npx playwright test --headed
npx playwright show-report
```

### 🟨 Python
```bash
pytest
pytest --headed
pytest --html=report.html
```

## 📦 Package Management

- **TypeScript**: npm/yarn/pnpm with `package.json`
- **Python**: pip/poetry/uv with `requirements.txt` or `pyproject.toml`

## ⏱ Auto-waiting

Both versions have auto-waiting built into locators and assertions, but:
- TypeScript: All operations are promises
- Python sync_api: Blocking operations
- Python async_api: Same as TypeScript

### 📝 Summary of Scope Mapping:

| Playwright TS | Playwright Python (Pytest) |
| --- | --- |
| `scope: 'worker'` | `scope="session"` |
| `scope: 'test'` | `scope="function"` (default) |
| `extraHTTPHeaders` | `extra_http_headers` |