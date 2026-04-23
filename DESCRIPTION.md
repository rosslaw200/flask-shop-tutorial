# Version Logs 

Documenting the evolution of the Greenfield Hub with a focus on system logic, database integrity, and functional validation.

## [v2.1.1] - 2026-04-23
### Changed
- **Input Validation**: Added `if quantity > 0` check to the `/order` route.
- **Why**: To prevent a logic flaw where users could "add" stock to the inventory by ordering negative quantities.

## [v2.1.0] - 2026-04-20
### Changed
- **Null-Type Guard**: Implemented a check for empty search strings in `app.py`.
- **Why**: The previous implementation caused a `TypeError` crash when users submitted an empty search bar; this ensures system stability.

## [v2.0.1] - 2026-04-18
### Changed
- **Admin Data Binding**: Switched from static IDs to `dataset` attributes in the dashboard JS.
- **Why**: Previous logic only updated the first product in the list; this change ensures the correct database record is selected for updates/deletions.

## [v2.0.0] - 2026-04-15
### Changed
- **Frontend Modularization**: Moved all logic to `script.js` and styling to `style.css`.
- **Why**: To separate concerns and improve maintainability as the system's logic (especially in the admin dashboard) became more complex.

## [v1.5.0] - 2026-04-12
### Added
- **Order Status Tracking**: Added a `status` column to the `orders` table.
- **Why**: To provide a functional bridge between customers and producers, allowing for real-time tracking of fulfillment (Pending, Shipped, etc.).

## [v1.4.0] - 2026-04-09
### Changed
- **Inventory Validation**: Implemented server-side stock checks before confirming orders.
- **Why**: To prevent "inventory debt" where orders were accepted for items that were out of stock, leading to negative values in the database.

## [v1.3.0] - 2026-04-05
### Added
- **Admin Authorization**: Implemented role-based access control (RBAC) for the `/dashboard` route.
- **Why**: To ensure that sensitive inventory and order data is only accessible to users with 'admin' privileges, preventing unauthorized data modification.

## [v1.2.0] - 2026-03-31
### Changed
- **Account Uniqueness Logic**: Added a pre-registration check for existing emails.
- **Why**: To maintain database integrity and prevent account collisions where multiple users could claim the same identity.

## [v1.1.0] - 2026-03-27
### Changed
- **Persistence Layer**: Replaced hardcoded Python lists with a SQLite3 database.
- **Why**: To enable persistent data storage, allowing user accounts, product stock, and order history to survive server restarts.

## [v1.0.1] - 2026-03-24
### Fixed
- **Routing Configuration**: Corrected the static file pathing for the Flask app.
- **Why**: Initial setup failed to load necessary CSS/JS assets, rendering the system's functional components unusable.

## [v1.0.0] - 2026-03-23
### Added
- **Core Architecture**: Established the Flask application structure and routing.
- **Why**: To create the foundational framework for the Greenfield Hub, enabling basic HTTP request handling and template rendering.
