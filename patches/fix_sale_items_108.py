"""Fix the 1.0.8 checkout crash without changing or deleting customer data.

The APK schema contains nine sale_items columns; two trailing flags have
database defaults. Explicitly name the seven columns the checkout supplies.
Run after full_scope_106.py and bundled_images_107.py.
"""
from pathlib import Path

db = Path("build-src/app/src/main/java/com/mahmoud/meposcashier/PosDb.java")
source = db.read_text(encoding="utf-8")
old = "INSERT INTO sale_items VALUES(?,?,?,?,?,?,?)"
new = ("INSERT INTO sale_items"
       "(id,sale_id,product_id,product_name,qty,unit_price_minor,line_total_minor)"
       " VALUES(?,?,?,?,?,?,?)")
if source.count(old) != 1:
    raise SystemExit("FAIL: expected exactly one original sale_items INSERT; source differs")
if "printed INTEGER NOT NULL DEFAULT 0,visible INTEGER NOT NULL DEFAULT 1" not in source:
    raise SystemExit("FAIL: expected 9-column sale_items schema not found")
source = source.replace(old, new)
db.write_text(source, encoding="utf-8")
assert old not in db.read_text(encoding="utf-8")
print("SALE_ITEMS_9_COLUMN_INSERT_FIXED")
