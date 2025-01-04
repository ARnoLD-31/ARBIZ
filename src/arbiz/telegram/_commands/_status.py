from aiogram.types import Message
from aiogram.filters import Command

from .. import _decorators
from .._base import DS
from ... import avito, yam


@DS.message(Command("status"))
@_decorators.security
async def _status(message: Message) -> None:
    text: str = (
        "Program's status:\n"
        f"\t\tAvito polling: {avito.config.polling}\n"
        f"\t\tYandex Market polling: {yam.config.polling}\n"
    )
    await message.answer(text)
