import asyncio
import datetime

from . import api, config
from .. import database, text, output


async def _process_dbs_order(order: dict) -> None:
    id: int = order["id"]
    buyer_id: str = order["buyer"]["id"]
    key: str = await database.keys.get(buyer_id, "Windows 10 Pro")
    activate_till: str = datetime.date.strftime(
        datetime.date.today() + datetime.timedelta(days=14),
        "%d-%m-%Y",
    )
    items: list = []
    for item in order["items"]:
        data: dict = {
            "id": item["id"],
            "codes": [],
            "activate_till": activate_till,
        }

        for index in range(item["count"]):
            if item["count"] > 1:
                data["codes"].append(
                    f"{index + 1}. {key} (Ключ на {item["count"]} активации)"
                )
            else:
                data["codes"].append(key)

        if item == order["items"][0]:
            data["slip"] = text.yam.key.EMAIL
        else:
            data["slip"] = "Инструкция выше"

        items.append(data)

    await api.orders.send_dbs(config.DBS, id, items)
    chat_id: int = (await api.chats.create(id))["result"]["chatId"]
    await api.chats.send_message(chat_id, text.yam.key.CHAT)
    output.info("YAM", f'New purchase. Order: "{buyer_id}"')


async def polling() -> None:
    while config.polling:
        for order in (
            await api.orders.orders(config.DBS, status=["PROCESSING"])
        )["orders"]:
            asyncio.create_task(_process_dbs_order(order))
        output.info("YAM", "New iteration")
        await asyncio.sleep(60)
