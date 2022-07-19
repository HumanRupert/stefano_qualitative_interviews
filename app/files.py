import os
import typing as T
from glob import glob

from app.load import transform_load, Region


def _get_files(root: str, p: str, case_sensitive: bool):
    files = glob(root + '/**/*.docx', recursive=True)
    files = [f for f in files if p in f] \
        if case_sensitive \
        else [f for f in files if p.lower() in f.lower()]

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


def get_kabul_files():
    p = "translated"
    root = "data/4. Kabul - KBL"
    return _get_files(root, p, False)


REGIONS: T.List[Region] = [
    {
        "name": "nangrahar",
        "files_method": get_nangrahar_files
    },
    {
        "name": "kandahar",
        "files_method": get_kandahar_files
    },
    {
        "name": "kabul",
        "files_method": get_kabul_files
    }
]

transform_load(REGIONS[-1])
