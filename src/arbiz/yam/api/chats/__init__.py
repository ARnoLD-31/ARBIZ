from typing import Literal

from ... import config
from .... import json, c_requests


async def create(order_id: int) -> dict:
    url: str = f"https://api.partner.market.yandex.ru/businesses/{config.business_id}/chats/new"
    kwargs: dict = {
        "headers": {"Api-Key": json.yam.api_key()},
        "json": {"orderId": order_id}
    }
    return await c_requests.post(url, **kwargs)


async def history(
        chat_id: int,
        limit: int = 100,
        message_id_from: int = 1
) -> dict:
    url: str = f"https://api.partner.market.yandex.ru/businesses/{config.business_id}/chats/history"
    kwargs: dict = {
        "headers": {"Api-Key": json.yam.api_key()},
        "params": {"chatId": chat_id, "limit": limit},
        "json": {"messageIdFrom": message_id_from}
    }
    return await c_requests.post(url, **kwargs)


async def send_message(chat_id: int, message: str) -> dict:
    url: str = f"https://api.partner.market.yandex.ru/businesses/{config.business_id}/chats/message"
    kwargs: dict = {
        "headers": {"Api-Key": json.yam.api_key()},
        "params": {"chatId": chat_id},
        "json": {"message": message}
    }
    return await c_requests.post(url, **kwargs)


async def chat_list(
        limit: int,
        order_ids: list[int],
        types: list[Literal["CHAT", "ARBITRAGE"]],
        statuses: tuple | list[Literal[
            "NEW", "WAITING_FOR_CUSTOMER", "WAITING_FOR_PARTNER",
            "WAITING_FOR_ARBITER", "WAITING_FOR_MARKET", "FINISHED"
        ]] = (
            "NEW", "WAITING_FOR_CUSTOMER", "WAITING_FOR_PARTNER",
            "WAITING_FOR_ARBITER", "WAITING_FOR_MARKET", "FINISHED"
        )
) -> dict:
    url: str = f"https://api.partner.market.yandex.ru/businesses/{config.business_id}/chats"
    if isinstance(statuses, tuple):
        statuses: list = list(statuses)
    kwargs: dict = {
        "headers": {"Api-Key": json.yam.api_key()},
        "params": {"limit": limit},
        "json": {"orderIds": order_ids, "statuses": statuses, "types": types}
    }
    return await c_requests.post(url, **kwargs)
