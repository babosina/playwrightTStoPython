import pytest
import re
from playwright.sync_api import Page, expect


def test_home_page_loading(page: Page):
    """Verify Home Page and Basic Navigation"""
    expect(page).to_have_title("Conduit")

    # Verify navigation links
    expect(page.get_by_role("link", name="Home")).to_be_visible()
    expect(page.get_by_role("link", name="Sign in")).to_be_visible()
    expect(page.get_by_role("link", name="Sign up")).to_be_visible()


def test_user_registration_page_elements(page: Page):
    """Verify User Registration Page Elements"""
    page.get_by_role("link", name="Sign up").click()

    expect(page).to_have_url(re.compile(r".*#/register"))
    expect(page.get_by_role("heading", name="Sign up")).to_be_visible()

    # Verify input fields
    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Email")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Sign up")).to_be_visible()


def test_user_login_page_elements(page: Page):
    """Verify User Login Page Elements"""
    page.get_by_role("link", name="Sign in").click()

    expect(page).to_have_url(re.compile(r".*#/login"))
    expect(page.get_by_role("heading", name="Sign in")).to_be_visible()

    # Verify input fields
    expect(page.get_by_placeholder("Email")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Sign in")).to_be_visible()


def test_global_feed_loading(page: Page):
    """Verify Global Feed Loading"""
    # In some Conduit versions, Global Feed might be a link or a plain element
    # Based on snapshot, 'Global Feed' was a generic element ref=e89
    # Let's use a more flexible locator
    global_feed_tab = page.get_by_text("Global Feed")
    expect(global_feed_tab).to_be_visible()

    # Check if at least one article title is visible
    articles = page.locator(".article-preview")
    # Wait for articles to appear
    page.wait_for_selector(".article-preview", timeout=10000)
    expect(articles.first).to_be_visible()


def test_filter_by_tag(page: Page):
    """Verify Filtering Articles by Tag"""
    # Wait for tags to load
    page.wait_for_selector(".tag-list", timeout=10000)

    # Get a tag (e.g., 'django') from the Popular Tags sidebar
    tag_name = "django"
    tag_link = page.locator(".sidebar").get_by_text(tag_name)
    expect(tag_link).to_be_visible()

    tag_link.click()

    # Verify a new tab with the tag name appears
    # Using get_by_text since role might vary
    tag_tab = page.locator(".feed-toggle").get_by_text(tag_name)
    expect(tag_tab).to_be_visible()


def test_redirect_to_login_on_like_unauthorized(page: Page):
    """Redirect to Sign In on Unauthorized Like"""
    # Wait for articles to load
    page.wait_for_selector(".article-preview", timeout=10000)

    # Find the first 'Like' button
    # It has a heart icon and count. It's usually the only button in the preview header
    like_button = page.locator(".article-preview").first.locator("button")

    like_button.click()

    # Verify redirection to the login page
    expect(page).to_have_url(re.compile(r".*#/login"))
    expect(page.get_by_role("heading", name="Sign in")).to_be_visible()
