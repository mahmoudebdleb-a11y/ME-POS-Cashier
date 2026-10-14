# ME POS Cashier

Standalone cashier-only Android application. This repository/project is intentionally independent from the legacy ME POS repository.

## Runtime scope
- Sales / POS
- Products
- Inventory
- Invoices
- 30-day sales history
- Network thermal printing
- Local-first SQLite storage

## Safety / coexistence
- Package: `com.mahmoud.meposcashier` (different from legacy package)
- Minimum Android: API 22
- No cloud sync, branches, CRM, loyalty, suppliers, attendance, barista/customer display, licensing, or Play Billing in this edition.
- Sales checkout is transactional: sale + items + stock movements commit together or rollback together.

## Alpha 02
- Product add/edit/activate/deactivate.
- Stock adjustment with immutable movement entries and negative-stock protection.
- Cash/card/mixed payment selection.
- Invoice details and reprint from invoice/history screens.
- Configurable network printer host/port with test action.
- Sales history windows: today / 7 days / 30 days.
- GitHub Actions workflow builds and publishes a debug APK artifact.

## Alpha 03
- Inline search (no search sidebar) for sales/products/inventory/invoices/history.
- Local backup and restore using Android's Storage Access Framework.
- Restore validates SQLite integrity and expected tables before replacing the live database.
- Checkout arithmetic extracted to a pure Java core with unit tests for totals, tax rounding, quantities, and negative-stock prevention.
- CI runs unit tests before assembling the debug APK.
