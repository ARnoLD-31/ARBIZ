from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from . import _base
from .. import database, json


async def new_message(chat_id: str) -> None:
    user_id: int = await database.avito.chats.user_id(chat_id)
    name: str = await database.avito.chats.name(chat_id)
    message: dict = (
        await database.avito.chats.messages(chat_id)
    )[-1]["message"]
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder(
        [[
            InlineKeyboardButton(
                text="Manual answer",
                callback_data=f"manual_answer {chat_id}"
            )
        ]]
    )
    if database.avito.chats.ignored_user(user_id):
        type: str = "IGNORED USER"
        builder.add(
            InlineKeyboardButton(
                text="Ignore chat",
                callback_data=f"ignore_chat {chat_id}"
            ),
            InlineKeyboardButton(
                text="Unignore user",
                callback_data=f"unignore_user {user_id}"
            )
        )
    elif database.avito.chats.ignored_chat(chat_id):
        type: str = "IGNORED CHAT"
        builder.add(
            InlineKeyboardButton(
                text="Ignore user",
                callback_data=f"ignore_user {user_id}"
            ),
            InlineKeyboardButton(
                text="Unignore chat",
                callback_data=f"unignore_chat {chat_id}"
            )
        )
    elif chat_id in database.avito.chats.skipped:
        type: str = "SKIPPED"
        builder.add(
            InlineKeyboardButton(
                text="Ignore chat",
                callback_data=f"ignore_chat {chat_id}"
            ),
            InlineKeyboardButton(
                text="Ignore user",
                callback_data=f"ignore_user {user_id}"
            )
        )
    else:
        type: str = "NEED TO ANSWER"
        builder.add(
            InlineKeyboardButton(
                text="Skip for now",
                callback_data=f"skip_chat {chat_id}"
            ),
            InlineKeyboardButton(
                text="Ignore chat",
                callback_data=f"ignore_chat {chat_id}"
            ),
            InlineKeyboardButton(
                text="Ignore user",
                callback_data=f"ignore_user {user_id}"
            )
        )
    builder.adjust(1)
    if "text" in message:
        message_text: str = message["text"]
    else:
        message_text: str = "Нет текста"
    text: str = (
        f'[{type}] New message from "{name}"\n'
        f'UserID: "{user_id}" ChatID: "{chat_id}"\n'
        f"Message:\n"
        f'"{message_text}"'
    )
    for user_id in json.telegram.user_ids():
        await _base.BOT.send_message(
            user_id, text, reply_markup=builder.as_markup()
        )
