import zipfile
import json
import os
import hashlib
from pathlib import Path

addons_dir = Path("addons")
supported_platforms = {
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
    
    filename = zip_path.name
    platform = filename.split("-")[-1].replace(".mvladdon", "")
    
    if platform not in supported_platforms:
        print(f"Unknown platform name {platform} in {filename}... skipping.")
        continue
    
    build_target = supported_platforms[platform]
    
    file_size = os.path.getsize(zip_path)
    with open(zip_path, 'rb', buffering=0) as f:
        file_hash = hashlib.file_digest(f, 'sha256').hexdigest()
    
    catalog_entry = catalog.get(addonDef["ReleaseGuid"], {
        "DisplayName": addonDef["DisplayName"],
        "Author": addonDef["Author"],
        "Version": addonDef["ReleaseVersion"],
        "Artifacts": {}
    })
    
    catalog_entry["artifacts"][build_target] = {
        "Url": f"https://raw.githubusercontent.com/ipodtouch0218/NSMB-MarioVsLuigi-AddonRepository/main/{zip_path}",
        "Size": file_size,
        "Sha256": file_hash
    }
    
    catalog[addonDef["ReleaseGuid"]] = catalog_entry


print(f"Found {len(catalog)} addon(s) to write to catalog.json")    
with open("catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)