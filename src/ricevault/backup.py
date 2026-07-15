import json
from datetime import datetime
from pathlib import Path

from ricevault.utils import VAULT_DIR, CONFIG_DIR
from ricevault.collector import copy_file, copy_directory
from ricevault.config import KDE_CONFIG_FILES, APP_CONFIG_FILES, KDE_DIRECTORIES, get_plasma_version

def create_backup(
    name: str,
    backup_type: str,
    custom_components: list,
    apps: list,
    include_packages: bool,
    preview_path: str = None
) -> dict:
    """
    Orchestrates the backup process. Creates the folder structure,
    copies the requested files, and writes the metadata.
    """
    backup_dir = VAULT_DIR / name

    # Safety check: Prevent accidental overwrites of existing rices
    if backup_dir.exists():
        raise FileExistsError(f"A rice named '{name}' already exists. Please choose a different name or delete the old one.")

    config_dest = backup_dir / "config"
    wallpaper_dest = backup_dir / "wallpaper"

    # Create the directory structure (Phase 1 spec: Named profiles)
    config_dest.mkdir(parents=True, exist_ok=True)
    wallpaper_dest.mkdir(parents=True, exist_ok=True)

    copied_items = 0

    # 1. Backup Core KDE Configs
    # In a full implementation, we would finely map custom_components to specific files.
    # For now, if they select Full or Custom, we grab the base configs.
    if backup_type == "Full" or backup_type == "Custom":
        for file_name in KDE_CONFIG_FILES:
            src = CONFIG_DIR / file_name
            if copy_file(src, config_dest):
                copied_items += 1

    # 2. Backup Application Configs
    if apps:
        for app in apps:
            if app in APP_CONFIG_FILES:
                for file_name in APP_CONFIG_FILES[app]:
                    src = CONFIG_DIR / file_name
                    if copy_file(src, config_dest):
                        copied_items += 1

    # 3. Backup Theme Directories (Kvantum, Aurorae, etc.)
    if backup_type in ["Full", "Theme only"] or backup_type == "Custom":
        for dir_name, dir_path in KDE_DIRECTORIES.items():
            dest = backup_dir / dir_name
            if copy_directory(dir_path, dest):
                copied_items += 1

    # 4. Handle Preview Image
    if preview_path and preview_path != "Skip":
        preview_src = Path(preview_path)
        if preview_src.exists() and preview_src.is_file():
            # Keep the original file extension (e.g., .png or .jpg)
            dest_ext = preview_src.suffix
            copy_file(preview_src, backup_dir / f"preview{dest_ext}")

    # 5. Write the Modern Metadata (Phase 1 spec)
    metadata = {
        "name": name,
        "created": datetime.now().isoformat(timespec="seconds"),
        "plasma_version": get_plasma_version(),
        "backup_type": backup_type,
        "apps_included": apps if apps else [],
        "packages_included": include_packages
    }

    with open(backup_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    return {
        "status": "success",
        "path": backup_dir,
        "items_copied": copied_items
    }
