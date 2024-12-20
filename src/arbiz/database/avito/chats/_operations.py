import asyncio
import json

import aiosqlite

from . import _parameters
from ... import keys
from .... import avito, gemini, telegram, output

_delays: dict[str, int] = {}
skipped: set[str] = set()


def _convert_last_message(last_message: dict) -> dict:
    message: dict = {}
    if last_message["direction"] == "in":
        message["role"] = "buyer"
    else:
        message["role"] = "seller"
    if "image" in last_message["content"].keys():
        message["message"] = {
            "image": list(
                last_message["content"]["image"]["sizes"].values()
            )[0]
        }
    else:
        message["message"] = last_message["content"]
    return message


async def _process_keywords(chat_id: str, response: str) -> str:
    if "SEND_KEY W10P" in response:
        key: str = await keys.get(chat_id, "Windows 10 Pro")
        response = response.replace("SEND_KEY W10P", key)
    return response


async def _add(
    chat_id: str,
    user_id: int,
    name: str,
    advertisement: str,
    messages: list,
    unread: int
) -> None:
    query: str = """
        INSERT OR IGNORE INTO Clients 
        (
            chat_id,
            user_id,
            name,
            advertisement,
            messages,
            unread
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """
    async with aiosqlite.connect("clients.db") as conn:
        await conn.execute(
            query,
            (
                chat_id,
                user_id,
                name,
                advertisement,
                json.dumps(messages, ensure_ascii=False),
                unread
            )
        )
        await conn.commit()

    if chat_id not in _delays:
        _delays[chat_id] = 0


async def _answer(chat_id: str, user_id: int) -> None:
    if _delays[chat_id] != 0:
        _delays[chat_id] += 20
        return
    _delays[chat_id] = 60
    while _delays[chat_id] > 0:
        await asyncio.sleep(1)
        _delays[chat_id] -= 1

    messages: list[dict] = await _parameters.messages(chat_id)
    if (not _parameters.ignored(chat_id, user_id) and
            chat_id not in skipped and
            messages[-1]["role"] == "buyer"):
        response: str = await _process_keywords(
            chat_id,
            await gemini.answer(chat_id)
        )
        await avito.api.messenger.send_message(chat_id=chat_id, text=response)
        await avito.api.messenger.mark_chat_as_read(chat_id=chat_id)
    elif chat_id in skipped:
        skipped.remove(chat_id)


async def process(raw: dict) -> None:
    chat_id: str = raw["id"]
    user_id: int = raw["users"][0]["id"]
    last_message: dict = raw["last_message"]
    name: str = raw["users"][0]["name"]
    advertisement: str = raw["context"]["value"]["title"]
    message: dict = _convert_last_message(last_message)
    unread: int = 0 if "read" in raw["last_message"] else 1
    messages: list[dict] = await _parameters.messages(chat_id)
    await _add(chat_id, user_id, name, advertisement, [message], unread)
    await _parameters.unread(chat_id, unread)
    if len(messages) == 0 or message != messages[-1]:
        await _parameters.messages(chat_id, message)
        if message["role"] == "buyer" and unread:
            await telegram.notifications.new_message(chat_id)
            if (not _parameters.ignored(chat_id, user_id)
                    and chat_id not in skipped):
                output.info(chat_id, "Need to answer")
                await _answer(chat_id, user_id)
