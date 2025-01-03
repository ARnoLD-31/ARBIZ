import sys
from argparse import ArgumentParser, Namespace

from . import json, output


def _args() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--version",
        action="store_true",
        help="Shows program's version",
    )
    parser.add_argument(
        "--json",
        "-js",
        type=str,
        help="Path to the json file",
    )
    parser.add_argument(
        "--avito", "-av", help="Enables Avito polling", action="store_true"
    )
    parser.add_argument(
        "--yandex_market",
        "-yam",
        help="Enables Yandex Market polling",
        action="store_true",
    )
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
