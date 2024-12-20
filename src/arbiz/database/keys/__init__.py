import aiosqlite

from ._exceptions import NoKeys
from ._operations import add, get
from ._parameters import (
    keys,
    product,
    activation_type,
    link,
    mak,
    expired,
    sent_to
)

__all__: list[str] = [
    # _exceptions.py
    "NoKeys",
    # _operations.py
    "add",
    "get",
    # _parameters.py
    "keys",
    "product",
    "activation_type",
    "link",
    "mak",
    "expired",
    "sent_to"
]


async def initialize() -> None:
    query: str = """
        CREATE TABLE IF NOT EXISTS Keys
        (
            key                 TEXT    PRIMARY KEY UNIQUE,
            product             TEXT    NOT NULL,
            activation_type     TEXT    NOT NULL,
            link                TEXT,
            mak                 INTEGER NOT NULL,
            expired             INTEGER NOT NULL,
            sent_to             TEXT
        )
    """
    async with aiosqlite.connect("keys.db") as conn:
        await conn.execute(query)
        await conn.commit()
