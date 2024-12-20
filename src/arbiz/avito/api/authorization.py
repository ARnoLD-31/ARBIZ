from ... import json, c_requests


async def access_token() -> dict[str, str | int]:
    url: str = "https://api.avito.ru/token"
    kwargs: dict = {
        "data": {
            "client_id": json.avito.client_id(),
            "client_secret": json.avito.client_secret(),
            "grant_type": "client_credentials",
        }
    }
    return await c_requests.post(url, **kwargs)
