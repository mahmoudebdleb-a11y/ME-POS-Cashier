# Fresh-install-only official cashier catalog

Decision: build a brand-new customer APK with ONLY the 28 logical products in the supplied official menu. No legacy/demo products, invoices, sales, shifts, stock movements, or test data may be seeded.

This is a NEW INSTALL profile, not an upgrade/migration or deletion procedure. Do not uninstall or erase a customer's installed app or database. Existing installations are outside this build's data-reset scope.

Acceptance gates:
1. Fresh SQLite database; product count exactly 28 logical entries; only three approved categories.
2. Official Arabic names, prices in halalas and mandatory variants match the supplied catalog; 15% VAT configuration must be validated separately for inclusive/exclusive pricing.
3. All 28 products have an image, including four newly generated replacements. No placeholders, old demo products, or image URL downloads at runtime.
4. Zero sales, sale_items, shifts, inventory ledger, invoices, and other historical transactional records at first launch.
5. No old seed routine runs after the official seed. Seed is idempotent.
6. Successful checkout, inventory behavior, printing and drawer flows must be verified on emulator and SUNMI hardware before release.
7. New installation must not reuse an existing production database. Never modify a customer device without a separate explicit installation approval.

Status: requirements approved, implementation and tests NOT YET VERIFIED.
