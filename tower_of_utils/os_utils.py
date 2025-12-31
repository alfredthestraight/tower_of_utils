from pathlib import Path
import os
import shutil
import pandas as pd

from os import listdir
from os.path import isfile, join




"""
File & path string manipulation/extraction functions

Each function includes a short description, parameters, and return details.
"""


def get_parent_directory(directory_path: str) -> str:
    """Return the absolute parent directory of a given path.

    Example: ".../Desktop/file.txt" -> ".../Desktop".

    Args:
        directory_path: File or directory path.
    Returns:
        Absolute path string to the parent directory.
    """
    return str(Path(directory_path).parent.absolute())



def get_filename_from_path(path: str, include_extension: bool = True) -> str:
    """Extract the filename component from a path.

    Args:
        path: Full file path.
        include_extension: If True returns the filename with extension, otherwise the stem.
    Returns:
        The filename or stem as a string.
    """
    if include_extension:
        return Path(path).name
    else:
        return Path(path).stem


def get_extension_from_path(path: str) -> str:
    """Return the file extension (without dot) from a path, or empty string for directories/no extension"""
    if Path(path).is_dir() or '.' not in str(path):
        return ''
    path_suff = str(path).split(os.sep)[-1:][0]
    extension = path_suff.split('.')[-1:][0]
    return extension


def is_dir(path: str) -> bool:
    return Path(path).is_dir()


def remove_extension_from_filename(filename: str) -> str:
    stripped_filename = filename.replace('.' + get_extension_from_path(filename), '')
    if stripped_filename == '':
        return filename
    else:
        return stripped_filename


def is_subfolder_descendant_of_folder(subfolder: str, folder: str):
    return subfolder.startswith(folder + os.sep)



def folder_size(path: str = '.') -> int:
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total


def beautify_bytes_size(size_in_bytes: int) -> str:
    """Return human-readable representations for a byte size.

    Returns a tuple: (scaled_value, unit, formatted_string).
    Units: bytes, KB, MB, GB (base 1024).
    """
    if size_in_bytes < 1024:
        return size_in_bytes, "bytes", f"{size_in_bytes} bytes"
    elif size_in_bytes < 1024**2:
        return size_in_bytes/1024, "KB", f"{size_in_bytes/1024:.0f} KB"
    elif size_in_bytes < 1024**3:
        return size_in_bytes/1024**2, "MB", f"{size_in_bytes/1024**2:.1f} MB"
    else:
        return size_in_bytes/1024**3, "GB", f"{size_in_bytes/1024**3:.1f} GB"



def get_item_size_pretty(fs) -> str:
    bytes = 0
    if isinstance(fs, str):
        fs = [fs]
    for f in fs:
        if os.path.isdir(f):
            bytes = bytes + get_folder_size_bytes(f)
        else:
            bytes = bytes + os.path.getsize(f)

    return beautify_bytes_size(bytes)



def get_folder_size_bytes(folder_path: str) -> int:
    total_size = 0
    stack = [folder_path]
    while stack:
        current_path = stack.pop()
        try:
            scandir = os.scandir(current_path)
        except:
            print(1)
        for entry in scandir:
            try:
                if entry.is_file():
                    total_size += os.path.getsize(entry.path)
                elif entry.is_dir():
                    stack.append(entry.path)
            except:
                print(1)
    return total_size


def size_string_to_bytes(size: str) -> float:
    """Convert a human-friendly size string (e.g., '12.5 MB') to bytes (float)."""
    size_num = float(size.split(' ')[0])
    size_scale = size.split(' ')[1]
    if size_scale == 'KB':
        return size_num * 1024
    elif size_scale == 'MB':
        return size_num * 1024**2
    elif size_scale == 'GB':
        return size_num * 1024**3
    else:
        return size_num


def get_path_size(path: str):
    """Return size in bytes of a file at the given path"""
    return Path(path).stat().st_size


def is_read_only(path: str) -> bool:
    """Check whether a file or directory is read-only (readable but not writable)."""
    # Check if the file or folder is readable
    readable = os.access(path, os.R_OK)
    # Check if the file or folder is writable
    writable = os.access(path, os.W_OK)

    # If it's readable but not writable, it's read-only
    if readable and not writable:
        return True
    return False


def move_item_from_dir1_to_dir2(item: str, dir1: str, dir2: str):
    """Move an item by name from dir1 to dir2.

    Returns 1 on success, -1 on failure, -1 if paths don't exist.
    """
    if os.path.exists(os.path.join(dir1, item)) and os.path.exists(dir2):
        try:
            shutil.move(os.path.join(dir1, item),
                        os.path.join(dir2, item))
            return 1
        except:
            return -1
    else:
        return -1


def delete_item(path: str):
    """Delete a file, symlink, or directory tree.

    Args:
        path: Relative or absolute path.
    Returns:
        1 on success, -1 on failure.
    Raises:
        ValueError: If the path is neither a file nor a directory.
    """
    if os.path.isfile(path) or os.path.islink(path):
        try:
            if os.path.exists(path):
                os.remove(path)  # remove the file
            success = 1
        except:
            success = -1
    elif os.path.isdir(path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)  # remove dir and all contains
            success = 1
        except:
            success = -1
    else:
        raise ValueError("file {} is not a file or dir.".format(path))
        success = -1
    return success


def copy_item_to_dir(item_full_path: str, dest_dir: str, override: bool = True):
    """Copy a file or directory into a destination directory.

    Returns 1 on success, 0 if not overridden and exists, -1 on failure.
    """
    if os.path.exists(item_full_path) and os.path.exists(dest_dir):
        item_name = get_filename_from_path(item_full_path)
        if not override and os.path.exists(os.path.join(dest_dir, item_name)):
            return 0
        try:
            if os.path.isdir(item_full_path):
                shutil.copytree(item_full_path, os.path.join(dest_dir, item_name))
            else:
                shutil.copy(item_full_path, os.path.join(dest_dir, item_name))
            return 1
        except:
            return -1
    else:
        return -1


def create_file(full_file_path: str):
    """Create an empty file if it doesn't exist. Returns 1 on success, -1 on failure."""
    try:
        open(full_file_path, 'a').close()
        return 1
    except:
        return -1


def dir_(obj, substring: str = '') -> pd.DataFrame:
    """List attributes/methods of an object filtered by substring, returned as a numpy array of names."""
    returned_values = [x for x in dir(obj) if substring in x]
    return pd.DataFrame(columns=returned_values).columns.values


def rename_file_or_dir(path_to_file_or_dir: str, new_name: str):
    """Rename a file or directory to a new name within the same parent directory."""
    new_path = os.path.join(os.sep.join(path_to_file_or_dir.split(os.sep)[:-1]), new_name)
    os.rename(path_to_file_or_dir, new_path)


def get_all_items_in_path(path: str, search_type: int = 0, extension: str = None):
    """List items in a directory with optional filtering.

    Args:
        path: Directory path to list.
        search_type: 0=all, 1=files only, 2=folders only.
        extension: When search_type=1, optionally filter files by extension suffix.
    Returns:
        List of item names in the provided directory.
    """
    all_items = []
    if os.path.exists(path):
        all_items = [f for f in listdir(path)]
    if search_type == 1:
        all_items = [f for f in all_items if isfile(join(path, f))]
        if extension is not None:
            all_items = [f for f in all_items if f.endswith(extension)]
    if search_type == 2:
        all_items = [f for f in all_items if not isfile(join(path, f))]
    return all_items

