from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from .. import json, output

DS: Dispatcher = Dispatcher()
BOT: Bot = Bot(token=json.telegram.bot_token())
COMMANDS: list[BotCommand] = [
    BotCommand(command="start_avito", description="Starts avito polling"),
    BotCommand(command="stop_avito", description="Stops avito polling"),
    BotCommand(command="show_keys", description="Shows keys"),
    BotCommand(command="add_keys", description="Adds keys")
]

async def initialize() -> None:
    output.info("MAIN", "Telegram initialized")
    await BOT.set_my_commands(COMMANDS)
    await DS.start_polling(BOT)
