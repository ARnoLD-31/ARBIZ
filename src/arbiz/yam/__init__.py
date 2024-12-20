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
            await api.orders.send_dbs(
                _config.DBS,
                order["id"],
                [
                    {
                        "id": order["items"][0]["id"],
                        "codes": [
                            await database.keys.get(
                                order["buyer"]["id"],
                                "Windows 10 Pro"
                            )
                        ],
                        "slip": text.templates.KEY,
                        "activate_till": datetime.date.strftime(
                            datetime.date.today() + datetime.timedelta(days=7),
                            "%d-%m-%Y"
                        )
                    }
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
