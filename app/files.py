import os
import typing as T

from app.load import transform_load, Region


def _get_files(root: str, p: str, case_sensitive: bool):
    files = [
        f"{root}/{dir_}/{file}" for dir_ in os.listdir(root)
        if not dir_.startswith('.')
        for file in os.listdir(f"{root}/{dir_}")]

    files = [f for f in files if p in f] \
        if case_sensitive \
        else [f for f in files if p in f.lower()]

    return files


def get_nangrahar_files():
    root = "data/1. Nangrahar - NGR"
    p = 'English'
    return _get_files(root, p, False)


def get_kandahar_files():
    p = "eng"
    root = "data/2. Kandahar - KDR"
    gov_files = _get_files(f"{root}/Government KDR IDI", p, False)
    non_gov_files = _get_files(f"{root}/Non-Government KDR IDI", p, False)
    return gov_files + non_gov_files


REGIONS: T.List[Region] = [
    {
        "name": "nangrahar",
        "files_method": get_nangrahar_files
    },
    {
        "name": "kandahar",
        "files_method": get_kandahar_files
    }
]
