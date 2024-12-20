import os

_PATH: str = os.path.dirname(os.path.abspath(__file__))
with open(f"{_PATH}/key.txt", encoding="utf-8") as file:
    KEY: str = file.read()
