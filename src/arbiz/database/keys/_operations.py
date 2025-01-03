import aiosqlite

from . import _parameters
from ._exceptions import NoKeys
from .. import _base
from ... import output


async def info(key: str) -> dict[str, None | str | int]:
    return {
        "product": await _parameters.product(key),
        "activation_type": await _parameters.activation_type(key),
        "mak": await _parameters.mak(key),
        "expired": await _parameters.expired(key),
        "link": await _parameters.link(key),
    }


async def add(
    key: str,
    product: str,
    activation_type: str,
    mak: int,
    expired: int,
    link: str | None = None,
) -> None:
    query: str = """
        INSERT OR IGNORE INTO Keys 
        (
            key,
            product,
            activation_type,
            link,
            mak,
            expired
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """
    async with aiosqlite.connect("keys.db") as conn:
        await conn.execute(
            query, (key, product, activation_type, link, mak, expired)
        )
        await conn.commit()


async def delete(key: str) -> None:
    async with aiosqlite.connect("keys.db") as conn:
        await _base.delete(conn, "Keys", f"key = '{key}'")


async def get(
    chat_id: str,
    product: str,
) -> str:
    constant_kwargs: dict[str, str | bool] = {
        "product": product,
        "expired": False,
    }
    kwargs: tuple[dict[str, str | bool], ...] = (
        {
            "activation_type": "Online",
            "mak": True,
        },
        {
            "activation_type": "Online",
            "mak": False,
        },
        {
            "activation_type": "Phone",
        },
    )
    for kwarg in kwargs:
        for key in await _parameters.keys(**(kwarg | constant_kwargs)):
            sent_to_: None | list[str] = await _parameters.sent_to(key)
            if sent_to_ is None or chat_id not in sent_to_:
                await _parameters.sent_to(key, chat_id)
                output.info(chat_id, f'Key "{key}" sent')
                return key
    raise NoKeys()
