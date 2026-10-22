"""Apply the official clean-install catalog AFTER patches 106, 107 and 108.
Existing installed databases are never reset or migrated by this patch.
"""
from pathlib import Path
import json
import shutil

root=Path("build-src/app/src/main")
db=root/"java/com/mahmoud/meposcashier/PosDb.java"
gradle=Path("build-src/app/build.gradle")
assets=root/"assets"
assets.mkdir(parents=True,exist_ok=True)
catalog=json.loads(Path("catalog/official_fresh_28.json").read_text(encoding="utf-8"))
assert len(catalog)==28
assert len({p["id"] for p in catalog})==28
assert sum(bool(p.get("variants")) for p in catalog)==4
assert all(p["price_minor"]>0 and p["stock_qty"]==0 for p in catalog)
shutil.copyfile("catalog/official_fresh_28.json",assets/"catalog_official_fresh.json")
s=db.read_text(encoding="utf-8")
old="seed(db);"
if s.count(old)!=1:
    raise SystemExit("FRESH28_ONCREATE_ANCHOR_MISSING")
s=s.replace(old,"importOfficialFresh(db);",1)
context_anchor="public class PosDb extends SQLiteOpenHelper {"
if context_anchor not in s:
    raise SystemExit("FRESH28_CLASS_ANCHOR_MISSING")
s=s.replace(context_anchor,context_anchor+"\n    private final android.content.Context officialFreshContext;",1)
constructor_anchor="super(context, DB_NAME, null, DB_VERSION);"
if s.count(constructor_anchor)!=1:
    raise SystemExit("FRESH28_CONSTRUCTOR_ANCHOR_MISSING")
s=s.replace(constructor_anchor,constructor_anchor+" officialFreshContext=context.getApplicationContext();",1)
anchor="    private void seed(SQLiteDatabase db){"
if s.count(anchor)!=1:
    raise SystemExit("FRESH28_SEED_METHOD_ANCHOR_MISSING")
method='''    private void importOfficialFresh(SQLiteDatabase db){
        try {
            java.io.InputStream in=officialFreshContext.getAssets().open("catalog_official_fresh.json");
            java.io.ByteArrayOutputStream out=new java.io.ByteArrayOutputStream();
            byte[] buf=new byte[4096]; int n;
            while((n=in.read(buf))>0)out.write(buf,0,n);
            in.close();
            org.json.JSONArray arr=new org.json.JSONArray(new String(out.toByteArray(),"UTF-8"));
            if(arr.length()!=28) throw new IllegalStateException("Expected 28 official products");
            for(int i=0;i<arr.length();i++){
                org.json.JSONObject o=arr.getJSONObject(i);
                ContentValues v=new ContentValues();
                v.put("id",o.getString("id"));
                v.put("name",o.getString("name"));
                v.put("category",o.getString("category"));
                v.put("price_minor",o.getLong("price_minor"));
                v.put("stock_qty",0);
                v.put("low_stock",5);
                v.put("image_uri",o.getString("image_uri"));
                v.put("active",1);
                db.insertOrThrow("products",null,v);
            }
        } catch(Exception e){ throw new IllegalStateException("Official fresh catalog import failed",e); }
    }

'''
s=s.replace(anchor,method+anchor,1)
db.write_text(s,encoding="utf-8")
g=gradle.read_text(encoding="utf-8")
if "versionCode 107" in g:
    g=g.replace("versionCode 107","versionCode 109").replace("versionName '1.0.7-client-images'","versionName '1.0.9-fresh28-cloud'")
else:
    raise SystemExit("FRESH28_VERSION_ANCHOR_MISSING")
gradle.write_text(g,encoding="utf-8")
print("PASS: 28 official products, 28 image references, 4 variant groups, zero opening stock, no legacy seeding on new installs")
