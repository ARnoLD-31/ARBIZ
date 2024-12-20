import os

_PATH: str = os.path.dirname(os.path.abspath(__file__))
with open(f"{_PATH}/keys.txt", encoding="utf-8") as file:
    KEYS: str = file.read()
