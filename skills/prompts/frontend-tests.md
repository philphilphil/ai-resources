---
name: frontend-tests
description: Run comprehensive Playwright QA tests across the entire frontend
disable-model-invocation: true
---

# Frontend Test Instructions

Test the entire frontend using Playwright MCP.

**IMPORTANT: Never skip a test.** Every test listed below must be executed. If a test cannot be run due to missing data or preconditions, note it as N/A with a reason — do not silently skip it.

---

## Before you start

1. Read the project's CLAUDE.md (or README) to understand how to start the app, what URL it runs on, and what test credentials to use.
2. Start the application (dev server, Docker compose, etc.) and confirm it's healthy.
3. Open the browser and log in with the test credentials.

---

## Test plan

Build a test plan by reading the frontend source code. Cover every area below that exists in the app. Skip sections that don't apply and note why.

### 1. Authentication
- **Login** — fill credentials, submit, verify redirect to the authenticated landing page
- **Register** — verify form validation (password rules, required fields, matching passwords), verify submit is disabled until valid. Do NOT actually submit unless using a disposable account.
- **Forgot password** — verify the form renders
- **Logout** — log out, verify redirect to login, log back in for remaining tests
- **Auth guards** — visit a protected route while logged out, verify redirect to login. Visit login while logged in, verify redirect away.

### 2. Main dashboard / landing page
- Verify key stats, counts, or summaries render
- Verify primary call-to-action buttons work
- Verify any secondary navigation (cards, links to sub-sections) render and link correctly

### 3. List views / tables
For each major list or table view in the app:
- Verify columns and data render correctly
- Verify date/number formatting
- **Filters** — test every filter control (text search, dropdowns, toggles, checkboxes). Verify results update.
- **Pagination** — if enough data exists, verify next/previous controls work
- **Create** — open the create dialog/form, fill required fields, save, verify the new item appears
- **Edit** — edit an item inline or via detail page, verify changes persist
- **Delete** — trigger delete, verify confirmation dialog, cancel first (verify nothing changes), then confirm on a disposable item

### 4. Detail views
For each detail/single-item view:
- Verify breadcrumbs or back navigation
- Verify all metadata and content sections render (including markdown, images, embedded content)
- **Edit mode** — toggle edit, modify a field, save, verify persistence. Test cancel discards changes.
- **Destructive actions** (delete, reset, etc.) — verify confirmation dialogs, test cancel, only confirm on disposable data

### 5. Search
- Open search (click or keyboard shortcut)
- Verify results appear after minimum character threshold
- Verify result categories are grouped and ordered correctly
- Verify keyboard navigation (arrow keys, enter, escape)
- Verify edge cases: too few characters, no results, clearing input

### 6. Navigation & layout
- **Desktop** — verify header/nav bar items, active state styling, all links work
- **Mobile** — resize to mobile width, verify responsive nav (bottom bar, hamburger menu, etc.), verify desktop-only elements hide
- **Dark mode** — toggle if available, verify theme switches, verify persistence across refresh

### 7. Settings / profile
- Verify settings page layout matches available options
- Test form validation (e.g., password mismatch shows error)
- Only submit changes on disposable accounts

### 8. Admin (if applicable)
- Verify admin-only views render for admin users
- Test admin actions (lock/unlock, role changes, etc.) — only confirm on test users

### 9. Error handling
- **404** — navigate to a nonexistent route, verify error page renders with a way back
- **Invalid IDs** — navigate to a detail view with a bogus ID, verify graceful handling (redirect or error message)

---

## Rules

- Execute tests in order. Check off each one as you go.
- For every assertion, note pass/fail. If fail, capture what you actually saw.
- Never perform destructive actions (delete, reset) on real data — only on items you created during testing or that are explicitly disposable.
- If a section doesn't exist in the app, skip it and note "N/A — app does not have [feature]".
