from aiogram import F
from aiogram.types import CallbackQuery

from .._base import DS
from ... import database, json


@DS.callback_query(F.data.startswith("skip_chat"))
async def _skip_chat(callback: CallbackQuery) -> None:
    chat_id: str = callback.data.replace("skip_chat ", "")
    database.avito.chats.skipped.add(chat_id)
    await callback.answer(f"Chat ({chat_id}) skipped")


@DS.callback_query(F.data.startswith("unignore_chat"))
async def _unignore_chat(callback: CallbackQuery) -> None:
    chat_id: str = callback.data.replace("unignore_chat ", "")
    json.avito.unignore_chat(chat_id)
    await callback.answer(f"Chat ({chat_id}) unignored")


@DS.callback_query(F.data.startswith("unignore_user"))
async def _unignore_user(callback: CallbackQuery) -> None:
    user_id: int = int(callback.data.replace("unignore_user ", ""))
    json.avito.unignore_user(user_id)
    await callback.answer(f"User ({user_id}) unignored")


@DS.callback_query(F.data.startswith("ignore_chat"))
async def _ignore_chat(callback: CallbackQuery) -> None:
    chat_id: str = callback.data.replace("ignore_chat ", "")
    json.avito.ignore_chat(chat_id)
    await callback.answer(f"Chat ({chat_id}) ignored")


@DS.callback_query(F.data.startswith("ignore_user"))
async def _ignore_user(callback: CallbackQuery) -> None:
    user_id: int = int(callback.data.replace("ignore_user ", ""))
    json.avito.ignore_user(user_id)
    await callback.answer(f"User ({user_id}) ignored")
