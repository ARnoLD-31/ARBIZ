import asyncio

from aiogram.filters import Command
from aiogram.types import Message

from ... import _decorators
from ..._base import DS
from .... import avito, yam, output


@DS.message(Command("start_yam"))
@_decorators.security
async def _start_yam(message: Message) -> None:
    if yam.config.polling:
        await message.answer("Yandex Market polling is running")
    else:
        yam.config.polling = True
        asyncio.create_task(yam.polling())
        output.warning("MAIN", "Yandex Market polling started")
        await message.answer("Yandex Market polling started")


@DS.message(Command("stop_yam"))
@_decorators.security
async def _stop_yam(message: Message) -> None:
    if not yam.config.polling:
        await message.answer("Yandex Market polling is stopped")
    else:
        yam.config.polling = False
        output.warning("MAIN", "Yandex Market polling stopped")
        await message.answer("Yandex Market polling stopped")


@DS.message(Command("start_avito"))
@_decorators.security
async def _start_avito(message: Message) -> None:
    if avito.config.polling:
        await message.answer("Avito polling is running")
    else:
        avito.config.polling = True
        asyncio.create_task(avito.polling())
        output.warning("MAIN", "Avito polling started")
        await message.answer("Avito polling started")


@DS.message(Command("stop_avito"))
@_decorators.security
async def _stop_avito(message: Message) -> None:
    if not avito.config.polling:
        await message.answer("Avito polling is stopped")
    else:
        avito.config.polling = False
        output.warning("MAIN", "Avito polling stopped")
        await message.answer("Avito polling stopped")
