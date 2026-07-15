import json
from datetime import datetime
from pathlib import Path

from ricevault.utils import VAULT_DIR, CONFIG_DIR
from ricevault.collector import copy_file, copy_directory
from ricevault.config import KDE_CONFIG_FILES, APP_CONFIG_FILES, KDE_DIRECTORIES
from ricevault.backup import create_backup

def validate_rice(name: str) -> bool:
    """
    Validates if a rice exists and contains a valid metadata file.
    """
    rice_dir = VAULT_DIR / name
    return rice_dir.exists() and rice_dir.is_dir() and (rice_dir / "metadata.json").exists()

def create_emergency_backup() -> str:
    """
    Takes a snapshot of the current desktop state before any destructive actions.
    Uses the exact same engine as the standard backup.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    emergency_name = f"Emergency-{timestamp}"

    # We grab everything possible for safety
    all_apps = list(APP_CONFIG_FILES.keys())

    create_backup(
        name=emergency_name,
        backup_type="Full",
        custom_components=[],
        apps=all_apps,
        include_packages=False, # Speed up emergency backups by skipping pacman queries
        preview_path=None
    )

    return emergency_name

def restore_rice(name: str) -> dict:
    """
    Orchestrates the safe restore process:
    1. Validates the target backup.
    2. Creates an emergency backup of the CURRENT state.
    3. Overwrites the live configuration with the backup files.
    """
    if not validate_rice(name):
        raise FileNotFoundError(f"Rice '{name}' is invalid, corrupted, or missing metadata.json.")

    # 1. THE FAILSAFE: Backup current system state
    emergency_name = create_emergency_backup()

    # 2. Setup paths
    rice_dir = VAULT_DIR / name
    config_src = rice_dir / "config"
    restored_items = 0

    # 3. Restore Core Configs
    if config_src.exists():
        for file_name in KDE_CONFIG_FILES:
            src = config_src / file_name
            # Only restore files that were actually backed up
            if src.exists() and copy_file(src, CONFIG_DIR):
                restored_items += 1

        # 4. Restore Application Configs
        for app_files in APP_CONFIG_FILES.values():
            for file_name in app_files:
                src = config_src / file_name
                if src.exists() and copy_file(src, CONFIG_DIR):
                    restored_items += 1

    # 5. Restore Theme Directories (Kvantum, Aurorae, etc.)
    for dir_name, dest_path in KDE_DIRECTORIES.items():
        src_dir = rice_dir / dir_name
        if src_dir.exists() and copy_directory(src_dir, dest_path):
            restored_items += 1

    # In the future, we will handle the Wallpaper replacement here

    return {
        "status": "success",
        "emergency_backup": emergency_name,
        "restored_items": restored_items
    }
