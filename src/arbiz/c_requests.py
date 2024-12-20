import asyncio

from aiohttp import ClientConnectorError, ClientSession

from . import output

_MAX_ATTEMPTS: int = 10


async def _fetch(url: str, method: str, **kwargs: dict):
    attempts: int = 0
    while attempts < _MAX_ATTEMPTS:
        try:
            async with ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    content_type = \
                        response.headers.get("Content-Type", "").lower()
                    if "application/json" in content_type:
                        return await response.json()
                    if "text/" in content_type:
                        return await response.text()
                    return await response.read()
        except ClientConnectorError:
            await asyncio.sleep(5)
            attempts += 1
    output.error("", f'Error with request. URL: "{url}"')


async def get(url: str, **kwargs: dict):
    return await _fetch(url, "GET", **kwargs)


async def post(url: str, **kwargs: dict):
    return await _fetch(url, "POST", **kwargs)
