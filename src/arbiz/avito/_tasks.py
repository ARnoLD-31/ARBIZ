import asyncio

from . import api, config
from .. import database, output


async def update_access_token() -> None:
    while True:
        token_info: dict[
            str, str | int
        ] = await api.authorization.access_token()
        config.access_token = token_info["access_token"]
        output.info("MAIN", "Access token updated")
        await asyncio.sleep(token_info["expires_in"] - 10)


async def polling() -> None:
    while config.polling:
        try:
            for chat in await api.messenger.chats(limit=2):
                asyncio.create_task(database.avito.chats.process(chat))
            output.info("AVITO", "New iteration")
        except TypeError:
            output.warning("AVITO", "Iteration skipped")
        finally:
            await asyncio.sleep(2)
