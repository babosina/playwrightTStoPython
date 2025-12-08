from playwright.sync_api import Page, expect
import re


def test_example(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
