from ... import _config
from .... import json, c_requests


async def create(order_id: int) -> dict:
    url: str = f"https://api.partner.market.yandex.ru/businesses/{_config.business_id}/chats/new"
    kwargs: dict = {
        "headers": {"Api-Key": json.yam.api_key()},
        "json": {"orderId": order_id},
    }
    return await c_requests.post(url, **kwargs)


async def send_message(chat_id: int, message: str) -> dict:
    url: str = f"https://api.partner.market.yandex.ru/businesses/{_config.business_id}/chats/message"
    kwargs: dict = {
        "headers": {"Api-Key": json.yam.api_key()},
        "params": {"chatId": chat_id},
        "json": {"message": message},
    }
    return await c_requests.post(url, **kwargs)
