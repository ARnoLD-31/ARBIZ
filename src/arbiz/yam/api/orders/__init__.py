from typing import Literal

from .... import json, c_requests


async def orders(
        campaign_id: int,
        fake: bool = None,
        waiting_for_ca: bool = None,
        status: list[Literal[
            "PLACING", "RESERVED", "UNPAID", "PROCESSING", "DELIVERY",
            "PICKUP", "DELIVERED", "CANCELLED", "PENDING",
            "PARTIALLY_RETURNED", "RETURNED", "UNKNOWN"
        ]] = None
) -> dict[Literal["orders", "pager", "paging"], dict | list[dict]]:
    url: str = f"https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders"
    kwargs: dict = {
        "headers": {
            "Api-Key": json.yam.api_key()
        },
        "params": {}
    }
    if fake is True:
        kwargs["params"]["fake"] = "true"
    elif fake is False:
        kwargs["params"]["fake"] = "false"
    if waiting_for_ca is not None:
        kwargs["params"]["onlyWaitingForCancellationApprove"] = waiting_for_ca
    if status is not None:
        kwargs["params"]["status"] = status
    return await c_requests.get(url, **kwargs)


async def send_dbs(
        campaign_id: int,
        order_id: int,
        items: list[dict[str, str | int | list[str]]]
) -> dict:
    url: str = f"https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders/{order_id}/deliverDigitalGoods"
    kwargs: dict = {
        "headers": {
            "Api-Key": json.yam.api_key()
        },
        "json": {
            "items": items
        }
    }
    return await c_requests.post(url, **kwargs)
