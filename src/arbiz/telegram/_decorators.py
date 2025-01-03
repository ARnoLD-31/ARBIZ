import inspect
from typing import Any, Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from .. import json


def security(function: Callable) -> Callable:
    async def wrapper(
        object: Message | CallbackQuery, state: FSMContext
    ) -> None:
        user_id: int = object.from_user.id
        kwargs_keys: tuple[str, ...] = tuple(
            inspect.signature(function).parameters.keys()
        )
        kwargs: dict[str, Any] = {}
        if "state" in kwargs_keys:
            kwargs["state"] = state

        if user_id not in json.telegram.user_ids():
            await object.answer("Access denied")
        else:
            await function(object, **kwargs)

    return wrapper
