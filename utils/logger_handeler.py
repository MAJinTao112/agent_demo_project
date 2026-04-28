import os

from utils.path_tool import get_abs_path

LOG_ROOT = get_abs_path("logs")


os.makedirs(LOG_ROOT, exist_ok=True)



