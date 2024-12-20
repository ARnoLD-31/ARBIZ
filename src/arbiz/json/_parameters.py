from . import _base


def avito() -> dict:
    return _base.get("avito")


def gemini() -> dict:
    return _base.get("gemini")


def telegram() -> dict:
    return _base.get("telegram")


def yam() -> dict:
    return _base.get("yandex_market")
