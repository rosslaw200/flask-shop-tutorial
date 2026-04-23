# Test Logs

Comprehensive record of system testing, validation logic, and iterative debugging.

## 🧪 System & Logic Test Suite

| ID | Date | Component | Type | Prerequisites | Feature | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T-01 | 2026-03-26 | Auth | Unit | Server running | Login Logic | Valid user gains session | Session created successfully | **PASS** |
| T-02 | 2026-03-26 | Auth | Unit | User exists | Password Validation| Rejects incorrect pass | "Invalid login" displayed | **PASS** |
| T-03 | 2026-03-27 | Auth | Integration| DB connection | Registration | New record added to DB | User ID returned, DB updated | **PASS** |
| T-04 | 2026-03-28 | Auth | System | App initialized | Duplicate Email | Prevents duplicate registration | **Bug**: Created 2nd record | **FAIL** |
| T-05 | 2026-03-30 | Shop | Integration| DB seeded | Catalogue Load | Displays 4 featured items | Items loaded from DB | **PASS** |
| T-06 | 2026-04-03 | Shop | Logic | Stock > 0 | Order Placement | Stock decrements by Qty | Stock reduced correctly | **PASS** |
| T-07 | 2026-04-05 | Shop | Logic | User in session | Stock Validation | Rejects Qty > Stock | **Bug**: Stock went negative | **FAIL** |
| T-08 | 2026-04-07 | Admin | Unit | role='admin' | Dashboard Access | Allow admins, block users| Redirects non-admins | **PASS** |
| T-09 | 2026-04-09 | Admin | Integration| Dashboard open | Add Product | New item appears in DB | Product visible in catalogue | **PASS** |
| T-10 | 2026-04-12 | Shop | System | Data exists | Search Logic | Filter by keyword "Honey" | Returns only honey products | **PASS** |
| T-11 | 2026-04-15 | Shop | Unit | Empty input | Search Guard | Handles null query gracefully| **Bug**: Server 500 error | **FAIL** |
| T-12 | 2026-04-18 | Admin | Integration| Order exists | Status Update | Update 'Pending' to 'Sent'| DB record updated correctly | **PASS** |
| T-13 | 2026-04-20 | Admin | Unit | Row selected | Dashboard Modals | Open correct ID in modal | Correct data populated | **PASS** |
| T-14 | 2026-04-22 | Shop | Unit | Numeric input | Qty Validation | Reject negative numbers | **Bug**: Accepted -5 items | **FAIL** |
| T-15 | 2026-04-23 | Shop | System | App finalized | End-to-End Flow | Registration to Purchase | Full workflow completed | **PASS** |

## 🛠️ Iteration & Bug History (Logic & Validation)

### [BUG-001] Registration Integrity (March 28)
- **Component**: Authentication
- **Expected Result**: System should check for existing email before insertion.
- **Actual Result**: Multiple users registered with `test@test.com`.
- **What Changed**: Implemented `SELECT * FROM users WHERE email=?` guard clause in `app.py`.
- **Iteration**: v1.1.2 fixed the collision logic.

### [BUG-002] Negative Stock Levels (April 05)
- **Component**: Order Processing
- **Expected Result**: Order should fail if `quantity > stock`.
- **Actual Result**: User could order 100 tomatoes when only 50 were available, resulting in `-50` stock.
- **What Changed**: Added server-side validation `if quantity <= stock:` before the SQL `UPDATE` statement.
- **Iteration**: v1.3.1 prevents inventory debt.

### [BUG-003] Search Module Crash (April 15)
- **Component**: Catalogue Search
- **Expected Result**: Empty search should redirect to the full catalogue.
- **Actual Result**: `TypeError` when `keyword` was None.
- **What Changed**: Added null check `if not keyword: return redirect('/catalogue')`.
- **Iteration**: v1.5.1 adds input sanitization.

### [BUG-004] Dashboard Row Mismatch (April 20)
- **Component**: Admin Interface
- **Expected Result**: Selecting "Update" on Product B should open Product B's details.
- **Actual Result**: Always opened Product A's details regardless of row.
- **What Changed**: Refactored `script.js` to use `dataset` attributes on each row to pass the correct ID to the modal.
- **Iteration**: v2.0.1 fixed the dynamic data binding.

### [BUG-005] Inventory Injection (April 22)
- **Component**: Validation Logic
- **Expected Result**: Quantity must be a positive integer.
- **Actual Result**: Negative numbers were accepted, allowing users to "add" stock via the purchase route.
- **What Changed**: Added `if quantity > 0` check to the order route.
- **Iteration**: v2.1.1 closes the logic loop.
