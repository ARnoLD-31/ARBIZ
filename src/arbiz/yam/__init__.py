from . import api, _config
from ._tasks import polling


__all__: list[str] = ["api", "polling"]


async def initialize() -> None:
    for campaign in (await api.bus_camp.campaigns())["campaigns"]:
        if campaign["placementType"] == "DBS":
            _config.DBS = campaign["id"]
            _config.business_id = campaign["business"]["id"]
