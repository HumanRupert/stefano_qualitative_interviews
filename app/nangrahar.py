import os

from app.load import transform_load


def get_nangrahar_files():
    root = "data/1. Nangrahar - NGR"
    files = [
        f"{root}/{dir_}/{file}" for dir_ in os.listdir(root)
        if not dir_.startswith('.')
        for file in os.listdir(f"{root}/{dir_}")]
    p = 'English'
    files = [f for f in files if p in f]
    return files


transform_load(get_nangrahar_files, "nangrahar")
