import base64
from queue import Queue
from typing import Literal

from ._exceptions import EmptyQueue, NoPrompt
from .. import json, text, c_requests

SAFETY_SETTINGS: list[dict[str, str]] = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]


api_keys: Queue = Queue()
api_keys.queue.extend(json.gemini.api_tokens())


def api_key() -> str:
    if api_keys.qsize() == 0:
        raise EmptyQueue()
    api_key_: str = api_keys.get()
    api_keys.put(api_key_)
    return api_key_


async def reformat_messages(
        avito_messages: list[dict],
        advertisement_code: Literal["KEY", "FLASHDRIVE", "UNKNOWN"]
) -> list[dict]:
    messages: list[dict] = []
    parts: list[dict] = []
    if advertisement_code == "KEY":
        messages = [
            {
                "role": "model",
                "parts": [
                    {
                        "text": text.prompts.KEYS
                    }
                ]
            }
        ]
    elif advertisement_code == "FLASHDRIVE":
        messages = [
            {
                "role": "model",
                "parts": [
                    {
                        "text": "" # TODO: Add flashdrive prompt
                    }
                ]
            }
        ]
    elif advertisement_code == "UNKNOWN":
        raise NoPrompt()
    for message in avito_messages:
        role: str = "model" if message["role"] == "seller" else "user"
        if "text" in message["message"].keys():
            parts = [
                {
                    "text": message["message"]["text"]
                }
            ]
        elif "image" in message["message"].keys():
            image_url: str = message["message"]["image"]
            image_bytes: bytes = await c_requests.get(image_url)
            image_base64: str = base64.b64encode(image_bytes).decode()
            parts = [
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                }
            ]
        messages.append(
            {
                "role": role,
                "parts": parts
            }
        )
    return messages
