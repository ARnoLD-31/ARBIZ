import sys

from aiogram.filters import Command
from aiogram.types import Message

from .. import _decorators
from .._base import DS
from ... import output


@DS.message(Command("terminate"))
@_decorators.security
async def _terminate(message: Message) -> None:
    await message.answer("Program terminated")
    output.fatal_error("MAIN", "Program terminated")
    sys.exit(0)
