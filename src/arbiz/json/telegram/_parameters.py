from .. import _parameters


def user_ids() -> list[int]:
    return _parameters.telegram()["user_ids"]


def bot_token() -> str:
    return _parameters.telegram()["bot_token"]
