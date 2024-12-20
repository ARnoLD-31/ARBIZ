import asyncio

from aiogram.filters import Command
from aiogram.types import Message

from .. import _decorators
from .._base import DS
from ... import avito, output


@DS.message(Command("start_avito"))
@_decorators.security
async def _start_avito(message: Message) -> None:
    if not avito.config.paused:
        await message.answer("Avito polling is running")
    else:
        avito.config.paused = False
        asyncio.create_task(avito.polling())
        output.warning("MAIN", "Avito polling started")
        await message.answer("Avito polling started")


@DS.message(Command("stop_avito"))
@_decorators.security
async def _stop_avito(message: Message) -> None:
    if avito.config.paused:
        await message.answer("Avito polling is stopped")
    else:
        avito.config.paused = True
        output.warning("MAIN", "Avito polling stopped")
        await message.answer("Avito polling stopped")
