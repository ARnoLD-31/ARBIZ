from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..._base import BOT, DS
from .... import database


@DS.callback_query(F.data.startswith("key_delete"))
async def _key_delete(callback: CallbackQuery) -> None:
    key: str = callback.data.replace("key_delete ", "")
    await database.keys.delete(key)
    await callback.answer("Key deleted")
    await BOT.edit_message_text(
        "Key deleted",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )


@DS.callback_query(F.data.startswith("key_info"))
async def _key_info(callback: CallbackQuery) -> None:
    key: str = callback.data.replace("key_info ", "")
    info: dict[str, None | str | int] = await database.keys.info(key)
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(
                    text="Delete", callback_data=f"key_delete {key}"
                ),
            ]
        ]
    )
    keyboard.adjust(1)
    text: str = f"Key {key}:\nInfo:"
    for parameter, value in info.items():
        if isinstance(value, str):
            value: str = value[0].upper() + value[1:]
        text += f"\n\t\t{parameter.capitalize()}: {value}"
    await callback.message.answer(text, reply_markup=keyboard.as_markup())
    await BOT.delete_message(
        callback.from_user.id,
        callback.message.message_id,
    )
