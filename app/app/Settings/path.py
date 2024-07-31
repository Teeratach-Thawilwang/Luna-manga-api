import os
import re
from pathlib import Path

MAIN_DIR = str(Path(__file__).resolve().parent.parent.parent).replace("\\", "/") + "/"
BASE_DIR = MAIN_DIR + "app/"
STORAGE_DIR = MAIN_DIR + "storage/"
TEMPORARY_DIR = MAIN_DIR + "storage/temporary/"
TEMPLATES_DIR = BASE_DIR + "Templates/"


def env(key, default=None):
    value = os.environ.get(key)
    if re.match(r"\[.*\]", value):
        value = eval(value)

    if value is None:
        os.environ.setdefault(key, str(default))
        return default
    return value
