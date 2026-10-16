from pathlib import Path

root=Path('build-src')
main=root/'app/src/main/java/com/mahmoud/meposcashier/MainActivity.java'
sunmi=root/'app/src/main/java/com/mahmoud/meposcashier/SunmiPrinter.java'
gradle=root/'app/build.gradle'

# Bump so it can be installed over the previous 1.0.4 client build.
s=gradle.read_text(encoding='utf-8')
s=s.replace('versionCode 104','versionCode 105').replace("versionName '1.0.4-client'","versionName '1.0.5-drawer-test'")
gradle.write_text(s,encoding='utf-8')

# Open the SUNMI cash drawer only after a CASH sale has been successfully committed.
s=main.read_text(encoding='utf-8')
old='try { PosDb.Sale s=db.checkout(new ArrayList<>(cart.values()),payment,taxBps); cart.clear();'
new='try { PosDb.Sale s=db.checkout(new ArrayList<>(cart.values()),payment,taxBps); if("CASH".equals(payment) && sunmi!=null){ if(!sunmi.openDrawer()) toast("تم حفظ البيع النقدي لكن تعذر فتح درج الكاشير"); } cart.clear();'
if old not in s:
    raise SystemExit('DRAWER_HOTFIX_FAILED: checkout anchor not found')
s=s.replace(old,new,1)
main.write_text(s,encoding='utf-8')

# Use the same successfully-bound SUNMI printer service for the drawer.
s=sunmi.read_text(encoding='utf-8')
anchor='    public void close(){ try{ InnerPrinterManager.getInstance().unBindService(context,callback); }catch(Exception ignored){} service=null; }'
method='''    public boolean openDrawer(){\n        SunmiPrinterService s=service; if(s==null)return false;\n        try{ s.openDrawer(null); return true; }\n        catch(RemoteException e){ service=null; return false; }\n    }\n'''
if anchor not in s:
    raise SystemExit('DRAWER_HOTFIX_FAILED: SunmiPrinter close anchor not found')
s=s.replace(anchor,method+anchor,1)
sunmi.write_text(s,encoding='utf-8')

checks=[
 ('version',"1.0.5-drawer-test" in gradle.read_text(encoding='utf-8')),
 ('cash_only','"CASH".equals(payment)' in main.read_text(encoding='utf-8')),
 ('open_drawer_call','sunmi.openDrawer()' in main.read_text(encoding='utf-8')),
 ('sunmi_drawer_api','s.openDrawer(null)' in sunmi.read_text(encoding='utf-8')),
 ('print_preserved','s.printText(text+"\\n",null)' in sunmi.read_text(encoding='utf-8')),
]
for name,ok in checks:
    if not ok: raise SystemExit('DRAWER_HOTFIX_CHECK_FAILED:'+name)
print('SUNMI_T2S_DRAWER_HOTFIX_105_APPLIED')
