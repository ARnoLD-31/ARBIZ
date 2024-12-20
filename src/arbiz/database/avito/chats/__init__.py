import aiosqlite

from ._operations import skipped, process
from ._parameters import (
    chat_ids,
    messages,
    unread,
    advertisement,
    advertisement_code,
    user_id,
    name,
    ignored_chat,
    ignored_user,
    ignored
)

__all__: list[str] = [
    # _operations.py
    "skipped",
    "process",
    # _parameters.py
    "chat_ids",
    "messages",
    "unread",
    "advertisement",
    "advertisement_code",
    "user_id",
    "name",
    "ignored_chat",
    "ignored_user",
    "ignored"
]


async def initialize() -> None:
    query: str = """
        CREATE TABLE IF NOT EXISTS Clients
        (
            chat_id             TEXT    PRIMARY KEY,
            user_id             INTEGER NOT NULL,
            name                TEXT    NOT NULL,
            advertisement       TEXT,
            messages            TEXT    NOT NULL,
            unread              INTEGER NOT NULL
        )
    """
    async with aiosqlite.connect("clients.db") as conn:
        await conn.execute(query)
        await conn.commit()
