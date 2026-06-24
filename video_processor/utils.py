# utils.py

import os


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_filename_without_ext(path):
    return os.path.splitext(os.path.basename(path))[0]