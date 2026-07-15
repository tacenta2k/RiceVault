import shutil
from pathlib import Path
from typing import Union

def copy_file(src: Union[str, Path], dest: Union[str, Path]) -> bool:
    """
    Safely copies a single file from source to destination.
    Preserves original file metadata (timestamps, permissions).

    Args:
        src: The path to the file to copy.
        dest: The destination directory or exact file path.

    Returns:
        bool: True if copied successfully, False if source doesn't exist.
    """
    src_path = Path(src)
    dest_path = Path(dest)

    # If the source file doesn't exist, we just return False.
    # This is normal since not all KDE users have every config file generated.
    if not src_path.exists() or not src_path.is_file():
        return False

    # Ensure the parent directory of the destination exists
    if dest_path.is_dir():
        # If dest is a directory, keep the original filename
        dest_file = dest_path / src_path.name
    else:
        # If dest is a specific file path, use it directly
        dest_file = dest_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(src_path, dest_file)
        return True
    except Exception as e:
        # In a full production app we'd log this, but for now we catch and fail safely
        print(f"Error copying file {src_path.name}: {e}")
        return False


def copy_directory(src: Union[str, Path], dest: Union[str, Path]) -> bool:
    """
    Safely copies an entire directory tree.

    Args:
        src: The source directory path.
        dest: The destination directory path.

    Returns:
        bool: True if copied successfully, False if source doesn't exist.
    """
    src_path = Path(src)
    dest_path = Path(dest)

    if not src_path.exists() or not src_path.is_dir():
        return False

    try:
        # dirs_exist_ok=True allows us to merge into existing backup directories
        # safely without throwing an error if the folder was already created.
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        return True
    except Exception as e:
        print(f"Error copying directory {src_path.name}: {e}")
        return False
