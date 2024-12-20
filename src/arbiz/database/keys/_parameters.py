import aiosqlite

from .. import _base
from .._datatypes import NotGiven


async def _do(
        name: str,
        condition: str,
        value: NotGiven | str | int = NotGiven,
) -> None | str | int | list | tuple:
    async with aiosqlite.connect("keys.db") as conn:
        if value is NotGiven:
            return await _base.get(conn, "Keys", name, condition)
        await _base.set(conn, "Keys", name, value, condition)


async def keys(
        product: str = None,
        activation_type: str = None,
        link: str = None,
        mak: int = None,
        expired: int = None,
) -> tuple[str, ...]:
    condition: str = "1=1"
    if product is not None:
        condition += f" AND product = '{product}'"
    if activation_type is not None:
        condition += f" AND activation_type = '{activation_type}'"
    if link is not None:
        condition += f" AND link = '{link}'"
    if mak is not None:
        condition += f" AND mak = {mak}"
    if expired is not None:
        condition += f" AND expired = {expired}"
    keys: tuple[str, ...] | str = await _do("key", condition)
    if isinstance(keys, str):
        keys = (keys,)
    return keys


async def product(
        key: str,
        product: NotGiven | str = NotGiven
) -> str | None:
    return await _do("product", f"key = '{key}'", product)


async def activation_type(
        key: str,
        activation_type: NotGiven | str = NotGiven
) -> str | None:
    return await _do("activation_type", f"key = '{key}'", activation_type)


async def link(
        key: str,
        link: None | str = NotGiven
) -> str | None:
    return await _do("link", f"key = '{key}'", link)


async def mak(
        key: str,
        mak: NotGiven | int = NotGiven
) -> int | None:
    return await _do("mak", f"key = '{key}'", mak)


async def expired(
        key: str,
        expired: NotGiven | int = NotGiven
) -> int | None:
    return await _do("expired", f"key = '{key}'", expired)


async def sent_to(
        key: str,
        sent_to: NotGiven | str | list[str] = NotGiven
) -> None | list[str]:
    if isinstance(sent_to, str):
        previous_sent_to: None | list[str] = await _do(
            "sent_to",
            f"key = '{key}'"
        )
        if previous_sent_to is None:
            sent_to = [sent_to]
        else:
            previous_sent_to.append(sent_to)
            sent_to = previous_sent_to
    return await _do("sent_to", f"key = '{key}'", sent_to)
