from .AttrDict import AttrDict
from .Logger import logger
from typing import Final as __Final

import os as __os
from dotenv import load_dotenv as __load_dotenv

__dotenv_path = __os.path.join(__os.path.dirname('../'), '.env')
__load_dotenv(__dotenv_path)
CONFIG: __Final = AttrDict(__os.environ)
