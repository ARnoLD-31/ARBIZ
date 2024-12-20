import asyncio

from . import _tasks, api, config
from ._tasks import polling
from .. import output

__all__: list[str] = [
    "api",
    "config",
    # _tasks.py
    "polling"
]


async def initialize() -> None:
    asyncio.create_task(_tasks.update_access_token())
    await asyncio.sleep(10)
    config.user_id = (await api.user_info.account_data())["id"]
    output.info("MAIN", "Avito initialized")
