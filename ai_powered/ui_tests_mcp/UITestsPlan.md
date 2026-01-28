# UI Test Plan - Conduit (MCP)

## Overview

This test plan covers the key functional areas of the Conduit application (http://localhost:4200/#/). The tests focus on
core user journeys including navigation, authentication, and article interaction.

## Test Cases

### 1. Home Page Loading and Navigation

- **Title**: Verify Home Page and Basic Navigation
- **Intent**: Ensure the home page loads correctly and navigation links are functional.
- **Preconditions**: None
- **Steps**:
    1. Navigate to `http://localhost:4200/#/`.
    2. Verify the page title is "Conduit".
    3. Verify the "Home", "Sign in", and "Sign up" links are visible in the navigation bar.
- **Assertions**:
    - Page title is "Conduit".
    - Navigation bar contains expected links.

### 2. User Registration (UI Flow)

- **Title**: Verify User Registration Page Elements
- **Intent**: Ensure the registration form is accessible and has correct fields.
- **Preconditions**: None
- **Steps**:
    1. Navigate to the home page.
    2. Click on the "Sign up" link.
    3. Verify the "Sign up" heading is visible.
    4. Verify Username, Email, and Password fields are present.
- **Assertions**:
    - URL contains `#/register`.
    - Heading "Sign up" is present.
    - Input fields for Username, Email, and Password are visible.

### 3. User Login (UI Flow)

- **Title**: Verify User Login Page Elements
- **Intent**: Ensure the login form is accessible and has correct fields.
- **Preconditions**: None
- **Steps**:
    1. Navigate to the home page.
    2. Click on the "Sign in" link.
    3. Verify the "Sign in" heading is visible.
    4. Verify Email and Password fields are present.
- **Assertions**:
    - URL contains `#/login`.
    - Heading "Sign in" is present.
    - Input fields for Email and Password are visible.

### 4. Global Feed and Article List

- **Title**: Verify Global Feed Loading
- **Intent**: Ensure articles are displayed in the Global Feed.
- **Preconditions**: None
- **Steps**:
    1. Navigate to the home page.
    2. Wait for articles to load.
    3. Verify that at least one article is displayed in the feed.
- **Assertions**:
    - Global Feed is active.
    - Article list contains at least one article preview.

### 5. Filter by Tag

- **Title**: Verify Filtering Articles by Tag
- **Intent**: Ensure that clicking a tag in the "Popular Tags" section filters the feed.
- **Preconditions**: None
- **Steps**:
    1. Navigate to the home page.
    2. Click on a tag in the "Popular Tags" sidebar (e.g., "django").
    3. Verify that a new tab for the tag appears in the feed.
- **Assertions**:
    - The selected tag appears as an active feed tab.
    - Articles are filtered (implied by the new tab).

### 6. Unauthorized Like Redirect

- **Title**: Redirect to Sign In on Unauthorized Like
- **Intent**: Verify that a non-logged-in user is redirected to the login page when trying to like an article.
- **Preconditions**: User is not logged in.
- **Steps**:
    1. Navigate to the home page.
    2. Click the "Like" button (heart icon) on any article.
    3. Verify redirection to the "Sign in" page.
- **Assertions**:
    - URL contains `#/login`.
    - "Sign in" heading is visible.

## Technical Details

- **Locators**: Use `get_by_role`, `get_by_label`, `get_by_placeholder`.
- **Hooks**: Screenshots on failure.
- **Folder**: `./ai_powered/ui_tests_mcp`
