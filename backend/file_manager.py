import os
import shutil
import zipfile
from pathlib import Path
from send2trash import send2trash


def copy_item(src: str, dest_dir: str) -> bool:
    """Copy a file or directory safely to a destination folder."""
    try:
        src_path = Path(src)
        dest_path = Path(dest_dir) / src_path.name
        if src_path.is_dir():
            shutil.copytree(src, str(dest_path))
        else:
            shutil.copy2(src, str(dest_path))
        return True
    except Exception:
        return False


def move_item(src: str, dest_dir: str) -> bool:
    """Move a file or directory to a destination folder."""
    try:
        src_path = Path(src)
        dest_path = Path(dest_dir) / src_path.name
        shutil.move(src, str(dest_path))
        return True
    except Exception:
        return False


def rename_item(src: str, new_name: str) -> bool:
    """Rename a file or folder in its current directory."""
    try:
        src_path = Path(src)
        new_path = src_path.parent / new_name
        src_path.rename(new_path)
        return True
    except Exception:
        return False


def delete_item(path: str, recycle: bool = True) -> bool:
    """Delete a file or folder, using Send2Trash (Recycle Bin) by default."""
    try:
        if recycle:
            send2trash(path)
        else:
            p = Path(path)
            if p.is_dir():
                shutil.rmtree(path)
            else:
                p.unlink()
        return True
    except Exception:
        return False


def zip_compress(src_path: str, zip_dest: str) -> bool:
    """Compress a file or folder into a ZIP archive."""
    try:
        path = Path(src_path)
        with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as zipf:
            if path.is_dir():
                for root, _, files in os.walk(src_path):
                    for file in files:
                        full_path = Path(root) / file
                        arcname = full_path.relative_to(path.parent)
                        zipf.write(str(full_path), str(arcname))
            else:
                zipf.write(src_path, path.name)
        return True
    except Exception:
        return False


def zip_extract(zip_path: str, extract_to: str) -> bool:
    """Extract a ZIP archive to a destination directory."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(extract_to)
        return True
    except Exception:
        return False
