import aiosqlite

from . import _parameters
from ._exceptions import NoKeys
from ... import output


async def add(
        key: str,
        product: str,
        activation_type: str,
        mak: int,
        expired: int,
        link: str | None = None
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
            query,
            (
                key,
                product,
                activation_type,
                link,
                mak,
                expired
            )
        )
        await conn.commit()


async def get(
        chat_id: str,
        product: str,
) -> str:
    constant_kwargs: dict[str, str | bool] = {
        "product": product,
        "expired": False
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
        }
    )
    for kwarg in kwargs:
        for key in await _parameters.keys(**(kwarg | constant_kwargs)):
            sent_to_: None | list[str] = await _parameters.sent_to(key)
            if sent_to_ is None or chat_id not in sent_to_:
                await _parameters.sent_to(key, chat_id)
                output.info(chat_id, f'Key "{key}" sent')
                return key
    raise NoKeys()
