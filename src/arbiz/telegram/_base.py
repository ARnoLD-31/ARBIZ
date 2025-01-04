from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from .. import json, output

DS: Dispatcher = Dispatcher()
BOT: Bot = Bot(token=json.telegram.bot_token())
COMMANDS: dict[str, str] = {
    "status": "Program's status",
    "terminate": "Terminate program",
    "start_yam": "Start Yandex Market polling",
    "stop_yam": "Stop Yandex Market polling",
    "start_avito": "Start Avito polling",
    "stop_avito": "Stop Avito polling",
    "show_keys": "Show keys",
    "add_key": "Add key",
}


async def initialize() -> None:
    output.info("MAIN", "Telegram initialized")
    await BOT.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in COMMANDS.items()
        ]
    )
    await DS.start_polling(BOT)
