import sys
from argparse import ArgumentParser, Namespace
from typing import Any

from . import json, output


ARGUMENTS: tuple[dict[str, Any], ...] = (
    {
        "flags": ("--version",),
        "help": "Show version and exit",
        "action": "store_true",
    },
    {
        "flags": ("--json", "-js"),
        "help": "Path to the json config",
        "type": str,
    },
    {
        "flags": ("--avito", "-av"),
        "help": "Enable Avito polling",
        "action": "store_true",
    },
    {
        "flags": ("--yandex_market", "-yam"),
        "help": "Enable Yandex Market polling",
        "action": "store_true",
    },
)


def _args() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    for argument in ARGUMENTS:
        parser.add_argument(*argument.pop("flags"), **argument)
    args: Namespace = parser.parse_args()

    if args.version:
        output.info("MAIN", "Program's version is 1.4.4")
        sys.exit(0)
    elif not args.json:
        parser.error("Json is empty. You must specify it: --json/-js")
    elif not args.avito and not args.yandex_market:
        parser.error(
            "You must specify at least one of the flags: "
            "--avito/-av or --yandex_market/-yam"
        )

    return args


def initialize() -> Namespace:
    args: Namespace = _args()

    json.config.path = args.json
    return args
