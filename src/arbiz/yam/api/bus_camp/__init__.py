from typing import Literal

from .... import json, c_requests

async def campaigns(
        page: int = 1,
        page_size: int = None
) -> dict[Literal["campaigns", "pager"], list[dict] | dict]:
    url: str = "https://api.partner.market.yandex.ru/campaigns"
    kwargs: dict = {
        "headers": {
            "Api-Key": json.yam.api_key()
        },
        "params": {
            "page": page
        }
    }
    if page_size is not None:
        kwargs["params"]["pageSize"] = page_size
    return await c_requests.get(url, **kwargs)
