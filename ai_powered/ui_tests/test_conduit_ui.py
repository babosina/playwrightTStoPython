import pytest
import os
from playwright.sync_api import Page, expect


def test_home_page_loading(page: Page):
    """
    Test Case 1: Home Page Loading and Navigation
    """
    expect(page).to_have_title("Conduit")

    # Check navbar links
    navbar = page.get_by_role("navigation")
    expect(navbar.get_by_role("link", name="conduit")).to_be_visible()
    expect(navbar.get_by_role("link", name="Home")).to_be_visible()
    expect(navbar.get_by_role("link", name="Sign in")).to_be_visible()
    expect(navbar.get_by_role("link", name="Sign up")).to_be_visible()

    # Check Global Feed
    expect(page.get_by_text("Global Feed")).to_be_visible()


def test_user_registration(page: Page, random_user):
    """
    Test Case 2: User Registration (Sign Up)
    """
    page.get_by_role("link", name="Sign up").click()

    page.get_by_placeholder("Username").fill(random_user["username"])
    page.get_by_placeholder("Email").fill(random_user["email"])
    page.get_by_placeholder("Password").fill(random_user["password"])

    page.get_by_role("button", name="Sign up").click()

    # Verification: Navbar should show username
    # Check if there are error messages
    error_messages = page.locator(".error-messages").first
    # Wait a bit for potential error messages to appear if registration fails
    page.wait_for_timeout(2000)
    if error_messages.is_visible():
        msg = error_messages.inner_text()
        print(f"Registration failed with: {msg}")
        pytest.fail(f"Registration failed: {msg}")

    # Using a longer timeout as registration might take a moment
    expect(page.get_by_role("navigation")).to_contain_text(random_user["username"], timeout=15000)
    expect(page.get_by_role("link", name="Sign up")).not_to_be_visible()


def test_user_login(page: Page):
    """
    Test Case 3: User Login (Sign In)
    """
    email = os.getenv("EMAIL", "testuser@example.com")
    password = os.getenv("PASSWORD", "Password123!")

    page.get_by_role("link", name="Sign in").click()

    page.get_by_placeholder("Email").fill(email)
    page.get_by_placeholder("Password").fill(password)

    page.get_by_role("button", name="Sign in").click()

    # Verification: Navbar should show username or at least not show Sign in
    expect(page.get_by_role("link", name="Sign in")).not_to_be_visible()
    # If we knew the username for the email, we could check for it. 
    # Usually it's 'bob' or 'john' in these demo apps.


def test_redirect_to_login_on_like_unauthorized(page: Page):
    """
    Test Case 4: Redirect to Sign In when Liking an Article (Unauthorized)
    """
    # Find any like button (usually has a heart icon and counter)
    # Based on exploration, it might be a button with a number
    like_button = page.get_by_role("button").filter(has_text=re.compile(r"^\d+$")).first
    # Wait, let me check the exact role/text if possible. 
    # In Conduit it's often a button inside .article-preview

    # Let's try to find a button with a heart icon or just the first button that looks like a like button
    # Actually, let's use a more generic locator if we are not sure
    first_article_like_btn = page.locator(".article-preview button").first
    first_article_like_btn.click()

    # Assert redirect to login
    expect(page).to_have_url(re.compile(r".*/login.*"))


import re


def test_view_article_detail(page: Page):
    """
    Test Case 5: View Article Detail
    """
    # Click on the first article title
    first_article_title = page.locator(".article-preview h1").first
    title_text = first_article_title.inner_text()
    first_article_title.click()

    # Assertions
    expect(page).to_have_url(re.compile(r".*/article/.*"))
    expect(page.get_by_role("heading", level=1)).to_contain_text(title_text)


def test_filter_by_tag(page: Page):
    """
    Test Case 6: Filter by Tag
    """
    # Wait for tags to load - they might be in a different container or just links
    # Let's look for tags by text if .tag-list fails
    first_tag = page.locator(".sidebar .tag-pill").first

    # Ensure tags are loaded
    expect(first_tag).to_be_visible(timeout=15000)

    tag_name = first_tag.inner_text().strip()
    first_tag.click()

    # Assert that the active tab in feed is the tag
    active_tab = page.locator(".feed-toggle .nav-link.active")
    expect(active_tab).to_contain_text(tag_name)
