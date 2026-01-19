import zipfile
import json
import os
from pathlib import Path

addons_dir = Path("addons")
catalog = []

for zip_path in addons_dir.rglob("*.mvladdon"):
    with zipfile.ZipFile(zip_path) as z:
        with z.open("addon.json") as f:
            addonDef = json.load(f)

    catalog.append({
        "ReleaseGuid": addonDef["ReleaseGuid"],
        "DisplayName": addonDef["DisplayName"],
        "Author": addonDef["Author"],
        "Version": addonDef["Version"],
        "Size": os.path.getsize(zip_path),
        "DownloadUrl": f"https://github.com/ipodtouch0218/NSMB-MarioVsLuigi-AddonRepository/raw/refs/heads/main/addons/{zip_path.name}"
    })

print(f"Found {len(catalog)} addon(s) to write to catalog.json")    
with open("catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)