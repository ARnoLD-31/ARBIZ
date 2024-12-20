from .. import config
from ... import c_requests


async def account_data() -> dict[str, str | int]:
    url: str = "https://api.avito.ru/core/v1/accounts/self"
    kwargs: dict = {
        "headers": {
            "Authorization": f"Bearer {config.access_token}"
        }
    }
    return await c_requests.get(url, **kwargs)
