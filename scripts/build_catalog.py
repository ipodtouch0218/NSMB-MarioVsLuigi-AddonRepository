import zipfile
import json
import os
import hashlib
from pathlib import Path

addons_dir = Path("addons")
platforms = {
    "Win32": "StandaloneWindows",
    "MacOS": "StandaloneOSX",
    "Linux": "StandaloneLinux64",
    "Android": "Android",
    "iOS": "iOS",
    "WebGL": "WebGL"
}

catalog = {}

for zip_path in addons_dir.rglob("*.mvladdon"):
    with zipfile.ZipFile(zip_path) as z:
        with z.open("addon.json") as f:
            addonDef = json.load(f)
    
    catalog_entry = catalog.get(addonDef["ReleaseGuid"], {
        "displayName": addonDef["DisplayName"],
        "author": addonDef["Author"],
        "version": addonDef["ReleaseVersion"],
        "artifacts": {}
    })
    
    filename = os.path.basename(zip_path)
    platform = filename.split("-")[-1].replace(".mvladdon", "")
    
    if platform not in platforms:
        print(f"Unknown platform name {platform} in {filename}... skipping.")
        continue
    
    file_size = os.path.getsize(zip_path)
    with open(filename, 'rb', buffering=0) as f:
        file_hash = hashlib.file_digest(f, 'sha256').hexdigest()
    
    catalog_entry["Artifacts"][platform] = {
        "size": file_size,
        "sha256": file_hash,
        "url": f"https://raw.githubusercontent.com/ipodtouch0218/NSMB-MarioVsLuigi-AddonRepository/main/addons/{zip_path.name}"
    }

print(f"Found {len(catalog)} addon(s) to write to catalog.json")    
with open("catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)