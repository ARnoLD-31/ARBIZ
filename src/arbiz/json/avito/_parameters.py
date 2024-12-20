from typing import Literal

from .. import _parameters


def ignored() -> dict[Literal["chat_ids", "user_ids"], list[int | str]]:
    return _parameters.avito()["ignored"]


def client_id() -> str:
    return _parameters.avito()["client_id"]


def client_secret() -> str:
    return _parameters.avito()["client_secret"]
