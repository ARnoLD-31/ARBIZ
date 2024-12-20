from argparse import ArgumentParser, Namespace

from . import json


def _args() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--json",
        "-js",
        type=str,
        required=True,
        help="Path to the json file",
    )
    parser.add_argument(
        "--avito",
        "-av",
        help="Enables Avito polling",
        action="store_true"
    )
    parser.add_argument(
        "--yandex_market",
        "-yam",
        help="Enables Yandex Market polling",
        action="store_true"
    )
    args: Namespace = parser.parse_args()

    if not args.avito and not args.yandex_market:
        parser.error("You must specify at least one of the flags: "
                     "--avito/-av or --yandex_market/-yam")

    return args


def initialize() -> Namespace:
    args: Namespace = _args()

    json.config.path = args.json
    return args
