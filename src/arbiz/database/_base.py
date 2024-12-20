import json
from json import JSONDecodeError

from aiosqlite import Connection

from ._exceptions import ValueNotFound


async def get(
        conn: Connection,
        table_name: str,
        name: str,
        condition: str
) -> None | str | int | list | tuple:
    query: str = f"SELECT {name} FROM {table_name} WHERE {condition}"
    async with await conn.execute(query) as cursor:
        response: list = await cursor.fetchall()
    try:
        if len(response) == 1:
            result: str = response[0][0]
        else:
            result: tuple = tuple(element[0] for element in response)
    except TypeError as exception:
        raise ValueNotFound() from exception
    try:
        result: str | int | list = json.loads(result)
    except (JSONDecodeError, TypeError):
        if result == "":
            result: None = None
    return result


async def set(
        conn: Connection,
        table_name: str,
        name: str,
        value: str | int | list,
        condition: str
) -> None:
    query: str = f"""
        UPDATE {table_name}
        SET {name} = ?
        WHERE {condition}
    """
    if isinstance(value, list):
        value: str = json.dumps(value, ensure_ascii=False)
    elif isinstance(value, bool):
        value: int = int(value)
    await conn.execute(query, (value,))
    await conn.commit()
