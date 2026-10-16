from pathlib import Path

root=Path('build-src')
db=root/'app/src/main/java/com/mahmoud/meposcashier/PosDb.java'
gradle=root/'app/build.gradle'

# Version bump for the image-bundled customer build.
s=gradle.read_text(encoding='utf-8')
s=s.replace('versionCode 106','versionCode 107').replace("versionName '1.0.6-client-full'","versionName '1.0.7-client-images'")
gradle.write_text(s,encoding='utf-8')

# Give every seeded customer product a bundled drawable URI. Custom user-selected
# images can still replace this later through the existing product image picker.
s=db.read_text(encoding='utf-8')
anchor='''            db.execSQL("UPDATE products SET name=?,category=?,price_minor=?,low_stock=?,barcode=?,active=1 WHERE id=?",new Object[]{r[1],r[2],r[3],r[5],r[6],r[0]});'''
replacement=anchor+'''\n            db.execSQL("UPDATE products SET image_uri=? WHERE id=? AND (image_uri IS NULL OR image_uri='' OR image_uri LIKE 'android.resource://%')",new Object[]{"android.resource://com.mahmoud.meposcashier/drawable/prod_"+r[0],r[0]});'''
if anchor not in s:
    raise SystemExit('BUNDLED107_DB_ANCHOR_NOT_FOUND')
s=s.replace(anchor,replacement,1)
db.write_text(s,encoding='utf-8')

checks=[
 ('version',"1.0.7-client-images" in gradle.read_text(encoding='utf-8')),
 ('resource_uri','android.resource://com.mahmoud.meposcashier/drawable/prod_' in db.read_text(encoding='utf-8')),
 ('image_column','image_uri' in db.read_text(encoding='utf-8')),
]
for name,ok in checks:
    if not ok: raise SystemExit('BUNDLED107_CHECK_FAILED:'+name)
print('BUNDLED_PRODUCT_IMAGES_107_APPLIED')
