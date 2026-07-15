import subprocess
from pathlib import Path
from ricevault.utils import CONFIG_DIR, LOCAL_SHARE_DIR

# ---------------------------------------------------------
# Core Configuration Paths
# ---------------------------------------------------------

# The essential text files that define the KDE Plasma UI and Window Manager
KDE_CONFIG_FILES = [
    "kdeglobals",
    "kwinrc",
    "kglobalshortcutsrc",
    "plasmarc",
    "plasma-org.kde.plasma.desktop-appletsrc"
]

# Application specific configs
APP_CONFIG_FILES = {
    "Konsole": ["konsolerc"],
    "Dolphin": ["dolphinrc"],
    "Kate": ["katerc", "kateschemarc"]
}

# Entire directories that contain theme assets
KDE_DIRECTORIES = {
    "Kvantum": CONFIG_DIR / "Kvantum",
    "Aurorae": LOCAL_SHARE_DIR / "aurorae",
    "ColorSchemes": LOCAL_SHARE_DIR / "color-schemes",
    "PlasmaLookFeel": LOCAL_SHARE_DIR / "plasma" / "look-and-feel"
}

# ---------------------------------------------------------
# System State Detection
# ---------------------------------------------------------

def get_plasma_version() -> str:
    """
    Detects the current Plasma version running on the system.
    Returns something like 'plasmashell 6.1.2' or 'Unknown'.
    """
    try:
        # We use subprocess to ask KDE for its version directly
        result = subprocess.run(
            ["plasmashell", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "Unknown"

def get_active_wallpaper() -> str:
    """
    Reads the current wallpaper path from plasma applet config.
    (Placeholder - parsing KDE's multi-monitor config is complex,
    we will build the regex for this later).
    """
    return "Unknown"
