from typing import Any

from .. import config
from ... import database, c_requests


async def chats(
        *,
        limit: int = 100,
        offset: int = 0
) -> list[dict]:
    url: str = (
        f"https://api.avito.ru/messenger/v2/accounts/"
        f"{config.user_id}/chats"
    )
    kwargs: dict = {
        "params": {
            "limit": limit,
            "offset": offset,
        },
        "headers": {
            "Authorization": f"Bearer {config.access_token}"
        }
    }
    response: dict = await c_requests.get(url, **kwargs)
    return response["chats"]


async def send_message(
        *,
        chat_id: str,
        text: str
) -> dict[str, Any]:
    url: str = (
        f"https://api.avito.ru/messenger/v1/accounts/"
        f"{config.user_id}/chats/{chat_id}/messages"
    )
    kwargs: dict = {
        "json": {
            "message": {
                "text": text
            },
            "type": "text",
        },
        "headers": {
            "Authorization": f"Bearer {config.access_token}"
        }
    }
    response: dict = await c_requests.post(url, **kwargs)
    database_message: dict = {
        "role": "seller",
        "message": {"text": text}
    }
    await database.avito.chats.messages(chat_id, database_message)
    return response


async def blacklist(
        *,
        user_id: int,
        chat_id: str
) -> dict[str, Any]:
    url: str = (
        f"https://api.avito.ru/messenger/v2/accounts/"
        f"{config.user_id}/blacklist"
    )
    kwargs: dict = {
        "json": {
            "users": [
                {
                    "context": {
                        "item_id": 0,
                        "reason_id": 4
                    },
                    "user_id": user_id
                }
            ],
        },
        "headers": {
            "Authorization": f"Bearer {config.access_token}"
        }
    }
    response: dict = await c_requests.post(url, **kwargs)
    await database.avito.chats.unread(chat_id, 0)
    return response


async def mark_chat_as_read(
        *,
        chat_id: str
) -> dict[str, Any]:
    url: str = (
        f"https://api.avito.ru/messenger/v1/accounts/"
        f"{config.user_id}/chats/{chat_id}/read"
    )
    kwargs: dict = {
        "headers": {
            "Authorization": f"Bearer {config.access_token}"
        }
    }
    response: dict = await c_requests.post(url, **kwargs)
    return response
