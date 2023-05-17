from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class InTextFilter(BaseFilter):
    def __init__(self, message: Union[str]):
        self.message = str(message)

    async def __call__(self, message: Message) -> bool:
        if isinstance(message.text, str):
            return self.message in message.text
        elif isinstance(message.text, str):
            return self.message in message.caption
        return False
