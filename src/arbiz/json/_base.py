import json

from . import config


def get(*keys: str) -> str | int | dict | list:
    with open(config.path, "r", encoding="utf-8") as file:
        value: str | int | dict = json.load(file)
    for key in keys:
        value = value[key]
    return value

def set(*keys: str, value: str | list) -> None:
    all_settings: dict = get()
    old_value: str | int | dict = all_settings
    for key in keys[:-1]:
        old_value = old_value[key]
    old_value[keys[-1]] = value
    with open(config.path, "w", encoding="utf-8") as file:
        json.dump(all_settings, file, indent=4)
