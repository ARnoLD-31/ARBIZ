from typing import Literal

import aiosqlite

from ... import _base
from ..._datatypes import NotGiven
from .... import json


async def _do(
        chat_id: str = None,
        name: str = None,
        value: str | int | list = NotGiven
) -> None | str | int | list:
    async with aiosqlite.connect("clients.db") as conn:
        if chat_id is None:
            return await _base.get(
                conn,
                "Clients",
                "chat_id",
                "1=1"
            )
        if value is NotGiven:
            return await _base.get(
                conn,
                "Clients",
                name,
                f"chat_id = '{chat_id}'"
            )
        await _base.set(
            conn,
            "Clients",
            name,
            value,
            f"chat_id = '{chat_id}'"
        )


async def chat_ids() -> list[str]:
    return await _do()


async def messages(
        chat_id: str,
        messages: NotGiven | list[dict] | dict = NotGiven
) -> list[dict] | None:
    if isinstance(messages, dict):
        new_messages: list[dict] = await _do(chat_id, "messages")
        new_messages.append(messages)
        return await _do(chat_id, "messages", new_messages)
    return await _do(chat_id, "messages", messages)


async def unread(
        chat_id: str,
        unread: NotGiven | int = NotGiven
) -> int | None:
    return await _do(chat_id, "unread", unread)


async def advertisement(
        chat_id: str,
        advertisement: NotGiven | str = NotGiven
) -> str | None:
    return await _do(chat_id, "advertisement", advertisement)


async def advertisement_code(
        chat_id: str
) -> Literal["KEY", "FLASHDRIVE", "UNKNOWN"]:
    advertisement_: str = (await advertisement(chat_id)).lower()
    if all(parameter in advertisement_ for parameter in ("флешка", "windows")):
        return "FLASHDRIVE"
    if all(parameter in advertisement_ for parameter in ("ключ", "windows")):
        return "KEY"
    return "UNKNOWN"


async def user_id(
        chat_id: str
) -> int:
    return await _do(chat_id, "user_id")


async def name(
        chat_id: str
) -> str:
    return await _do(chat_id, "name")


def ignored_chat(chat_id: str) -> bool:
    return chat_id in json.avito.ignored()["chat_ids"]


def ignored_user(user_id: int) -> bool:
    return user_id in json.avito.ignored()["user_ids"]


def ignored(chat_id: str, user_id: int) -> bool:
    return ignored_chat(chat_id) or ignored_user(user_id)
