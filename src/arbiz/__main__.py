import asyncio
import sys
from argparse import Namespace

from . import arguments, output


async def initialize() -> None:
    args: Namespace = arguments.initialize()

    from . import database, telegram
    await database.initialize()

    if args.avito:
        from . import avito
        await avito.initialize()
        asyncio.create_task(avito.polling())
    if args.yandex_market:
        from . import yam
        await yam.initialize()
        asyncio.create_task(yam.polling())

    await telegram.initialize()


def main() -> None:
    try:
        asyncio.run(initialize())
    except KeyboardInterrupt:
        output.fatal_error("MAIN", "Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
