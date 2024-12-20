from .. import _parameters


def api_key() -> str:
    return _parameters.yam()["api_key"]
