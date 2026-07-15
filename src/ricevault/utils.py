import os
import subprocess
import tempfile
import time
from pathlib import Path

# The standard Linux config directory (where KDE saves its settings)
CONFIG_DIR = Path.home() / ".config"

# The standard Linux local share directory (where KDE saves themes, icons, etc.)
LOCAL_SHARE_DIR = Path.home() / ".local" / "share"

# Set the vault directly inside the user's Documents folder
VAULT_DIR = Path.home() / "Documents" / "RiceVault Backups"

def ensure_vault():
    """Ensure the RiceVault directory exists."""
    if not VAULT_DIR.exists():
        VAULT_DIR.mkdir(parents=True, exist_ok=True)

def take_screenshot() -> str:
    """
    Takes a screenshot using KDE Spectacle in the background.
    Returns the path to the temporary image file, or None if it fails.
    """
    # Create a temporary file path
    tmp_file = Path(tempfile.gettempdir()) / f"ricevault_preview_{int(time.time())}.png"

    try:
        # -b: background (no GUI)
        # -n: do not show a notification
        # -o: output file path
        subprocess.run(
            ["spectacle", "-b", "-n", "-o", str(tmp_file)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return str(tmp_file)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
