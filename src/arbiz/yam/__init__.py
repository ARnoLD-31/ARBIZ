from . import api, config
from ._tasks import polling


__all__: list[str] = [
    "api",
    "config",
    # _tasks.py
    "polling",
]


async def initialize() -> None:
    for campaign in (await api.bus_camp.campaigns())["campaigns"]:
        if campaign["placementType"] == "DBS":
            config.DBS = campaign["id"]
            config.business_id = campaign["business"]["id"]
