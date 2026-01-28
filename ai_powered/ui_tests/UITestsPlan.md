# UI Test Plan - Conduit Application

## Introduction

This test plan covers the basic functional testing of the Conduit application (Angular frontend) located at
`http://localhost:4200/#/`.

## Test Environment

- **URL:** http://localhost:4200/#/
- **Framework:** Pytest with Playwright
- **Locators:** Role-based, labels, and placeholders for robustness.

## Test Cases

### 1. Home Page Loading and Navigation

**Intent:** Verify that the home page loads correctly and navigation links are present.

- **Preconditions:** None.
- **Steps:**
    1. Navigate to `http://localhost:4200/#/`.
    2. Wait for the page to load.
- **Assertions:**
    - Page title is "Conduit".
    - Navbar contains "conduit", "Home", "Sign in", and "Sign up".
    - "Global Feed" is visible.

### 2. User Registration (Sign Up)

**Intent:** Verify that a new user can register successfully.

- **Preconditions:** Use a unique username and email.
- **Steps:**
    1. Navigate to the Home page.
    2. Click on "Sign up" in the navbar.
    3. Enter a unique username, email, and password.
    4. Click the "Sign up" button.
- **Assertions:**
    - User is redirected to the Home page or logged-in state.
    - Navbar shows the username instead of "Sign in" and "Sign up".

### 3. User Login (Sign In)

**Intent:** Verify that an existing user can log in.

- **Preconditions:** A registered user exists (e.g., from environment variables).
- **Steps:**
    1. Navigate to the Home page.
    2. Click on "Sign in" in the navbar.
    3. Enter valid email and password.
    4. Click the "Sign in" button.
- **Assertions:**
    - User is redirected to the Home page.
    - Navbar shows the username.

### 4. Redirect to Sign In when Liking an Article (Unauthorized)

**Intent:** Verify that an unauthenticated user is redirected to the Sign In page when trying to like an article.

- **Preconditions:** User is not logged in.
- **Steps:**
    1. Navigate to the Home page.
    2. Locate any article in the feed.
    3. Click on the "Like" button (heart icon/counter).
- **Assertions:**
    - Page redirects to `#/login`.

### 5. View Article Detail

**Intent:** Verify that clicking on an article opens its detail page.

- **Preconditions:** Articles exist in the feed.
- **Steps:**
    1. Navigate to the Home page.
    2. Click on an article title.
- **Assertions:**
    - URL contains `#/article/`.
    - Article title, content, and tags are displayed.

### 6. Filter by Tag

**Intent:** Verify that clicking a tag in the Popular Tags sidebar filters the feed.

- **Preconditions:** Tags are visible in the sidebar.
- **Steps:**
    1. Navigate to the Home page.
    2. Click on any tag in the "Popular Tags" sidebar.
- **Assertions:**
    - The active tab in the feed changes to the selected tag.
    - Articles in the feed are filtered by that tag.
