from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ... import _decorators
from ..._base import DS
from .... import database

@DS.message(Command("show_keys"))
@_decorators.security
async def _show_keys(message: Message) -> None:
    keys: tuple[str, ...] = await database.keys.keys()
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder(
        [[
            InlineKeyboardButton(text=key, callback_data=f"key_info {key}")
            for key in keys
        ]]
    )
    builder.adjust(1)
    await message.answer("All keys:", reply_markup=builder.as_markup())
