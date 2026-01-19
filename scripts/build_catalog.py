import zipfile
import json
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
        "FileName": zip_path.name
    })
    
    
with open("catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)