import asyncio
import datetime

from . import api, _config
from .. import database, text, output

__all__: list[str] = ["api"]


async def polling() -> None:
    while True:
        for order in (await api.orders.orders(
                _config.DBS,
                status=["PROCESSING"]
        ))["orders"]:
            key: str = await database.keys.get(
                order["buyer"]["id"],
                "Windows 10 Pro")
            await api.orders.send_dbs(
                _config.DBS,
                order["id"],
                [
                    {
                        "id": item["id"],
                        "codes": [
                            f"{index + 1}. {key} (Ключ на {item["count"]} активации)"
                            if item["count"] > 1 else
                            key
                            for index in range(item["count"])
                        ],
                        "slip":
                            text.templates.KEY
                            if item == order["items"][0] else
                            "Инструкция выше",
                        "activate_till": datetime.date.strftime(
                            datetime.date.today() + datetime.timedelta(
                                days=14),
                            "%d-%m-%Y"
                        )
                    }
                    for item in order["items"]
                ]
            )
            output.info(
                "YAM",
                f'New purchase. Order: "{order["buyer"]["id"]}"'
            )
        output.info("YAM", "New iteration")
        await asyncio.sleep(60)


async def initialize() -> None:
    for campaign in (await api.bus_camp.campaigns())["campaigns"]:
        if campaign["placementType"] == "DBS":
            _config.DBS = campaign["id"]
