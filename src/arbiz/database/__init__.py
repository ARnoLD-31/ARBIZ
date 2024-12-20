from . import avito, keys
from ._datatypes import NotGiven
from ._exceptions import ValueNotFound
from .. import output

__all__: list[str] = [
    "avito",
    "keys",
    # _datatypes.py
    "NotGiven",
    # _exceptions.py
    "ValueNotFound"
]


async def initialize() -> None:
    await avito.chats.initialize()
    await keys.initialize()
    output.info("MAIN", "Database initialized")
