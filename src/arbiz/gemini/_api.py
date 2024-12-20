import asyncio
import functools
from asyncio import AbstractEventLoop
from typing import Any

import google.generativeai
from google.generativeai import GenerativeModel
from google.generativeai.types import GenerateContentResponse

from . import _config, _exceptions
from ._exceptions import GeminiException
from .. import database, output


async def _do_request(
        messages: list[dict] | str,
        model: str
) -> GenerateContentResponse:
    loop: AbstractEventLoop = asyncio.get_event_loop()
    kwargs: dict[str, Any] = {
        "contents": messages,
        "safety_settings": _config.SAFETY_SETTINGS
    }
    api_key: str = _config.api_key()
    google.generativeai.configure(api_key=api_key)
    model: GenerativeModel = GenerativeModel(model)
    # noinspection PyTypeChecker
    response: GenerateContentResponse = await loop.run_in_executor(
        None,
        functools.partial(
            model.generate_content,
            **kwargs
        )
    )
    return response


async def _process_response(
        chat_id: str,
        model: str,
        messages: list[dict] | str
) -> str:
    attempts: int = 0
    while attempts <= _config.api_keys.qsize() * 2:
        try:
            response: GenerateContentResponse = await _do_request(
                messages,
                model
            )
            return response.text
        # pylint: disable=broad-except
        except Exception as original_exception:
            print(original_exception)
            exception: GeminiException = _exceptions.handle(
                chat_id,
                original_exception
            )
            await asyncio.sleep(5)
        finally:
            attempts += 1
    # noinspection PyUnboundLocalVariable
    output.error(chat_id, f'Custom exception: "{exception}"')
    raise exception


# noinspection PyTypeChecker
async def answer(
        chat_id: str,
        model: str = "gemini-1.5-pro",
) -> str:
    avito_messages: list[dict] = await database.avito.chats.messages(chat_id)
    messages: list[dict] = await _config.reformat_messages(
        avito_messages,
        await database.avito.chats.advertisement_code(chat_id)
    )
    output.info(chat_id, "Responding...")
    response_text: str = await _process_response(chat_id, model, messages)
    return response_text.strip()
