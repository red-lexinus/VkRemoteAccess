from .AttrDict import AttrDict
from .Logger import logger
from typing import Final as __Final

import os as __os
from dotenv import load_dotenv as __load_dotenv
from pathlib import Path as __Path


def get_project_path(file_exists_only_in_main_dir: str = ".env"):
    for i in range(4):
        path = __Path(__file__).parents[i]
        if file_exists_only_in_main_dir in __os.listdir(path):
            return path
    raise 'У нас проблемы'


__dotenv_path = __os.path.join(get_project_path(), '.env')
__load_dotenv(__dotenv_path)
CONFIG: __Final = AttrDict(__os.environ)
